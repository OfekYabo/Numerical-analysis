
import zipfile
import xml.etree.ElementTree as ET
import sys
import os

ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

def docx_to_text(docx_path, output_md_path):
    print(f"Processing {docx_path}...")
    try:
        if not zipfile.is_zipfile(docx_path):
            print("Not a valid zip/docx file")
            return

        with zipfile.ZipFile(docx_path) as z:
            xml_content = z.read('word/document.xml')
        
        tree = ET.fromstring(xml_content)
        
        lines = []
        # Iterate over paragraphs
        for p in tree.iterfind('.//w:p', ns):
            texts = [node.text for node in p.iterfind('.//w:t', ns) if node.text]
            if texts:
                lines.append(''.join(texts))
            else:
                lines.append('') # Empty line for spacing
                
        # Basic cleanup: remove excessive scanning empty lines but keep paragraph structure
        formatted_lines = []
        for line in lines:
            formatted_lines.append(line)
        
        content = '\n'.join(formatted_lines)
        
        # Write to file
        with open(output_md_path, 'w', encoding='utf-8') as f:
            f.write("# Project Description (Extracted)\n\n")
            f.write(content)
            
        print(f"Successfully extracted text to {output_md_path}")
        
    except Exception as e:
        print(f"Error parsing docx: {e}")

if __name__ == "__main__":
    docx_file = r"Ass5\NA_Project.docx"
    output_file = r"docs\NA_Project_Full.md"
    
    if not os.path.exists(docx_file):
        print(f"File not found: {docx_file}")
    else:
        docx_to_text(docx_file, output_file)
