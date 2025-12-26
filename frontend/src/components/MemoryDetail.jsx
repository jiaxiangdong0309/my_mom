/**
 * 记忆详情组件
 */
import React, { useState, useEffect } from 'react'
import { getMemory } from '../api'

function MemoryDetail({ memoryId, onBack, onDelete }) {
  const [memory, setMemory] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const loadMemory = async () => {
      setLoading(true)
      setError(null)
      try {
        const data = await getMemory(memoryId)
        setMemory(data)
      } catch (err) {
        setError(err.message || '加载失败')
      } finally {
        setLoading(false)
      }
    }

    if (memoryId) {
      loadMemory()
    }
  }, [memoryId])

  const handleDelete = () => {
    if (window.confirm('确定要删除这条记忆吗？')) {
      onDelete(memory.id)
    }
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  if (loading) {
    return (
      <div className="memory-detail">
        <div className="loading">加载中...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="memory-detail">
        <div className="error">错误: {error}</div>
        <button onClick={onBack}>返回</button>
      </div>
    )
  }

  if (!memory) {
    return (
      <div className="memory-detail">
        <div className="error">记忆不存在</div>
        <button onClick={onBack}>返回</button>
      </div>
    )
  }

  return (
    <div className="memory-detail">
      <div className="memory-detail-header">
        <button onClick={onBack} className="back-button">← 返回</button>
        <button onClick={handleDelete} className="delete-button">删除</button>
      </div>

      <div className="memory-detail-content">
        <h1>{memory.title}</h1>

        <div className="memory-detail-meta">
          <div className="memory-detail-tags">
            {memory.tags && memory.tags.length > 0 ? (
              memory.tags.map((tag, index) => (
                <span key={index} className="memory-tag">{tag}</span>
              ))
            ) : (
              <span className="memory-tag-empty">无标签</span>
            )}
          </div>
          <span className="memory-detail-date">{formatDate(memory.created_at)}</span>
        </div>

        <div className="memory-detail-body">
          <p>{memory.content}</p>
        </div>
      </div>
    </div>
  )
}

export default MemoryDetail

