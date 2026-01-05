import React, { useEffect, useRef } from 'react'
import VChart from '@visactor/vchart'

/**
 * 标签柱状图组件
 */
const TagBarChart = ({ data }) => {
  const containerRef = useRef(null)
  const chartInstance = useRef(null)

  useEffect(() => {
    if (!containerRef.current || !data || data.length === 0) return

    const spec = {
      type: 'bar',
      data: [
        {
          id: 'data',
          values: data
        }
      ],
      xField: 'name',
      yField: 'value',
      seriesField: 'name',
      label: {
        visible: true
      },
      axes: [
        {
          orient: 'left',
          title: { visible: true, text: '频次' }
        },
        {
          orient: 'bottom',
          title: { visible: true, text: '标签' },
          label: {
            autoRotate: true
          }
        }
      ],
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
      console.error('柱状图渲染失败:', error)
    }

    return () => {
      if (chartInstance.current) {
        chartInstance.current.release()
        chartInstance.current = null
      }
    }
  }, [data])

  return <div ref={containerRef} className="vchart-container" style={{ width: '100%', height: '300px' }} />
}

export default TagBarChart







