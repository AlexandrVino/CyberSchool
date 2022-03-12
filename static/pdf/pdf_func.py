from docxtpl import DocxTemplate
import os


def create_word(data):
    # open template
    doc = DocxTemplate("tpl.docx")

    # format data
    data["day"], data["month"], data["year"] = data["release_date"].split(".")
    data["year"] = data["year"][2:]

    # render & save docx file
    doc.render(data)
    doc.save("res.docx")

    # call func printing file
    print("print_file")

    # delete docx file
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'res.docx')
    os.remove(path)


if __name__ == '__main__':
    data = {

        "serial_number": "002",
        "number_certificate": "01-2234",
        "product_name": "ложка",
        "product_number": "14",
        "product_type": "столовый прибор",
        "order_number": "22",
        "consumer_organization": "столовая",
        "shop_manufacturer": "нытвенский музей ложки",
        "full_name_of_the_certificate_issuer": "Попов Алексей Павлович",
        "kit": "5 ложек и вилка",
        "draft_number": "3",
        "release_date": "22.01.2005",
        "technical_conditions": "12АБ"

    }

    create_word(data)
