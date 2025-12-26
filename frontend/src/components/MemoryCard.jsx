/**
 * 记忆卡片组件
 */
import React from 'react'

function MemoryCard({ memory, onClick, onDelete }) {
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

  const handleDelete = (e) => {
    e.stopPropagation()
    if (window.confirm('确定要删除这条记忆吗？')) {
      onDelete(memory.id)
    }
  }

  return (
    <div className="memory-card" onClick={() => onClick && onClick(memory.id)}>
      <div className="memory-card-header">
        <h3 className="memory-card-title">{memory.title}</h3>
        <button className="memory-card-delete" onClick={handleDelete} title="删除">
          ×
        </button>
      </div>
      <p className="memory-card-content">{memory.content.substring(0, 150)}{memory.content.length > 150 ? '...' : ''}</p>
      <div className="memory-card-footer">
        <div className="memory-card-tags">
          {memory.tags && memory.tags.length > 0 ? (
            memory.tags.map((tag, index) => (
              <span key={index} className="memory-tag">{tag}</span>
            ))
          ) : (
            <span className="memory-tag-empty">无标签</span>
          )}
        </div>
        <span className="memory-card-date">{formatDate(memory.created_at)}</span>
      </div>
      {memory.relevance !== undefined && (
        <div className="memory-card-relevance">
          相似度: {(memory.relevance * 100).toFixed(1)}%
        </div>
      )}
    </div>
  )
}

export default MemoryCard

