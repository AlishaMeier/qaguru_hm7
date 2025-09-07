import os
import zipfile
from io import BytesIO
import pypdf
from openpyxl import load_workbook


def test_create_archive():
    os.makedirs('my_archives', exist_ok=True)

    archive_path = os.path.join('my_archives', 'test_archive.zip')

    files_for_zip = [
        'test_pdf.pdf',
        'test_xlsx.xlsx',
        'test_csv.csv'
    ]

    with zipfile.ZipFile(archive_path, 'w') as zf:
        for file in files_for_zip:
            file_path = os.path.join(os.getcwd(), file)
            if os.path.exists(file_path):
                zf.write(file_path, os.path.basename(file_path))


    with zipfile.ZipFile(archive_path, 'r') as zf:
        assert 'test_pdf.pdf' in zf.namelist()
        assert 'test_xlsx.xlsx' in zf.namelist()
        assert 'test_csv.csv' in zf.namelist()


def test_read_pdf_file():
    archive_path = 'my_archives/test_archive.zip'
    pdf_name = 'test_pdf.pdf'

    with zipfile.ZipFile(archive_path, 'r') as zf:
        with zf.open(pdf_name) as pdf_file:
            pdf_bytes = pdf_file.read()
            pdf_stream = BytesIO(pdf_bytes)
            reader = pypdf.PdfReader(pdf_stream)
            for page in reader.pages:
                content = page.extract_text()
    assert content == ''


def test_read_csv_file():
    archive_path = 'my_archives/test_archive.zip'
    file = 'test_csv.csv'

    with zipfile.ZipFile(archive_path, 'r') as zf:
        with zf.open(file) as csv_file:
            content = csv_file.read().decode('utf-8')
    assert content == '5001\n5002'

def test_read_xlsx_file():
    archive_path = 'my_archives/test_archive.zip'
    xlsx_name = 'test_xlsx.xlsx'

    with zipfile.ZipFile(archive_path, 'r') as zf:
        with zf.open(xlsx_name) as xlsx_file:
            xlsx_bytes = xlsx_file.read()
            xlsx_stream = BytesIO(xlsx_bytes)
            workbook = load_workbook(xlsx_stream, read_only=True)
            sheet = workbook.active
            value = sheet['A1'].value
    assert value == 5001