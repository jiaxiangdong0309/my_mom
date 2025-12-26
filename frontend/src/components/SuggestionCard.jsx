/**
 * 建议卡片组件 - 显示随机生成的记忆建议
 */
import React from 'react'

function SuggestionCard({ suggestion, onClick }) {
  return (
    <div className="suggestion-item" onClick={onClick}>
      <div className="suggestion-item-main">
        <div className="suggestion-item-header">
          <h4 className="suggestion-item-title">{suggestion.title}</h4>
          <span className="suggestion-badge">建议</span>
        </div>
        <p className="suggestion-item-content">
          {suggestion.content.substring(0, 200)}
          {suggestion.content.length > 200 ? '...' : ''}
        </p>
        <div className="suggestion-item-footer">
          <div className="suggestion-item-tags">
            {suggestion.tags && suggestion.tags.length > 0 ? (
              suggestion.tags.map((tag, index) => (
                <span key={index} className="suggestion-tag">{tag}</span>
              ))
            ) : null}
          </div>
          <span className="suggestion-hint">点击创建</span>
        </div>
      </div>
    </div>
  )
}

export default SuggestionCard

