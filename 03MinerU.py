from unstructured.partition.pdf import partition_pdf

elements = partition_pdf(
    filename="无表格电子版PDF.pdf",
    strategy="hi_res",              # 高精度模式，带版面分析
    infer_table_structure=True,     # 表格还原成 HTML
)

blocks = []
for el in elements:
    category = el.category          # Title / NarrativeText / Table / ListItem
    if category == "Table":
        # 表格取 HTML 而不是纯文本
        html = el.metadata.text_as_html
        blocks.append({"type": "table", "content": html})
    else:
        blocks.append({"type": category, "content": el.text})




# MinerU 是另一个近来很能打的开源项目，专门把 PDF 转成结构良好的 Markdown，表格和公式的还原能力尤其强。
# 文档偏学术、公式多的场景，可以优先试它。

# 重灾区专章：表格为什么必须被特殊对待
# 前面三种武器我都反复强调了表格。这里说透为什么。
# 表格是二维结构——行和列的交叉才有意义。而纯文本是一维的。你要是简单地把单元格 join 成一串，行列对应关系当场丢失。回到开头那张退货政策表：X3 那一行的"7"，一旦脱离了"X3"这个行标签，就变成了一个悬空的数字，模型根本不知道它属于谁。
# 正确做法只有一个思路：把表格转成 Markdown 或 HTML，保留行列结构。这样 LLM 读到 | X3 | 7天 | ￥1299 | 这一行，才能理解"7 天对应的是 X3"。
# 还有一条铁律：一个块 = 一张完整表格 + 它的标题，绝不切开。这一点我们放到切块那部分再细讲，但你现在就要记住——表格是切块阶段的高压线。













