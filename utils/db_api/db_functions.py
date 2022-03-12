import sqlite3

class ErrorCertificate(Exception):
    pass


class DataBase:
    """
    Класс для работы с базой данных
    """

    def __init__(self, database_name: str):
        self.db_name = database_name
        self.con = sqlite3.connect(self.db_name)

    def get_certificate_for_pdf(self, index_number: int) -> list:
        """
        :param index_number порядковй номер сертификата
        :return: сертификат
        """

        cur = self.con.cursor()

        try:
            cur.execute(f"SELECT all FROM certificates WHERE serial_number ='{index_number}'")
            return list(cur.fetchall())
        finally:
            cur.close()

    def get_certificates(self) -> list:
        """
        :return: сертификаты
        """

        cur = self.con.cursor()

        try:
            cur.execute(f"SELECT all FROM certificates")
            return list(cur.fetchall())
        finally:
            cur.close()

    def is_certificate_presents(self, index_number: int) -> bool:
        """
        :param index_number порядковй номер сертификата
        :return: str
        """

        # я бы возвращал bool))

        cur = self.con.cursor()

        try:
            cur.execute(f"INSERT OR IGNORE INTO certificates(index_number) "
                        f"VALUES({index_number});")
        except ErrorCertificate:
            return 1
        finally:
            self.con.commit()
            cur.close()
            return 0

    def add_certificate(self, dict_of_value: dict) -> bool:
        """
        :param dict_of_value данные сертификата
        :return: None
        добавляет сертификат в бд
        """
        cur = self.con.cursor()

        try:
            cur.execute(f"INSERT OR IGNORE INTO certificates() "
                        f"VALUES();")
        finally:
            self.con.commit()
            cur.close()
            return 1
