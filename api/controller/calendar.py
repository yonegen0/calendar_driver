# controllers/calendar_controller.py
from flask import Blueprint, request, current_app, jsonify

import api.external as external
from api.models.calendar import User, Plan

app = Blueprint('calendar_api', __name__)

# ユーザー情報取得API
@app.route('/get_user', methods=["GET"])
def get_user():
    try:
        # データベースから最初のユーザーを取得
        user = external.db.session.query(User).first()
        # ユーザーが存在しない場合
        if user is None:
            # 新しい User オブジェクトを作成
            user = User()
            # アプリケーションコンテキスト内でデータベースに新しいユーザーを追加し、コミットする
            with current_app.app_context():
                external.db.session.add(user)
                external.db.session.commit()
        
        plans = external.db.session.query(Plan)\
        .filter(Plan.user_id == user.id)
        plans_json = {}
        # 取得した予定を辞書に格納
        for plan in plans:
            # 各予定の情報を辞書に追加
            plans_json[plan.id] = {
                'start_date': plan.start_date,
                'plan_text': plan.plan_text
            }
        
        print(plans_json)
        
        # ユーザーオブジェクトを JSON に変換して返す
        return jsonify(plans_json), 200
    except Exception as e:
        return "", 500

# 予定追加API
@app.route('/setplan', methods=["POST"])
def setplan():
    if request.is_json:
        try:
            data = request.get_json() # dataは辞書
            for item in data: # リストの各要素（辞書）を処理
                date = item['date']
                text = item['text']
            if date == '' or text == '':
                return "値が入っていません", 400
            # データベースから最初のユーザーを取得
            user = external.db.session.query(User).first()
            
            # 新しい Plan オブジェクトを作成
            plan = Plan(
                user_id = user.id,
                start_date = date ,
                plan_text = text,
            )
            # ユーザーの plans リストに新しい予定を追加
            user.plans.append(plan)
            # データベースに変更をコミット
            external.db.session.commit()

            return "", 200
        except Exception as e:
            print("JSON データの処理中にエラーが発生しました:", e)
            return "", 400
    else:
        return "", 400

# 選択した予定取得API
@app.route('/getplan', methods=["POST"])
def getplan():
    if request.is_json:
        try:
            data = request.get_json() # dataは辞書
            # 'id' を取得し、整数に変換
            for item in data:
                id_value = item.get('id')
            if id_value is not None:
                id = int(id_value)  
            # 予定取得
            plan = external.db.session.query(Plan)\
            .filter(Plan.id == id).first()
            # 予定をjsonに変換
            plan_json = {
                'start_date': plan.start_date,
                'plan_text': plan.plan_text
            }

            return jsonify(plan_json), 200
        except Exception as e:
            print("JSON データの処理中にエラーが発生しました:", e)
            return "", 400
    else:
        return "", 400

# 予定修正API
@app.route('/editplan', methods=["POST"])
def editplan():
    if request.is_json:
        try:
            data = request.get_json() # dataは辞書
            # 'id' を取得し、整数に変換
            for item in data:
                id_value = item.get('id')
                date = item['date']
                text = item['text']
            if date == '' or text == '':
                return "値が入っていません", 400
            if id_value is not None:
                id = int(id_value)  
            # 予定修正
            plan = external.db.session.query(Plan)\
            .filter(Plan.id == id).first()
            plan.start_date = date
            plan.plan_text = text
            external.db.session.commit()
            
            return "", 200
        except Exception as e:
            print("JSON データの処理中にエラーが発生しました:", e)
            return "", 400
    else:
        return "", 400
    
# 予定削除API
@app.route('/deleteplan', methods=["POST"])
def deleteplan():
    if request.is_json:
        try:
            data = request.get_json() # dataは辞書
            # 'id' を取得し、整数に変換
            for item in data:
                id_value = item.get('id')
            if id_value is not None:
                id = int(id_value)  
            # 予定削除
            external.db.session.query(Plan).filter(Plan.id == id).delete()
            external.db.session.commit()

            return "", 200
        except Exception as e:
            print("JSON データの処理中にエラーが発生しました:", e)
            return "", 400
    else:
        return "", 400