/**
 * API 调用模块
 */

const BASE_URL = '/api/v1'

/**
 * 统一错误处理
 */
async function handleResponse(response) {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: '网络错误' }))
    throw new Error(error.detail || `HTTP ${response.status}: ${response.statusText}`)
  }
  return response.json()
}

/**
 * 向量搜索记忆（语义搜索）
 */
export async function searchMemories(query, limit = 10) {
  try {
    const response = await fetch(`${BASE_URL}/search/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, limit })
    })
    return await handleResponse(response)
  } catch (error) {
    if (error.message.includes('Failed to fetch')) {
      throw new Error('无法连接到服务器，请检查后端服务是否启动')
    }
    throw error
  }
}

/**
 * SQLite 文本搜索记忆
 */
export async function searchMemoriesSQLite(query, limit = 10) {
  try {
    const response = await fetch(`${BASE_URL}/search/sqlite`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, limit })
    })
    return await handleResponse(response)
  } catch (error) {
    if (error.message.includes('Failed to fetch')) {
      throw new Error('无法连接到服务器，请检查后端服务是否启动')
    }
    throw error
  }
}

/**
 * 创建记忆
 */
export async function createMemory(title, content, tags = []) {
  try {
    const response = await fetch(`${BASE_URL}/memories/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, content, tags })
    })
    return await handleResponse(response)
  } catch (error) {
    if (error.message.includes('Failed to fetch')) {
      throw new Error('无法连接到服务器，请检查后端服务是否启动')
    }
    throw error
  }
}

/**
 * 获取所有记忆列表
 */
export async function getAllMemories() {
  try {
    const response = await fetch(`${BASE_URL}/memories/`)
    return await handleResponse(response)
  } catch (error) {
    if (error.message.includes('Failed to fetch')) {
      throw new Error('无法连接到服务器，请检查后端服务是否启动')
    }
    throw error
  }
}

/**
 * 获取单个记忆详情
 */
export async function getMemory(id) {
  try {
    const response = await fetch(`${BASE_URL}/memories/${id}`)
    return await handleResponse(response)
  } catch (error) {
    if (error.message.includes('Failed to fetch')) {
      throw new Error('无法连接到服务器，请检查后端服务是否启动')
    }
    throw error
  }
}

/**
 * 更新记忆
 */
export async function updateMemory(id, title, content, tags = []) {
  try {
    const response = await fetch(`${BASE_URL}/memories/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, content, tags })
    })
    return await handleResponse(response)
  } catch (error) {
    if (error.message.includes('Failed to fetch')) {
      throw new Error('无法连接到服务器，请检查后端服务是否启动')
    }
    throw error
  }
}

/**
 * 删除记忆
 */
export async function deleteMemory(id) {
  try {
    const response = await fetch(`${BASE_URL}/memories/${id}`, {
      method: 'DELETE'
    })
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: '删除失败' }))
      throw new Error(error.detail || `HTTP ${response.status}`)
    }
    return { success: true }
  } catch (error) {
    if (error.message.includes('Failed to fetch')) {
      throw new Error('无法连接到服务器，请检查后端服务是否启动')
    }
    throw error
  }
}

/**
 * 获取数据库统计信息
 */
export async function getStats() {
  try {
    const response = await fetch(`${BASE_URL}/memories/stats`)
    return await handleResponse(response)
  } catch (error) {
    if (error.message.includes('Failed to fetch')) {
      throw new Error('无法连接到服务器，请检查后端服务是否启动')
    }
    throw error
  }
}

