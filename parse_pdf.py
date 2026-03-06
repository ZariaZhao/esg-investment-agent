# Import PyMuPDF library
import fitz
import re
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    # Open the PDF file and name it doc
    doc = fitz.open(pdf_path)
    # Create an empty list to store each page
    pages = []
    for page in doc:
        # Extract text from current page
        text = page.get_text()
        # Append page number and text as a dict into pages
        pages.append({"page": page.number, "text": text})
    return pages

def convert_to_markdown(pages):
    # 1. create a new list md_lines = []
    md_lines = []
    # 2. 遍历每一页，再遍历每一行
    for page in pages:
        for line in page["text"].split("\n"):
    # 3. 判断这行是标题还是普通文字，加上对应的 # 符号
            if line.isupper() and len(line) < 60:
                md_lines.append(f"# {line}")
            elif re.match(r"^\d+\.",line):
                md_lines.append(f"## {line}")
            else:
                md_lines.append(line)
    # 4. 返回用 \n 拼接的字符串
    return "\n".join(md_lines)



if __name__ == "__main__":
    pdf_paths = Path("data/raw").glob("*.pdf")
    for pdf_path in pdf_paths:
        # 1. 调用 extract_text_from_pdf(pdf_path)
        result = extract_text_from_pdf(pdf_path)
        # 2. 调用 convert_to_markdown(result)
        markdown = convert_to_markdown(result)
        # 3. 保存到 output/，文件名用 pdf_path.stem + ".md"
        #    （pdf_path.stem 就是文件名去掉后缀，比如 "bhp_ghg_2025"）
        with open(f"output/{pdf_path.stem}.md","w",encoding="utf-8") as f:
            f.write(markdown)
        print(f"Saved {pdf_path.stem}.md")




















