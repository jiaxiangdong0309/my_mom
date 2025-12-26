/**
 * 记忆列表组件
 */
import React, { useState, useEffect } from 'react'
import { getAllMemories } from '../api'

function MemoryList({ memories: propMemories, onMemoryClick, onMemoryDelete, refreshTrigger }) {
  const [memories, setMemories] = useState(propMemories || [])
  const [loading, setLoading] = useState(!propMemories)
  const [error, setError] = useState(null)

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

  useEffect(() => {
    const loadMemories = async () => {
      if (propMemories) {
        setMemories(propMemories)
        return
      }

      setLoading(true)
      setError(null)
      try {
        const data = await getAllMemories()
        setMemories(data)
      } catch (err) {
        setError(err.message || '加载失败')
      } finally {
        setLoading(false)
      }
    }

    loadMemories()
  }, [refreshTrigger, propMemories])

  if (loading) {
    return <div className="loading">加载中...</div>
  }

  if (error) {
    return <div className="error">错误: {error}</div>
  }

  if (!memories || memories.length === 0) {
    return (
      <div className="empty-state">
        <p>还没有记忆，创建第一条记忆吧！</p>
      </div>
    )
  }

  return (
    <div className="memory-list">
      {memories.map((memory) => (
        <div
          key={memory.id}
          className="memory-list-item"
          onClick={() => onMemoryClick(memory.id)}
        >
          <div className="memory-list-item-main">
            <div className="memory-list-item-header">
              <h4 className="memory-list-item-title">{memory.title}</h4>
            </div>
            <p className="memory-list-item-content">
              {memory.content.substring(0, 200)}{memory.content.length > 200 ? '...' : ''}
            </p>
            <div className="memory-list-item-footer">
              <div className="memory-list-item-tags">
                {memory.tags && memory.tags.length > 0 ? (
                  memory.tags.map((tag, index) => (
                    <span key={index} className="memory-tag">{tag}</span>
                  ))
                ) : (
                  <span className="memory-tag-empty">无标签</span>
                )}
              </div>
              <div className="memory-list-item-actions">
                <span className="memory-list-item-date">{formatDate(memory.created_at)}</span>
                <button
                  className="memory-list-item-delete"
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
  )
}

export default MemoryList

