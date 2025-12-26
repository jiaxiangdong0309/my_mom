/**
 * 主应用组件
 */
import React, { useState, useEffect } from 'react'
import Layout from './components/Layout'
import MemoryList from './components/MemoryList'
import MemoryForm from './components/MemoryForm'
import MemoryDetail from './components/MemoryDetail'
import SearchBar from './components/SearchBar'
import SearchResults from './components/SearchResults'
import SuggestionCard from './components/SuggestionCard'
import { createMemory, deleteMemory, searchMemories, searchMemoriesSQLite, getAllMemories, getStats } from './api'
import { generateRandomSuggestions } from './utils/randomSuggestions'

function App() {
  // 页面状态：'list' | 'create' | 'detail' | 'search'
  const [currentPage, setCurrentPage] = useState('list')
  const [memories, setMemories] = useState([])
  const [searchResults, setSearchResults] = useState([])
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedMemoryId, setSelectedMemoryId] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [refreshTrigger, setRefreshTrigger] = useState(0)
  const [suggestions, setSuggestions] = useState([])
  const [suggestionsExpanded, setSuggestionsExpanded] = useState(false)
  const [searchMode, setSearchMode] = useState('vector') // 'vector' | 'sqlite'
  const [stats, setStats] = useState({ sqlite_count: 0, chroma_count: 0 })

  // 生成随机建议 - 每次进入页面时生成
  useEffect(() => {
    const pagesWithSuggestions = ['list', 'create', 'detail', 'search']
    if (pagesWithSuggestions.includes(currentPage)) {
      const newSuggestions = generateRandomSuggestions(3)
      setSuggestions(newSuggestions)
    }
  }, [currentPage])

  // 加载统计信息
  useEffect(() => {
    const loadStats = async () => {
      try {
        const data = await getStats()
        setStats(data)
      } catch (err) {
        // 统计信息加载失败不影响主功能，静默处理
        console.error('加载统计信息失败:', err)
      }
    }
    loadStats()
  }, [refreshTrigger])

  // 加载所有记忆
  useEffect(() => {
    const loadMemories = async () => {
      if (currentPage === 'list' && memories.length === 0 && !loading) {
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
    }
    loadMemories()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [refreshTrigger])

  // 执行搜索
  const handleSearch = async (query, mode = searchMode) => {
    setSearchQuery(query)
    if (!query) {
      setSearchResults([])
      setCurrentPage('list')
      return
    }

    setLoading(true)
    setError(null)
    try {
      let results
      if (mode === 'sqlite') {
        results = await searchMemoriesSQLite(query, 10)
      } else {
        results = await searchMemories(query, 10)
      }
      setSearchResults(results)
      setCurrentPage('search')
    } catch (err) {
      setError(err.message || '搜索失败')
      setSearchResults([])
    } finally {
      setLoading(false)
    }
  }

  // 切换搜索模式
  const handleModeChange = (mode) => {
    setSearchMode(mode)
    // 如果当前有搜索查询，切换模式后重新搜索
    if (searchQuery) {
      handleSearch(searchQuery, mode)
    }
  }

  // 创建记忆
  const handleCreateMemory = async (data) => {
    setLoading(true)
    setError(null)
    try {
      const newMemory = await createMemory(data.title, data.content, data.tags)
      setMemories([newMemory, ...memories])
      setCurrentPage('list')
      setRefreshTrigger(prev => prev + 1)
      // 创建成功后重新生成建议
      const newSuggestions = generateRandomSuggestions(3)
      setSuggestions(newSuggestions)
    } catch (err) {
      setError(err.message || '创建失败')
      throw err
    } finally {
      setLoading(false)
    }
  }

  // 点击建议卡片，直接创建记忆
  const handleSuggestionClick = async (suggestion) => {
    await handleCreateMemory(suggestion)
  }

  // 删除记忆
  const handleDeleteMemory = async (id) => {
    setLoading(true)
    setError(null)
    try {
      await deleteMemory(id)
      setMemories(memories.filter(m => m.id !== id))
      setSearchResults(searchResults.filter(m => m.id !== id))
      if (currentPage === 'detail' && selectedMemoryId === id) {
        setCurrentPage('list')
        setSelectedMemoryId(null)
      }
      setRefreshTrigger(prev => prev + 1)
    } catch (err) {
      setError(err.message || '删除失败')
    } finally {
      setLoading(false)
    }
  }

  // 查看记忆详情
  const handleMemoryClick = (id) => {
    setSelectedMemoryId(id)
    setCurrentPage('detail')
  }

  // 返回列表
  const handleBack = () => {
    setCurrentPage('list')
    setSelectedMemoryId(null)
  }

  // 渲染建议区域
  const renderSuggestions = () => {
    const pagesWithSuggestions = ['list', 'create', 'detail', 'search']
    if (!pagesWithSuggestions.includes(currentPage) || suggestions.length === 0) {
      return null
    }

    return (
      <div className="suggestions-section">
        <div
          className="suggestions-header"
          onClick={() => setSuggestionsExpanded(!suggestionsExpanded)}
        >
          <h3>💡 快速创建建议</h3>
          <span className="suggestions-toggle">
            {suggestionsExpanded ? '▼' : '▶'}
          </span>
        </div>
        {suggestionsExpanded && (
          <div className="suggestions-list">
            {suggestions.map((suggestion, index) => (
              <SuggestionCard
                key={index}
                suggestion={suggestion}
                onClick={() => handleSuggestionClick(suggestion)}
              />
            ))}
          </div>
        )}
      </div>
    )
  }

  // 渲染当前页面
  const renderPage = () => {
    switch (currentPage) {
      case 'create':
        return (
          <>
            {renderSuggestions()}
            <MemoryForm
              onSubmit={handleCreateMemory}
              onCancel={handleBack}
            />
          </>
        )
      case 'detail':
        return (
          <>
            {renderSuggestions()}
            <MemoryDetail
              memoryId={selectedMemoryId}
              onBack={handleBack}
              onDelete={handleDeleteMemory}
            />
          </>
        )
      case 'search':
        return (
          <>
            {renderSuggestions()}
            <SearchResults
              results={searchResults}
              query={searchQuery}
              searchMode={searchMode}
              onMemoryClick={handleMemoryClick}
              onMemoryDelete={handleDeleteMemory}
            />
          </>
        )
      case 'list':
      default:
        return (
          <>
            {renderSuggestions()}
            <MemoryList
              memories={memories}
              onMemoryClick={handleMemoryClick}
              onMemoryDelete={handleDeleteMemory}
              refreshTrigger={refreshTrigger}
            />
          </>
        )
    }
  }

  return (
    <Layout>
      <div className="app-container">
        {error && (
          <div className="app-error" onClick={() => setError(null)}>
            {error} (点击关闭)
          </div>
        )}

        <div className="app-header-actions">
          <SearchBar
            onSearch={handleSearch}
            loading={loading}
            searchMode={searchMode}
            onModeChange={handleModeChange}
          />
          {currentPage !== 'create' && (
            <button
              className="btn-primary"
              onClick={() => setCurrentPage('create')}
            >
              + 创建记忆
            </button>
          )}
        </div>

        <div className="app-stats">
          <span>SQLite 数据 {stats.sqlite_count} 条</span>
          <span>向量数据库 {stats.chroma_count} 条</span>
        </div>

        {renderPage()}
      </div>
    </Layout>
  )
}

export default App

