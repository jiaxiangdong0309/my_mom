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
import UserProfile from './components/UserProfile'
import { createMemory, updateMemory, deleteMemory, searchMemories, searchMemoriesSQLite, getAllMemories, getStats } from './api'
import { generateRandomSuggestions } from './utils/randomSuggestions'

function App() {
  // 页面状态：'list' | 'create' | 'detail' | 'search'
  const [currentPage, setCurrentPage] = useState('list')
  /** @type {[any[], Function]} */
  const [memories, setMemories] = useState([])
  /** @type {[any[], Function]} */
  const [searchResults, setSearchResults] = useState([])
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedMemoryId, setSelectedMemoryId] = useState(null)
  const [showDetailDialog, setShowDetailDialog] = useState(false) // 控制详情dialog显示
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [refreshTrigger, setRefreshTrigger] = useState(0)
  /** @type {[any[], Function]} */
  const [suggestions, setSuggestions] = useState([])
  const [suggestionsExpanded, setSuggestionsExpanded] = useState(false)
  const [searchMode, setSearchMode] = useState('vector') // 'vector' | 'sqlite'
  const [stats, setStats] = useState({ sqlite_count: 0, chroma_count: 0 })

  // 统计标签使用情况
  const tagStats = React.useMemo(() => {
    const tagCount = {}
    memories.forEach(memory => {
      if (memory.tags && Array.isArray(memory.tags)) {
        // 每个记忆中的标签去重后统计
        const uniqueTags = [...new Set(memory.tags)]
        uniqueTags.forEach(tag => {
          if (tag) {
            tagCount[tag] = (tagCount[tag] || 0) + 1
          }
        })
      }
    })
    return Object.entries(tagCount)
      .map(([tag, count]) => ({ name: tag, value: count }))
      .sort((a, b) => b.value - a.value)
  }, [memories])

  // 生成随机建议 - 每次进入页面时生成
  useEffect(() => {
    const pagesWithSuggestions = ['list', 'create', 'search']
    if (pagesWithSuggestions.includes(currentPage)) {
      const newSuggestions = generateRandomSuggestions(3)
      setSuggestions(newSuggestions)
    }
  }, [currentPage])

  // 控制弹窗打开时禁用页面滚动
  useEffect(() => {
    if (showDetailDialog) {
      // 保存当前滚动位置
      const scrollY = window.scrollY
      // 禁用body滚动
      document.body.style.position = 'fixed'
      document.body.style.top = `-${scrollY}px`
      document.body.style.width = '100%'
      document.body.style.overflow = 'hidden'
    } else {
      // 恢复body滚动
      const scrollY = document.body.style.top
      document.body.style.position = ''
      document.body.style.top = ''
      document.body.style.width = ''
      document.body.style.overflow = ''
      if (scrollY) {
        window.scrollTo(0, parseInt(scrollY || '0') * -1)
      }
    }

    // 清理函数
    return () => {
      if (!showDetailDialog) {
        document.body.style.position = ''
        document.body.style.top = ''
        document.body.style.width = ''
        document.body.style.overflow = ''
      }
    }
  }, [showDetailDialog])

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
      if ((currentPage === 'list' || currentPage === 'profile') && memories.length === 0 && !loading) {
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
  }, [refreshTrigger, currentPage])

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

  // 更新记忆
  const handleUpdateMemory = async (id, data) => {
    setLoading(true)
    setError(null)
    try {
      const updatedMemory = await updateMemory(id, data.title, data.content, data.tags)
      // 更新记忆列表
      setMemories(memories.map(m => m.id === id ? updatedMemory : m))
      // 更新搜索结果
      setSearchResults(searchResults.map(m => m.id === id ? updatedMemory : m))
      setRefreshTrigger(prev => prev + 1)
    } catch (err) {
      setError(err.message || '更新失败')
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
      if (selectedMemoryId === id) {
        setShowDetailDialog(false)
        setSelectedMemoryId(null)
      }
      setRefreshTrigger(prev => prev + 1)
    } catch (err) {
      setError(err.message || '删除失败')
    } finally {
      setLoading(false)
    }
  }

  // 查看记忆详情 - 使用dialog展示
  const handleMemoryClick = (id) => {
    setSelectedMemoryId(id)
    setShowDetailDialog(true)
  }

  // 关闭详情dialog
  const handleCloseDetailDialog = () => {
    setShowDetailDialog(false)
    setSelectedMemoryId(null)
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
          <div className="page-container fadeIn">
            <div className="page-header">
              <h2>✨ 创建新记忆</h2>
              <button className="btn-secondary" onClick={handleBack}>返回列表</button>
            </div>
            {renderSuggestions()}
            <MemoryForm
              onSubmit={handleCreateMemory}
              onCancel={handleBack}
            />
          </div>
        )
      case 'search':
        return (
          <div className="page-container fadeIn">
            <div className="page-header">
              <h2>🔍 搜索记忆</h2>
              <div className="app-stats">
                <span>SQLite 数据 {stats.sqlite_count} 条</span>
                <span>向量数据库 {stats.chroma_count} 条</span>
              </div>
            </div>
            <div className="search-section">
              <SearchBar
                onSearch={handleSearch}
                loading={loading}
                searchMode={searchMode}
                onModeChange={handleModeChange}
              />
            </div>
            <SearchResults
              results={searchResults}
              query={searchQuery}
              searchMode={searchMode}
              onMemoryClick={handleMemoryClick}
              onMemoryDelete={handleDeleteMemory}
            />
          </div>
        )
      case 'profile':
        return (
          <div className="page-container fadeIn">
            <UserProfile
              tagStats={tagStats}
              totalMemories={stats.sqlite_count}
              onBack={handleBack}
              loading={loading}
            />
          </div>
        )
      case 'list':
      default:
        return (
          <div className="page-container fadeIn">
            <div className="page-header">
              <h2>📚 全部记忆</h2>
              <button
                className="btn-primary"
                onClick={() => setCurrentPage('create')}
              >
                + 创建记忆
              </button>
            </div>
            {renderSuggestions()}
            <MemoryList
              memories={memories}
              onMemoryClick={handleMemoryClick}
              onMemoryDelete={handleDeleteMemory}
              refreshTrigger={refreshTrigger}
            />
          </div>
        )
    }
  }

  const renderNav = () => (
    <>
      <div
        className={`nav-item ${(currentPage === 'list' || currentPage === 'create') ? 'active' : ''}`}
        onClick={() => {
          setCurrentPage('list')
          setSearchQuery('')
        }}
      >
        🏠 首页
      </div>
      <div
        className={`nav-item ${currentPage === 'search' ? 'active' : ''}`}
        onClick={() => setCurrentPage('search')}
      >
        🔍 搜索
      </div>
      <div
        className={`nav-item ${currentPage === 'profile' ? 'active' : ''}`}
        onClick={() => setCurrentPage('profile')}
      >
        👤 用户画像
      </div>
    </>
  )

  return (
    <Layout
      header={<h1 onClick={() => {setCurrentPage('list'); setSearchQuery('')}} style={{ cursor: 'pointer' }}>AI Memory Hub</h1>}
      nav={renderNav()}
    >
      <div className="app-container">
        {error && (
          <div className="app-error" onClick={() => setError(null)}>
            {error} (点击关闭)
          </div>
        )}

        {renderPage()}
      </div>

      {/* 详情Dialog */}
      {showDetailDialog && (
        <div className="dialog-overlay" onClick={handleCloseDetailDialog}>
          <div className="dialog-container" onClick={(e) => e.stopPropagation()}>
            <MemoryDetail
              memoryId={selectedMemoryId}
              onBack={handleCloseDetailDialog}
              onDelete={(id) => {
                handleDeleteMemory(id)
                handleCloseDetailDialog()
              }}
              onUpdate={handleUpdateMemory}
            />
          </div>
        </div>
      )}
    </Layout>
  )
}

export default App

