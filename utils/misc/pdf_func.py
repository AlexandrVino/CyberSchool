from docxtpl import DocxTemplate
import os


def create_word(data: dict):
    # open template
    doc = DocxTemplate("static/template/tpl.docx")

    # format data
    data["day"], data["month"], data["year"] = data["release_date"].split(".")
    data["year"] = data["year"][2:]

    # render & save docx file
    doc.render(data)
    doc.save("res.docx")

    # print file
    os.startfile("res.docx", 'print')

    # call func printing file
    print("print_file")

    # delete docx file
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'res.docx')
    os.remove(path)

