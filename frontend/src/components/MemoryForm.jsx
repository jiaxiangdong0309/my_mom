/**
 * 创建/编辑记忆表单组件
 */
import React, { useState, useEffect } from 'react'

function MemoryForm({ onSubmit, onCancel, initialData = null, isEdit = false }) {
  const [title, setTitle] = useState(initialData?.title || '')
  const [content, setContent] = useState(initialData?.content || '')
  const [tags, setTags] = useState(initialData?.tags?.join(', ') || '')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  // 当 initialData 变化时更新表单数据
  useEffect(() => {
    if (initialData) {
      setTitle(initialData.title || '')
      setContent(initialData.content || '')
      setTags(initialData.tags?.join(', ') || '')
    }
  }, [initialData])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    // 验证必填字段
    if (!title.trim()) {
      setError('标题不能为空')
      return
    }
    if (!content.trim()) {
      setError('内容不能为空')
      return
    }

    // 处理标签
    const tagList = tags
      .split(',')
      .map(tag => tag.trim())
      .filter(tag => tag.length > 0)

    setSubmitting(true)
    try {
      await onSubmit({
        title: title.trim(),
        content: content.trim(),
        tags: tagList
      })
      // 清空表单
      setTitle('')
      setContent('')
      setTags('')
    } catch (err) {
      setError(err.message || '创建失败，请重试')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <form className="memory-form" onSubmit={handleSubmit}>
      <h2>{isEdit ? '编辑记忆' : '创建新记忆'}</h2>

      {error && <div className="form-error">{error}</div>}

      <div className="form-group">
        <label htmlFor="title">标题 *</label>
        <input
          id="title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="输入记忆标题"
          disabled={submitting}
        />
      </div>

      <div className="form-group">
        <label htmlFor="content">内容 *</label>
        <textarea
          id="content"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="输入记忆内容"
          rows={6}
          disabled={submitting}
        />
      </div>

      <div className="form-group">
        <label htmlFor="tags">标签</label>
        <input
          id="tags"
          type="text"
          value={tags}
          onChange={(e) => setTags(e.target.value)}
          placeholder="用逗号分隔多个标签，例如：工作, 重要"
          disabled={submitting}
        />
      </div>

      <div className="form-actions">
        {onCancel && (
          <button type="button" onClick={onCancel} disabled={submitting}>
            取消
          </button>
        )}
        <button type="submit" disabled={submitting}>
          {submitting ? (isEdit ? '保存中...' : '创建中...') : (isEdit ? '保存修改' : '创建记忆')}
        </button>
      </div>
    </form>
  )
}

export default MemoryForm

