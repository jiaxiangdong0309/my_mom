/**
 * 搜索结果组件
 */
import React from 'react'

function SearchResults({ results, onMemoryClick, onMemoryDelete, query, searchMode = 'vector' }) {
  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const handleDelete = (e, id) => {
    e.stopPropagation()
    if (window.confirm('确定要删除这条记忆吗？')) {
      onMemoryDelete(id)
    }
  }

  if (!query) {
    return null
  }

  if (results.length === 0) {
    return (
      <div className="search-results-empty">
        <p>未找到相关记忆</p>
      </div>
    )
  }

  return (
    <div className="search-results">
      <h3>
        搜索结果 ({results.length} 条)
        <span className="search-mode-badge">
          {searchMode === 'vector' ? '🔍 语义搜索' : '📝 文本搜索'}
        </span>
      </h3>
      <div className="search-results-list">
        {results.map((memory) => (
          <div
            key={memory.id}
            className="search-result-item"
            onClick={() => onMemoryClick(memory.id)}
          >
            <div className="search-result-item-main">
              <div className="search-result-item-header">
                <h4 className="search-result-item-title">{memory.title}</h4>
                {memory.relevance !== undefined && (
                  <span className="search-result-item-relevance">
                    {(memory.relevance * 100).toFixed(1)}%
                  </span>
                )}
              </div>
              <p className="search-result-item-content">
                {memory.content.substring(0, 200)}{memory.content.length > 200 ? '...' : ''}
              </p>
              <div className="search-result-item-footer">
                <div className="search-result-item-tags">
                  {memory.tags && memory.tags.length > 0 ? (
                    memory.tags.map((tag, index) => (
                      <span key={index} className="search-result-tag">{tag}</span>
                    ))
                  ) : (
                    <span className="search-result-tag-empty">无标签</span>
                  )}
                </div>
                <div className="search-result-item-actions">
                  <span className="search-result-item-date">{formatDate(memory.created_at)}</span>
                  <button
                    className="search-result-item-delete"
                    onClick={(e) => handleDelete(e, memory.id)}
                    title="删除"
                  >
                    删除
                  </button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default SearchResults

