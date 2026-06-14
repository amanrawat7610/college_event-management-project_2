from  pypdf import  PdfWriter
merger = PdfWriter()

pdfs = ["gitmore.pdf","new resume..pdf"]
for pdf in pdfs:
    merger.append(pdf)
merger.write("merged.pdf")