import sqlite3

class ErrorCertificate(Exception):
    pass


#give all columns value
def get_certificate_for_pdf(self, serial_number):
    con = sqlite3.connect("../../static/database/db.db")
    cur = con.cursor()

    try:
        cur.execute(f"SELECT all FROM certificates WHERE serial_number ='{serial_number}'")
        return cur.fetchall()
    finally:
        cur.close()
        con.close()


def is_certificate_presents(self, serial_number):
    con = sqlite3.connect("../../static/database/db.db")
    cur = con.cursor()
    message = "Успешно"

    try:
        cur.execute(f"INSERT OR IGNORE INTO certificates(serial_number) "
                    f"VALUES({serial_number});")
    except ErrorCertificate:
        message = "Сертификат с таким номером уже существует, проверьте номер п/п"
    finally:
        con.commit()
        cur.close()
        return message


#unpack dict and add certificate to the database
def add_certificate(self, dict_of_value):
    con = sqlite3.connect("../../static/database/db.db")
    cur = con.cursor()
    message = "Сертификат добавлен успешно"

    try:
        cur.execute(f"INSERT OR IGNORE INTO certificates() "
                    f"VALUES();")
    finally:
        con.commit()
        cur.close()
        return message
