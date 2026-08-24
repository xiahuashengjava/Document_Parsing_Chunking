import fitz  # PyMuPDF
import pdfplumber
from typing import List, Dict, Any


def parse_pdf(path: str) -> List[Dict[str, Any]]:
    blocks = []

    # 1. 用 PyMuPDF 按页取正文（快）
    doc = fitz.open(path)
    for page_no, page in enumerate(doc):
        text = page.get_text("text")  # 保留基本阅读顺序
        blocks.append({"type": "text", "page": page_no, "content": text})
    doc.close()

    # 2. 用 pdfplumber 单独抽表格（保结构）
    with pdfplumber.open(path) as pdf:
        for page_no, page in enumerate(pdf.pages):
            table = page.extract_table()
            if table:
                md = table_to_markdown(table)
                blocks.append({"type": "table", "page": page_no, "content": md})

    return blocks


def table_to_markdown(table: List[List[Any]]) -> str:
    """把二维表格转成 Markdown，保留行列对应关系"""
    if not table or not table[0]:
        return ""
    header = table[0]
    md = "| " + " | ".join(str(c or "") for c in header) + " |\n"
    md += "| " + " | ".join(["---"] * len(header)) + " |\n"
    for row in table[1:]:
        md += "| " + " | ".join(str(c or "") for c in row) + " |\n"
    return md


def main():
    # ========= 修改这里成你的PDF文件路径 =========
    pdf_file_path = "有表格电子版PDF.pdf"
    #pdf_file_path = "有表格电子版PDF.pdf"

    try:
        result_blocks = parse_pdf(pdf_file_path)
        print(f"解析完成，一共得到 {len(result_blocks)} 个块\n")

        # 打印解析结果
        for idx, block in enumerate(result_blocks):
            print(f"===== 块{idx+1} | 页码:{block['page']} | 类型:{block['type']} =====")
            print(block["content"])
            print("\n")

    except FileNotFoundError:
        print(f"错误：找不到文件 {pdf_file_path}")
    except Exception as e:
        print(f"解析PDF出错: {str(e)}")


if __name__ == "__main__":
    main()

