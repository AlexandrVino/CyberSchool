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

    def get_certificate_for_pdf(self, index_number: int, certificate_number: str) -> list:
        """
        :param index_number порядковй номер сертификата
        :param certificate_number порядковй номер сертификата
        :return: сертификат
        """

        cur = self.con.cursor()

        try:
            cur.execute(f"SELECT all FROM certificates WHERE index_number ={index_number} "
                        f"AND certificate_number ='{certificate_number}'")
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
        list_of_value = dict_of_value.values()
        cur = self.con.cursor()

        try:
            cur.execute(f"INSERT OR IGNORE INTO certificates(index_number, number_certificate, "
                        f"product_name, product_number, product_type, order_number, "
                        f"consumer_organization, shop_manufacturer, release_date, "
                        f"full_name_of_the_certificate_issuer, kit, draft_number, release_date, technical_conditions"
                        f") "
                        f"VALUES({list_of_value[0]}, {list_of_value[1]}, {list_of_value[3]}, {list_of_value[4]},"
                        f" {list_of_value[5]}, {list_of_value[6]}, {list_of_value[7]}, {list_of_value[8]},"
                        f" {list_of_value[9]}, {list_of_value[10]}, {list_of_value[11]}, "
                        f" {list_of_value[12]}, {list_of_value[13]}, {list_of_value[13]};")
        finally:
            self.con.commit()
            cur.close()
            return 1

