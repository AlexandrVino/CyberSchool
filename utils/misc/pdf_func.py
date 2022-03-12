from time import sleep

from docxtpl import DocxTemplate
import os
import asyncio


def create_word(data: dict):
    # open template
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'res.docx').replace('\\utils\\misc', '')
    doc = DocxTemplate("static/template/tpl.docx")

    # format data
    data["day"], data["month"], data["year"] = data["release_date"].split("/")
    data["year"] = data["year"][2:]

    # render & save docx file
    doc.render(data)
    doc.save(f"{path}")

    # print file
    os.startfile("res.docx", 'print')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(remove_file(path))

    # call func printing file
    print("print_file")


async def remove_file(path):
    await asyncio.sleep(3)
    # delete docx file
    try:
        os.remove(path)
    except FileNotFoundError:
        return
