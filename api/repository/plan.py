from flask import current_app, jsonify
from abc import abstractmethod
import api.external as external
from api.models.calendar import User, Plan

# Plan クラス
class PlanRepository():

    @abstractmethod
    def get_user(self):
        """
        ユーザーに関連付けられた全ての予定を取得する。

        Returns:
            dict: ユーザーの予定を格納した辞書。
        """

    @abstractmethod
    def setplan(self, data):
        """
        新しい予定を作成する。

        Args:
            data (list): リクエストデータ（予定情報のリスト）。

        Returns:
            tuple: 成功した場合は ("", 200)、失敗した場合はエラーメッセージとステータスコード。
        """

    @abstractmethod
    def getplan(self, data):
        """
        指定された ID の予定を取得する。

        Args:
            data (list): リクエストデータ（ID を含む）。

        Returns:
            tuple: 成功した場合は JSON 形式の予定データと 200、
                   指定された ID の予定が見つからなかった場合は 404、
                   ID が指定されていない場合は 400。
        """

    @abstractmethod
    def editplan(self, data):
        """
        指定された ID の予定を更新する。

        Args:
            data (list): リクエストデータ（ID、日付、テキストを含む）。

        Returns:
            tuple: 成功した場合は ("", 200)、
                   指定された ID の予定が見つからなかった場合は 404、
                   ID が指定されていない場合は 400、
                   日付またはテキストが空の場合は 400。
        """

    @abstractmethod
    def deleteplan(self, data):
        """
        指定された ID の予定を削除する。

        リクエストデータから ID 値を取得し、指定された ID の予定を削除する。

        Args:
            data (list): リクエストデータ（ID を含む）。

        Returns:
            tuple: 成功した場合は ("", 200)、
                   指定された ID の予定が見つからなかった場合は 404、
                   ID が指定されていない場合は 400。
        """

class PlanRepositoryImpl(PlanRepository):

    def _get_first_user(self):
        try:
            user = external.db.session.query(User).first()
            if user is None:
                user = User()
                with current_app.app_context():
                    external.db.session.add(user)
                    external.db.session.commit()
            return user
        except Exception as e:
            print(f"Error in _get_first_user: {e}")  # エラーログ
            raise  # 上位の呼び出し元に例外を再送出

    def _get_plan_by_id(self, plan_id):
        try:
            return external.db.session.query(Plan).filter(Plan.id == plan_id).first()
        except Exception as e:
            print(f"Error in _get_plan_by_id: {e}")
            raise

    # override
    def get_user(self):
        try:
            user = self._get_first_user()
            plans = external.db.session.query(Plan)\
                .filter(Plan.user_id == user.id)
            plans_json = {}
            for plan in plans:
                plans_json[plan.id] = {
                    'start_date': plan.start_date,
                    'plan_text': plan.plan_text
                }
            return jsonify(plans_json), 200
        except Exception as e:
            print(f"Error in get_user: {e}")
            return "", 500 

    # override
    def setplan(self, data):
        try:
            user = self._get_first_user()
            for item in data:
                date = item['date']
                text = item['text']
                if date == '' or text == '':
                    return "値が入っていません", 400
                plan = Plan(
                    user_id=user.id,
                    start_date=date,
                    plan_text=text,
                )
                user.plans.append(plan)
            external.db.session.commit()
            return "", 200
        except Exception as e:
            print(f"Error in setplan: {e}")
            return "", 500

    # override
    def getplan(self, data):
        try:
            for item in data:
                id_value = item.get('id')
            if id_value is not None:
                plan_id = int(id_value)
                plan = self._get_plan_by_id(plan_id)
                if plan:
                    plan_json = {
                        'start_date': plan.start_date,
                        'plan_text': plan.plan_text
                    }
                    return jsonify(plan_json), 200
                else:
                    return "指定されたIDの予定は見つかりませんでした", 404
            return "IDが指定されていません", 400
        except Exception as e:
            print(f"Error in getplan: {e}")
            return "", 500

    # override
    def editplan(self, data):
        try:
            for item in data:
                id_value = item.get('id')
                date = item['date']
                text = item['text']
                if date == '' or text == '':
                    return "値が入っていません", 400
                if id_value is not None:
                    plan_id = int(id_value)
                    plan = self._get_plan_by_id(plan_id)
                    if plan:
                        plan.start_date = date
                        plan.plan_text = text
                        external.db.session.commit()
                        return "", 200
                    else:
                        return "指定されたIDの予定は見つかりませんでした", 404
                return "IDが指定されていません", 400
        except Exception as e:
            print(f"Error in editplan: {e}")
            return "", 500

    # override
    def deleteplan(self, data):
        try:
            for item in data:
                id_value = item.get('id')
            if id_value is not None:
                plan_id = int(id_value)
                plan = self._get_plan_by_id(plan_id)
                if plan:
                    external.db.session.query(Plan).filter(Plan.id == plan_id).delete()
                    external.db.session.commit()
                    return "", 200
                else:
                    return "指定されたIDの予定は見つかりませんでした", 404
            return "IDが指定されていません", 400
        except Exception as e:
            print(f"Error in deleteplan: {e}")
            return "", 500