# 解析出文本，不等于干净文本。文本里往往还混着一堆你没注意到的噪音，它们不会让程序报错，只会悄悄拉低召回质量。
# 三类最高频的：
# 一是页眉页脚、水印、页码。这些东西每一页都重复出现。你把整本手册切块入库，"XX 公司版权所有 第 12 页"这种字符串会反复混进正文块里。
# embedding 一算，这些高频噪音稀释了真正的语义。
# 二是多栏错位。双栏排版的论文、手册，如果解析工具没处理好阅读顺序，出来就是左右两栏横着串行——读起来每一句都断头断尾。
# 三是软换行和断字。PDF 里一句完整的话，因为排版被物理换行拆成了好几行，\n 就这么混进了句子中间。
# 切块和 embedding 都会被这些假换行干扰。


import re
from collections import Counter


def clean_text(pages: list[str]) -> str:
    # 1. 检测并去掉页眉页脚：出现在 >80% 页面的短行
    line_freq = Counter()
    for page in pages:
        for line in page.splitlines():
            line = line.strip()
            if 0 < len(line) < 40:         # 只看短行，正文长句不算
                line_freq[line] += 1
    threshold = len(pages) * 0.8
    headers_footers = {ln for ln, c in line_freq.items() if c >= threshold}

    cleaned_pages = []
    for page in pages:
        lines = [ln for ln in page.splitlines()
                 if ln.strip() not in headers_footers]
        cleaned_pages.append("\n".join(lines))

    text = "\n".join(cleaned_pages)

    # 2. 合并软换行：句子中间的换行去掉，段落间的保留
    #    规则：如果换行前不是句末标点，判定为软换行
    text = re.sub(r"(?<![。！？.!?：；\n])\n(?!\n)", "", text)

    # 3. 去多余空白和控制符
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# ============ 构造输入：pages 是字符串列表，每一个元素代表PDF的一页 ============
if __name__ == "__main__":
    sample_pages = [
        # 第1页
        """文档示例｜第 1 页
人工智能是当下非常热门
的技术方向。它深刻
影响
各行各业的发展。

这是第一段正文内容。
这是第二段正文内容。
""",
        # 第2页
        """文档示例｜第 2 页
机器学习属于人工智能
的一个重要分支，拥有
广阔的应用前景。

第三段正文内容。
第四段正文内容。
""",
        # 第3页
        """文档示例｜第 3 页
深度学习是机器学习下
的子领域，最近
几年发
展速度飞快啊。

第五段正文内容。
第六段正文内容。
"""
    ]

    result = clean_text(sample_pages)
    print("=====清洗后的结果=====")
    print(result)



# 但清洗要适度。这是个反直觉的点：过度清洗会把有意义的换行——列表项、代码缩进、表格分行——也一起抹平。所以清洗规则要跟着文档类型走：散文类可以放心合并软换行；代码文档、结构化手册，就得手下留情。
# 噪音的危害很隐蔽：它不改变召回分数的量级，但会系统性地拉低 top-k 的信噪比。你召回了对的块，可块里 30% 是页脚和乱序，喂给 LLM 就等于凭空多了 30% 的干扰。模型不是变笨了，是你给它的卷子上印了别的题。








