# controllers/calendar_controller.py
from flask import Blueprint, request, current_app, jsonify
from sqlalchemy import and_

import api.external as external
from api.models.calendar import User, Plan

app = Blueprint('calendar_api', __name__)

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
        
        # ユーザーオブジェクトを JSON に変換して返す
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch user data", "details": str(e)}), 500