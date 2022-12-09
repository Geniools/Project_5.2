# class PDF:
#
#         def _pdf(self):
#             with open("python", "rsf.py") as f:
#                 data = f.read()
#             run(['tar', 'xzf', '-'], input=data)
#
#             pdf = FPDF(orientation='P', unit='mm', format='A4')
#             pdf.add_page()
#             pdf.set_font('Arial', 'B', 16)
#             pdf.cell(200, 10, text="data", ln=1, align='C')
#             pdf.output('pdf/Report.pdf')
#
import os
import subprocess
import os.path
from subprocess import run

from fpdf import FPDF


class PDF:
    def __init__(self, path):
        self._path = path
        self.pdf_path = os.path.join(os.getcwd(), 'src/modules/PDFGenerator')

    def _pdf(self):
        subprocess.run(input=(["python", "rsf.py"]), cwd=self.pdf_path)

        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(200, 10, text='', ln=1, align='C')
        pdf.output('pdf/Report.pdf')

    def run(self):
        self._pdf()

# add open file, read from result ?


# pdfgenerator = PDF('src/modules/PDFGenerator')
# pdfgenerator.run()
