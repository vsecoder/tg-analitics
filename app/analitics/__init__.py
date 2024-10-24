from app.analitics.report import get_report


class Analitics:
    def __init__(self, db):
        self.db = db

    def get_report(self):
        """
        Get report

        :return:

        """

        get_report(self.db["chats"]["list"])
