from PyPDF2 import PdfMerger

def merge_pdfs(pdf_list, output_name):
    merger = PdfMerger()
    for pdf in pdf_list:
        merger.append(pdf)
    merger.write(output_name)
    merger.close()

if __name__ == "__main__":
    files = input("Enter PDF filenames separated by comma: ")
    pdf_list = [f.strip() for f in files.split(",")]

    output = input("Output file name (e.g., merged.pdf): ")
    merge_pdfs(pdf_list, output)

    print("PDF merged successfully!")
