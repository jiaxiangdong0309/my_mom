import React, { useEffect, useRef } from 'react'
import VChart from '@visactor/vchart'

/**
 * 标签词云组件 (使用 VChart)
 */
const TagWordCloud = ({ data }) => {
  const containerRef = useRef(null)
  const chartInstance = useRef(null)

  useEffect(() => {
    if (!containerRef.current || !data || data.length === 0) return

    const spec = {
      type: 'wordCloud',
      data: [
        {
          id: 'data',
          values: data
        }
      ],
      nameField: 'name',
      valueField: 'value',
      seriesField: 'name',
      maskShape: 'circle',
      wordCloudConfig: {
        zoomToFit: true
      },
      word: {
        padding: 5,
        style: {
          fontFamily: 'sans-serif',
          fontWeight: 'bold',
          cursor: 'pointer'
        }
      },
      tooltip: {
        visible: true,
        mark: {
          content: [
            {
              key: (datum) => datum.name,
              value: (datum) => datum.value + ' 次'
            }
          ]
        }
      }
    }

    try {
      if (chartInstance.current) {
        chartInstance.current.release()
      }

      const vchart = new VChart(spec, { dom: containerRef.current })
      vchart.renderSync()
      chartInstance.current = vchart
    } catch (error) {
      console.error('词云图渲染失败:', error)
    }

    return () => {
      if (chartInstance.current) {
        chartInstance.current.release()
        chartInstance.current = null
      }
    }
  }, [data])

  if (!data || data.length === 0) {
    return (
      <div className="word-cloud-empty">
        <p>暂无标签数据</p>
      </div>
    )
  }

  return <div ref={containerRef} className="vchart-container" style={{ width: '100%', height: '400px' }} />
}

export default TagWordCloud
