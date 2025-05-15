from flask import Blueprint, request
from api.repository.plan import PlanRepositoryImpl

app = Blueprint('calendar_api', __name__)

# ユーザー情報取得API
@app.route('/get_user', methods=["GET"])
def get_user():
    return PlanRepositoryImpl().get_user()

# 予定追加API
@app.route('/setplan', methods=["POST"])
def setplan():
    data = request.get_json()
    return PlanRepositoryImpl().setplan(data)

# 選択した予定取得API
@app.route('/getplan', methods=["POST"])
def getplan():
    data = request.get_json()
    return PlanRepositoryImpl().getplan(data)

# 予定修正API
@app.route('/editplan', methods=["POST"])
def editplan():
    data = request.get_json()
    return PlanRepositoryImpl().editplan(data)

# 予定削除API
@app.route('/deleteplan', methods=["POST"])
def deleteplan():
    data = request.get_json()
    return PlanRepositoryImpl().deleteplan(data)