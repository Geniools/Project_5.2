from fpdf import FPDF

from src.modules.module import Module


class PDFGenerator(Module):
    def __init__(self, pdfName="report.pdf"):
        super().__init__("PDFGenerator")
        self._pdf = FPDF(orientation='P', unit='mm', format='A4')
        self._pdfName = pdfName
        self._inputReceived = []

    def addContent(self, content):
        try:
            iter(content)
        except TypeError:
            self._inputReceived.append(content)
        else:
            for item in content:
                self.addContent(item)

    def run(self):
        self._pdf.add_page()
        self._pdf.set_font('Arial', 'B', 16)
        self._pdf.cell(200, 10, ln=1, txt=str(" ".join(self._inputReceived)), align='C')
        return self._pdf.output(dest='S').encode('latin-1')

    @property
    def pdfName(self):
        return self._pdfName


if __name__ == '__main__':
    pdfgenerator = PDFGenerator()
    pdfgenerator.run()
