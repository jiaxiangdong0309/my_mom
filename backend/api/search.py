"""
搜索接口路由
"""
import sys
import logging
from fastapi import APIRouter
from .models import SearchRequest, SearchResult
from ..core.chroma_db import ChromaDB
from ..core.sqlite_db import SQLiteDB
from ..core.embedding import Embedding

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/search", tags=["search"])

# 禁用自动重定向，统一路径行为
router.redirect_slashes = False

# 直接实例化（后续可改为依赖注入）
chroma_db = ChromaDB()
sqlite_db = SQLiteDB()
embedder = Embedding()

@router.post("/", response_model=list[SearchResult])
async def search(data: SearchRequest):
    """语义搜索"""
    # 1. 查询向量化
    query_embedding = embedder.encode(data.query)

    # 2. 向量检索（ChromaDB 返回 ID 和 distance）
    # 返回的ID格式是 "memory_id:chunk_index"
    # 先获取top 10条数据用于间隔分析
    vector_results = chroma_db.search(query_embedding, top_k=10)

    if not vector_results:
        return []

    # 3. 解析ID，提取memory_id，并去重（同一记忆的多个块只保留相关性最高的）
    memory_id_to_best_result = {}
    for vec_result in vector_results:
        chunk_id = vec_result["id"]
        metadata = vec_result.get("metadata", {})

        # 从metadata中获取memory_id，如果没有则从ID中解析
        if "memory_id" in metadata:
            memory_id = metadata["memory_id"]
        else:
            # 兼容旧格式：如果ID是纯数字
            try:
                memory_id = int(chunk_id)
            except ValueError:
                # 新格式：memory_id:chunk_index
                memory_id = int(chunk_id.split(":")[0])

        distance = vec_result.get("distance", 1.0)

        # 如果这个memory_id还没有记录，或者这个块的相关性更高，则更新
        if memory_id not in memory_id_to_best_result:
            memory_id_to_best_result[memory_id] = {
                "memory_id": memory_id,
                "distance": distance
            }
        else:
            # 保留距离更小的（相关性更高）
            if distance < memory_id_to_best_result[memory_id]["distance"]:
                memory_id_to_best_result[memory_id]["distance"] = distance

    # 4. 从 SQLite 批量获取完整数据
    memory_ids = list(memory_id_to_best_result.keys())
    deduplicated_ids = sorted(memory_ids)
    memories = sqlite_db.get_memories_by_ids(memory_ids)
    found_ids = sorted([mem["id"] for mem in memories])

    # 警告：如果SQLite中找不到某些id
    if len(found_ids) < len(deduplicated_ids):
        missing_ids = sorted(set(deduplicated_ids) - set(found_ids))
        log_msg = f"[语义搜索] 警告: 以下id在SQLite中未找到: {missing_ids}"
        print(log_msg, flush=True)
        logger.warning(log_msg)

    # 创建 ID 到记忆的映射
    memory_dict = {mem["id"]: mem for mem in memories}

    # 5. 合并结果（将 distance 转换为相似度）
    # ChromaDB cosine 距离：0 表示完全相同，2 表示完全相反
    # 相似度 = 1 - (distance / 2)，归一化到 [0, 1]
    results = []
    for memory_id, best_result in memory_id_to_best_result.items():
        if memory_id in memory_dict:
            memory = memory_dict[memory_id]
            distance = best_result["distance"]
            relevance = max(0.0, 1.0 - (distance / 2.0))  # 归一化到 [0, 1]

            results.append(SearchResult(
                id=memory["id"],
                title=memory["title"],
                content=memory["content"],
                tags=memory["tags"],
                created_at=memory["created_at"],
                relevance=relevance
            ))

    # 6. 按相关性排序（从高到低）
    results.sort(key=lambda x: x.relevance, reverse=True)

    # 辅助函数：格式化结果输出
    def format_result_list(result_list, prefix="  "):
        """格式化结果列表，显示id、title和relevance"""
        if not result_list:
            return ""
        lines = []
        for i, r in enumerate(result_list, 1):
            title_short = r.title[:30] + "..." if len(r.title) > 30 else r.title
            lines.append(f"{prefix}{i}. [ID:{r.id}] {title_short} (relevance: {r.relevance:.4f})")
        return "\n".join(lines)

    print(f"\n{'='*80}", flush=True)
    print(f"[语义搜索] 查询: '{data.query}'", flush=True)
    print(f"[初始结果] 排序后共 {len(results)} 条", flush=True)
    if results:
        print(format_result_list(results), flush=True)

    # 7. 阈值过滤：先过滤明显不相关的结果
    RELEVANCE_THRESHOLD = 0.7
    before_threshold_filter = len(results)
    # 保存被过滤掉的数据用于日志
    filtered_out_results = [r for r in results if r.relevance < RELEVANCE_THRESHOLD]
    results = [r for r in results if r.relevance >= RELEVANCE_THRESHOLD]
    after_threshold_filter = len(results)

    if before_threshold_filter != after_threshold_filter:
        print(f"\n[阈值过滤] {before_threshold_filter} -> {after_threshold_filter} 条 (阈值: {RELEVANCE_THRESHOLD})", flush=True)
        if filtered_out_results:
            print(f"[阈值过滤] 过滤掉的数据:", flush=True)
            print(format_result_list(filtered_out_results), flush=True)
    else:
        print(f"[阈值过滤] {before_threshold_filter} 条 (全部通过阈值 {RELEVANCE_THRESHOLD})", flush=True)

    # 8. 智能分割：基于relevance间隔分析（找到相关性明显下降的临界点）
    if len(results) > 1:
        # 提取relevance值列表
        relevance_values = [r.relevance for r in results]

        # 计算相邻relevance的间隔
        gaps = []
        for i in range(len(relevance_values) - 1):
            gap = relevance_values[i] - relevance_values[i + 1]
            gaps.append(gap)

        if gaps:
            # 找到最大间隔的位置
            max_gap_index = gaps.index(max(gaps))
            max_gap_value = gaps[max_gap_index]

            # 计算所有间隔的平均值（包括最大间隔）
            avg_gap_value = sum(gaps) / len(gaps)
            GAP_THRESHOLD_OFFSET = 0.02  # 间隔阈值偏移量
            gap_threshold = avg_gap_value + GAP_THRESHOLD_OFFSET

            # 打印间隔分析详情
            print(f"\n[间隔分析] 计算相邻relevance间隔:", flush=True)
            for i, gap in enumerate(gaps):
                marker = " ← 最大间隔" if i == max_gap_index else ""
                title1 = results[i].title[:20] + "..." if len(results[i].title) > 20 else results[i].title
                title2 = results[i+1].title[:20] + "..." if len(results[i+1].title) > 20 else results[i+1].title
                print(f"  间隔 {i+1}: [{results[i].id}] {title1} ({relevance_values[i]:.4f}) -> "
                      f"[{results[i+1].id}] {title2} ({relevance_values[i+1]:.4f}) = {gap:.4f}{marker}", flush=True)

            print(f"\n[间隔分析] 最大间隔位置: {max_gap_index} (在索引 {max_gap_index} 和 {max_gap_index+1} 之间)", flush=True)
            print(f"[间隔分析] 最大间隔值: {max_gap_value:.4f}", flush=True)
            print(f"[间隔分析] 平均间隔值: {avg_gap_value:.4f}", flush=True)
            print(f"[间隔分析] 分割阈值: {gap_threshold:.4f} (平均间隔 {avg_gap_value:.4f} + {GAP_THRESHOLD_OFFSET})", flush=True)

            # 计算除了最大间隔之外的其他间隔的平均值（用于参考）
            other_gaps = [gap for i, gap in enumerate(gaps) if i != max_gap_index]
            if other_gaps:
                avg_other_gaps = sum(other_gaps) / len(other_gaps)
                print(f"[间隔分析] 其他间隔平均值: {avg_other_gaps:.4f} (共 {len(other_gaps)} 个间隔)", flush=True)
            else:
                print(f"[间隔分析] 其他间隔平均值: 无 (只有1个间隔)", flush=True)

            # 只有当最大间隔 > 平均间隔值 + 0.02 时才进行分割
            if max_gap_value > gap_threshold:
                split_position = max_gap_index + 1  # 分割位置（保留前split_position个）

                # 分割：只保留第一组（relevance更高的部分）
                filtered_results = results[:split_position]

                print(f"[间隔分析] 最大间隔 {max_gap_value:.4f} > 阈值 {gap_threshold:.4f}，执行分割", flush=True)
                print(f"[间隔分析] 分割结果: {len(results)} -> {len(filtered_results)} 条", flush=True)
                print(f"[间隔分析] 保留的数据:", flush=True)
                print(format_result_list(filtered_results), flush=True)
                if len(results) > split_position:
                    discarded = results[split_position:]
                    print(f"[间隔分析] 舍弃的数据:", flush=True)
                    print(format_result_list(discarded), flush=True)

                results = filtered_results
            else:
                print(f"[间隔分析] 最大间隔 {max_gap_value:.4f} <= 阈值 {gap_threshold:.4f}，不执行分割，保留全部 {len(results)} 条", flush=True)
        else:
            print(f"[间隔分析] {len(results)} 条 (无间隔，全部保留)", flush=True)
    elif len(results) == 1:
        print(f"[间隔分析] 1 条 (跳过间隔分析)", flush=True)
    elif len(results) == 0:
        print(f"[间隔分析] 0 条", flush=True)

    print(f"\n[最终结果] 返回 {len(results)} 条", flush=True)
    if results:
        print(format_result_list(results), flush=True)
    print(f"{'='*80}\n", flush=True)

    # 9. 限制返回数量（如果用户请求的数量小于过滤后的结果）
    return results[:data.limit]

@router.post("/sqlite", response_model=list[SearchResult])
async def search_sqlite(data: SearchRequest):
    """关键字搜索 (SQLite)"""
    print(f"\n{'='*80}", flush=True)
    print(f"[SQLite搜索] 查询关键字: '{data.query}'", flush=True)
    print(f"[SQLite搜索] 限制返回数量: {data.limit}", flush=True)

    memories = sqlite_db.search_memories(data.query)

    print(f"[SQLite搜索] 数据库返回 {len(memories)} 条记录", flush=True)

    results = []
    for memory in memories:
        results.append(SearchResult(
            id=memory["id"],
            title=memory["title"],
            content=memory["content"],
            tags=memory["tags"],
            created_at=memory["created_at"],
            relevance=1.0  # 关键字匹配默认相关度为 1.0
        ))

    # 格式化结果输出
    def format_result_list(result_list, prefix="  "):
        """格式化结果列表，显示id、title和tags"""
        if not result_list:
            return ""
        lines = []
        for i, r in enumerate(result_list, 1):
            title_short = r.title[:30] + "..." if len(r.title) > 30 else r.title
            tags_str = ", ".join(r.tags[:3]) if r.tags else "无标签"
            if r.tags and len(r.tags) > 3:
                tags_str += f" (+{len(r.tags)-3}个)"
            lines.append(f"{prefix}{i}. [ID:{r.id}] {title_short} (标签: {tags_str})")
        return "\n".join(lines)

    print(f"[SQLite搜索] 处理后的结果: {len(results)} 条", flush=True)
    if results:
        print(format_result_list(results), flush=True)

    final_results = results[:data.limit]
    print(f"[SQLite搜索] 最终返回: {len(final_results)} 条 (限制: {data.limit})", flush=True)
    print(f"{'='*80}\n", flush=True)

    return final_results

