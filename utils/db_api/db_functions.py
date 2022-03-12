import sqlite3

class ErrorCertificate(Exception):
    pass


#give all columns value
class DataBase():
    def __init__(self):
        self.db_name = "../../static/database/db.db"

    def get_certificate_for_pdf(self, index_number):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()

        try:
            cur.execute(f"SELECT all FROM certificates WHERE serial_number ='{index_number}'")
            return cur.fetchall()
        finally:
            cur.close()
            con.close()

    def is_certificate_presents(self, index_number):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        message = "Успешно"

        try:
            cur.execute(f"INSERT OR IGNORE INTO certificates(index_number) "
                        f"VALUES({index_number});")
        except ErrorCertificate:
            message = "Сертификат с таким номером уже существует, проверьте номер п/п"
        finally:
            con.commit()
            cur.close()
            return message

    #unpack dict and add certificate to the database
    #тут пока заглушка
    def add_certificate(self, dict_of_value):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        message = "Сертификат добавлен успешно"

        try:
            cur.execute(f"INSERT OR IGNORE INTO certificates() "
                        f"VALUES();")
        finally:
            con.commit()
            cur.close()
            return message
