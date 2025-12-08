from PyPDF2 import PdfMerger

merger = PdfMerger()

pdffiles = ['Texas_Well_Points.pdf','TWD_Majors.pdf']

for pdf in pdffiles:
    merger.append(pdf)

merger.write("merged_output.pdf")
merger.close()

print("PDF files merged successfully into 'merged_output.pdf'")