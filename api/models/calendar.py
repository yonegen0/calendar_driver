from api.external import db
from datetime import datetime

# User モデルの定義
class User(db.Model):
    # テーブル名を設定
    __tablename__ = 'users'
    # テーブルに関する追加情報（コメント）
    __table_args__ = {
        'comment': 'ユーザー情報'
    }
    # ユーザーID
    id = db.Column(db.Integer, primary_key=True)
    # 予定の一覧
    plans = db.relationship('Plan', backref='calendar', cascade="all, delete-orphan", lazy=True, uselist=True, foreign_keys='Plan.user_id')

# Plan モデルの定義
class Plan(db.Model):
    # テーブル名を設定
    __tablename__ = 'plans'
    # テーブルに関する追加情報（コメント）
    __table_args__ = {
        'comment': '予定'
    }
    # 予定ID
    id = db.Column(db.Integer, primary_key=True)
    # ユーザーID
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # 開始日付
    start_date = db.Column(db.String(30), nullable=False)
    # 予定のテキスト
    plan_text = db.Column(db.String(255), nullable=False)