/**
 * 搜索栏组件
 */
import React, { useState } from 'react'

function SearchBar({ onSearch, loading = false, searchMode = 'vector', onModeChange }) {
  const [query, setQuery] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (query.trim()) {
      onSearch(query.trim(), searchMode)
    }
  }

  const handleClear = () => {
    setQuery('')
    onSearch('', searchMode)
  }

  return (
    <div className="search-container">
      <form className="search-bar" onSubmit={handleSubmit}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={searchMode === 'vector' ? '输入关键词进行语义搜索...' : '输入关键词进行文本搜索...'}
          disabled={loading}
        />
        <div className="search-actions">
          {query && (
            <button type="button" onClick={handleClear} className="search-clear">
              清除
            </button>
          )}
          <button type="submit" disabled={loading || !query.trim()}>
            {loading ? '搜索中...' : '搜索'}
          </button>
        </div>
      </form>
      <div className="search-mode-selector">
        <button
          type="button"
          className={`search-mode-btn ${searchMode === 'vector' ? 'active' : ''}`}
          onClick={() => onModeChange('vector')}
          disabled={loading}
        >
          🔍 语义搜索
        </button>
        <button
          type="button"
          className={`search-mode-btn ${searchMode === 'sqlite' ? 'active' : ''}`}
          onClick={() => onModeChange('sqlite')}
          disabled={loading}
        >
          📝 文本搜索
        </button>
      </div>
    </div>
  )
}

export default SearchBar

