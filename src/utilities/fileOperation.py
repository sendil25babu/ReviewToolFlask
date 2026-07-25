# create method with file path and content as input to create new docx file
def create_docx_file(file_path, content):
    from docx import Document
    from docx.shared import Pt

    # create a new document
    doc = Document()

    # add content to the document
    for line in content.splitlines():
        paragraph = doc.add_paragraph(line)
        paragraph.style.font.size = Pt(12)

    # save the document
    doc.save(file_path)
