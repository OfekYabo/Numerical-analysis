try:
    import docx
    print("docx installed")
except ImportError:
    print("docx not installed")

try:
    import PyPDF2
    print("PyPDF2 installed")
except ImportError:
    print("PyPDF2 not installed")

try:
    import pdfminer
    print("pdfminer installed")
except ImportError:
    print("pdfminer not installed")
