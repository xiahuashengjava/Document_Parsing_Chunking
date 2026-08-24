from paddleocr import PPStructure

engine = PPStructure(show_log=False, lang="ch")

def parse_scanned_pdf(img_path: str):
    result = engine(img_path)        # 先版面分析，再分区 OCR
    blocks = []
    for region in sorted(result, key=lambda r: r["bbox"][1]):  # 按纵坐标排序，保阅读顺序
        rtype = region["type"]       # text / title / table / figure
        if rtype == "table":
            # 表格区域直接输出 HTML，保留结构
            blocks.append({"type": "table", "content": region["res"]["html"]})
        elif rtype in ("text", "title"):
            text = "".join(line["text"] for line in region["res"])
            blocks.append({"type": rtype, "content": text})
    return blocks