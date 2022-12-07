from fpdf import FPDF


class PDF:
    pdf = FPDF(orintation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, ln=1, align='C')
    pdf.output('pdf/Report.pdf')
