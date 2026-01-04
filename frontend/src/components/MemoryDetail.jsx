/**
 * 记忆详情组件
 */
import React, { useState, useEffect } from 'react'
import { getMemory } from '../api'
import MemoryForm from './MemoryForm'

function MemoryDetail({ memoryId, onBack, onDelete, onUpdate }) {
  const [memory, setMemory] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [isEditing, setIsEditing] = useState(false)

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

  const handleEdit = () => {
    setIsEditing(true)
  }

  const handleCancelEdit = () => {
    setIsEditing(false)
    // 重新加载数据以确保显示最新内容
    const loadMemory = async () => {
      try {
        const data = await getMemory(memoryId)
        setMemory(data)
      } catch (err) {
        setError(err.message || '加载失败')
      }
    }
    loadMemory()
  }

  const handleSubmitEdit = async (data) => {
    try {
      await onUpdate(memory.id, data)
      setIsEditing(false)
      // 重新加载数据
      const updatedMemory = await getMemory(memoryId)
      setMemory(updatedMemory)
    } catch (err) {
      throw err
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

  // 编辑模式
  if (isEditing) {
    return (
      <div className="memory-detail">
        <div className="memory-detail-header">
          <button onClick={handleCancelEdit} className="back-button">✕ 取消编辑</button>
        </div>
        <div className="memory-detail-body-scrollable">
          <div className="memory-detail-body">
            <MemoryForm
              initialData={memory}
              isEdit={true}
              onSubmit={handleSubmitEdit}
              onCancel={handleCancelEdit}
            />
          </div>
        </div>
      </div>
    )
  }

  // 查看模式
  return (
    <div className="memory-detail">
      <div className="memory-detail-header">
        <button onClick={onBack} className="back-button">✕ 关闭</button>
        <div className="memory-detail-actions">
          <button onClick={handleEdit} className="edit-button">编辑</button>
          <button onClick={handleDelete} className="delete-button">删除</button>
        </div>
      </div>

      <div className="memory-detail-fixed">
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
        </div>
      </div>

      <div className="memory-detail-body-scrollable">
        <div className="memory-detail-body">
          <p>{memory.content}</p>
        </div>
      </div>
    </div>
  )
}

export default MemoryDetail

