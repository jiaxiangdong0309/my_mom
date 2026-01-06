import React from 'react'
import TagWordCloud from './TagWordCloud'
import TagPieChart from './TagPieChart'
import TagBarChart from './TagBarChart'

/**
 * 用户画像页面组件
 */
function UserProfile({ tagStats, totalMemories, onBack, loading }) {
  if (loading && tagStats.length === 0) {
    return (
      <div className="user-profile loading">
        <div className="loader"></div>
        <p>正在生成用户画像...</p>
      </div>
    )
  }

  if (tagStats.length === 0) {
    return (
      <div className="user-profile empty">
        <h2>暂无标签数据</h2>
        <p>创建一些带有标签的记忆来生成你的用户画像吧！</p>
        <button className="btn-primary" onClick={onBack}>返回首页</button>
      </div>
    )
  }

  return (
    <div className="user-profile">
      <div className="profile-header">

        <div className="profile-summary">
          <div className="summary-item">
            <span className="summary-value">{totalMemories}</span>
            <span className="summary-label">记忆总数</span>
          </div>
          <div className="summary-item">
            <span className="summary-value">{tagStats.length}</span>
            <span className="summary-label">不同标签</span>
          </div>
        </div>
      </div>

      <div className="profile-content">
        <section className="chart-section">
          <h3>标签词云</h3>
          <p className="chart-desc">标签越大，代表你在该领域记录的内容越多</p>
          <div className="chart-container word-cloud-container">
            <TagWordCloud data={tagStats} />
          </div>
        </section>

        <div className="charts-grid">
          <section className="chart-section">
            <h3>标签分布</h3>
            <div className="chart-container">
              <TagPieChart data={tagStats.slice(0, 10)} />
            </div>
          </section>

          <section className="chart-section">
            <h3>Top 10 标签频率</h3>
            <div className="chart-container">
              <TagBarChart data={tagStats.slice(0, 10)} />
            </div>
          </section>
        </div>
      </div>
    </div>
  )
}

export default UserProfile

