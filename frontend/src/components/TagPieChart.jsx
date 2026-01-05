import React, { useEffect, useRef } from 'react'
import VChart from '@visactor/vchart'

/**
 * 标签饼状图组件
 */
const TagPieChart = ({ data }) => {
  const containerRef = useRef(null)
  const chartInstance = useRef(null)

  useEffect(() => {
    if (!containerRef.current || !data || data.length === 0) return

    const spec = {
      type: 'pie',
      data: [
        {
          id: 'data',
          values: data
        }
      ],
      outerRadius: 0.8,
      innerRadius: 0.5,
      valueField: 'value',
      categoryField: 'name',
      label: {
        visible: true,
        style: {
          fontSize: 12
        }
      },
      legends: {
        visible: true,
        orient: 'bottom'
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
      console.error('饼状图渲染失败:', error)
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

export default TagPieChart







