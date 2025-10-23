from flask import Flask, jsonify, request
from datetime import datetime, timedelta
from pydantic import BaseModel, Field, field_validator
import MetaTrader5 as mt5

# ==============================
# 🚀 Cấu hình Flask
# ==============================
app = Flask(__name__)

# ==============================
# 📦 Pydantic Models (Schema)
# ==============================
class AccountInfoRequest(BaseModel):
    """Schema for account info request"""
    login: int = Field(..., description="MT5 account login number")
    password: str = Field(..., description="MT5 account password")
    server: str = Field(..., description="MT5 server name")


class HistoryRequest(BaseModel):
    """Schema for history request"""
    login: int = Field(..., description="MT5 account login number")
    password: str = Field(..., description="MT5 account password")
    server: str = Field(..., description="MT5 server name")
    from_date: str = Field(..., description="Start date in YYYY-MM-DD format")
    to_date: str = Field(..., description="End date in YYYY-MM-DD format")

    @field_validator("from_date", "to_date")
    @classmethod
    def validate_date_format(cls, v):
        """Validate YYYY-MM-DD format"""
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")


# ==============================
# ⚙️ Cấu hình mặc định MT5
# ==============================
MT5_DEFAULT_PATH = "/home/schaffen/.wine/drive_c/Program Files/MetaTrader 5/terminal64.exe"

def initialize_mt5(login: int, password: str, server: str):
    """Initialize MetaTrader 5 connection"""
    mt5_settings = {
        "path": MT5_DEFAULT_PATH,
        "login": login,
        "password": password,
        "server": server,
        "portable": False,
    }

    if not mt5.initialize(**mt5_settings):
        return False, mt5.last_error()
    return True, None


# ==============================
# 🧩 API Endpoints
# ==============================
@app.route("/api/v1/account-info", methods=["POST"])
def get_account_info():
    """Get current account information"""
    try:
        request_data = request.get_json()
        if not request_data:
            return jsonify({"status": "error", "message": "Request body is required"}), 400

        # Validate request
        account_request = AccountInfoRequest(**request_data)

        # Connect to MT5
        success, error = initialize_mt5(
            account_request.login,
            account_request.password,
            account_request.server
        )
        if not success:
            return jsonify({"status": "error", "message": f"MT5 init failed: {error}"}), 500

        # Fetch account info
        account_info = mt5.account_info()
        if account_info is None:
            return jsonify({
                "status": "error",
                "message": "Failed to get account info",
                "details": mt5.last_error(),
            }), 500

        # Serialize
        account_dict = {
            k: (v.isoformat() if isinstance(v, datetime) else v)
            for k, v in account_info._asdict().items()
        }

        return jsonify({"status": "success", "data": account_dict}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        mt5.shutdown()


@app.route("/api/v1/history", methods=["POST"])
def get_history():
    """Get trading history within specified date range"""
    try:
        request_data = request.get_json()
        if not request_data:
            return jsonify({"status": "error", "message": "Request body is required"}), 400

        # Validate request
        history_request = HistoryRequest(**request_data)

        # Connect to MT5
        success, error = initialize_mt5(
            history_request.login,
            history_request.password,
            history_request.server
        )
        if not success:
            return jsonify({"status": "error", "message": f"MT5 init failed: {error}"}), 500

        # Parse date range
        from_date = datetime.strptime(history_request.from_date, "%Y-%m-%d")
        to_date = datetime.strptime(history_request.to_date, "%Y-%m-%d") + timedelta(days=1)

        # Get history deals
        deals = mt5.history_deals_get(from_date, to_date)
        if deals is None:
            return jsonify({
                "status": "error",
                "message": f"No deals found or MT5 error: {mt5.last_error()}"
            }), 404

        deals_data = []
        for deal in deals:
            d = deal._asdict()
            if "time" in d:
                d["time"] = datetime.fromtimestamp(d["time"]).isoformat()
            deals_data.append(d)

        return jsonify({
            "status": "success",
            "data": deals_data,
            "count": len(deals_data),
            "date_range": {
                "from": history_request.from_date,
                "to": history_request.to_date,
            },
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        mt5.shutdown()


@app.route("/api/v1/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Finance MCP API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }), 200


# ==============================
# ⚠️ Error Handlers
# ==============================
@app.errorhandler(404)
def not_found(_):
    return jsonify({"status": "error", "message": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(_):
    return jsonify({"status": "error", "message": "Internal server error"}), 500


# ==============================
# 🏁 Entry Point
# ==============================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8386
    )
