import React, { useEffect, useRef } from 'react'
import VChart from '@visactor/vchart'

/**
 * 标签词云图组件
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
      fontFamily: 'PingFang SC, Microsoft YaHei, sans-serif',
      fontWeightRange: [400, 700],
      fontSizeRange: [15, 60],
      maskShape: 'circle',
      word: {
        style: {
          fill: (datum) => {
            const colors = [
              '#2E5CFF', '#00B42A', '#F77234', '#F53F3F', '#722ED1',
              '#14C9C9', '#FADC19', '#FF7D00', '#D91AD9', '#3491FA'
            ]
            const index = Math.floor(Math.random() * colors.length)
            return colors[index]
          }
        }
      },
      tooltip: {
        visible: true,
        mark: {
          title: {
            visible: true,
            value: '标签统计'
          },
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

  return <div ref={containerRef} className="vchart-container" style={{ width: '100%', height: '400px' }} />
}

export default TagWordCloud

