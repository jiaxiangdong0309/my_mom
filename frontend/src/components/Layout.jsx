/**
 * 基础布局组件
 */
import React from 'react'

function Layout({ children, header, nav }) {
  return (
    <div className="layout">
      <header className="layout-header">
        <div className="header-container">
          <div className="header-left">
            {header || <h1>AI Memory Hub</h1>}
          </div>
          <nav className="header-nav">
            {nav}
          </nav>
        </div>
      </header>
      <main className="layout-main">
        {children}
      </main>
    </div>
  )
}

export default Layout

