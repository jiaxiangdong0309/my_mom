"""
文本分段工具
"""
from typing import List

def split_text_by_chars(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """
    按字符数分段文本

    Args:
        text: 输入文本
        chunk_size: 每段最大字符数（默认1000）
        overlap: 重叠字符数，避免在句子中间切断（默认100）

    Returns:
        分段后的文本列表
    """
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # 如果不是最后一段，尝试在合适的位置切断
        if end < len(text):
            # 尝试在换行符处切断
            newline_pos = text.rfind('\n', start, end)
            if newline_pos != -1 and newline_pos > start + chunk_size // 2:
                end = newline_pos + 1
            # 如果没有换行符，尝试在句号处切断
            elif overlap > 0:
                period_pos = text.rfind('。', start, end)
                if period_pos != -1 and period_pos > start + chunk_size // 2:
                    end = period_pos + 1

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        # 下一段的起始位置，考虑重叠
        start = end - overlap if overlap > 0 and end < len(text) else end

    return chunks

