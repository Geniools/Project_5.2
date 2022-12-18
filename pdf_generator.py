#
# class PDF:
#     def __init__(self, path):
#         self._path = path
#         self.pdf_path = os.path.join(os.getcwd(), 'src/modules/PDFGenerator')
#
#     def _pdf(self):
#         subprocess.run(input=(["python", "rsf.py"]), cwd=self.pdf_path)
#
#         pdf = FPDF(orientation='P', unit='mm', format='A4')
#         pdf.add_page()
#         pdf.set_font('Arial', 'B', 16)
#         pdf.cell(200, 10, text='', ln=1, align='C')
#         # var with input from roiutersploit  to text
#         pdf.output('pdf/Report.pdf')
#
#     def run(self):
#         self._pdf()

# add open file, read from result


# pdfgenerator = PDF('src/modules/PDFGenerator')
# pdfgenerator.run()

import os
#
# import os.path
#
# from fpdf import FPDF
#
#
# class PDF:
#     def __init__(self):
#         self._path = os.path
#         self.pdf_path = os.path.join(os.getcwd(), 'src/modules/PDFGenerator')
#         self._inputReceived = []

#     def addContent(self, content):
#         self._inputReceived.append(content)
#
#     def _pdf(self, content):
#         pdf_create = FPDF(orientation='P', unit='mm', format='A4')
#         pdf_create.add_page()
#         pdf_create.set_font('Arial', 'B', 16)
#         pdf_create.cell(200, 10, txt=content, ln=1, align='C')
#         pdf_create.output('pdf/Report.pdf')
#
#     def run(self, content):
#         self._pdf(content)
#
#
# pdfgenerator = PDF()
# pdfgenerator.run()


import os
import os.path
from subprocess import run

from fpdf import FPDF


class PDF:
    def __init__(self):
        self._path = os.path
        self.pdf_path = os.path.join(os.getcwd(), 'src/modules/PDFGenerator')
        self._inputReceived = []

    def addContent(self, content):
        self._inputReceived.append(content)

    def _pdf(self, content):
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(200, 10, ln=1, txt=content, align='C')
        pdf.output('pdf/Report.pdf')

    def run(self, content):
        self._pdf(content)


pdfgenerator = PDF()
pdfgenerator.run()
