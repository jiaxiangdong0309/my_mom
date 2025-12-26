/**
 * 基础布局组件
 */
import React from 'react'

function Layout({ children, header }) {
  return (
    <div className="layout">
      <header className="layout-header">
        {header || <h1>AI Memory Hub</h1>}
      </header>
      <main className="layout-main">
        {children}
      </main>
    </div>
  )
}

export default Layout

