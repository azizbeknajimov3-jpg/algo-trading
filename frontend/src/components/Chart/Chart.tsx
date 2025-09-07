'use client'

import { useEffect, useRef } from 'react'
import { createChart } from 'lightweight-charts'

interface ChartProps {
  data: any[]
  symbol: string
}

export default function Chart({ data, symbol }: ChartProps) {
  const chartContainerRef = useRef<HTMLDivElement>(null)
  const chartRef = useRef<any>(null)

  useEffect(() => {
    if (!chartContainerRef.current || data.length === 0) return

    // Initialize chart
    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: 400,
      layout: {
        backgroundColor: '#1a1a1a',
        textColor: '#d9d9d9',
      },
      grid: {
        vertLines: {
          color: 'rgba(42, 46, 57, 0.5)',
        },
        horzLines: {
          color: 'rgba(42, 46, 57, 0.5)',
        },
      },
    })

    const candleSeries = chart.addCandlestickSeries()
    candleSeries.setData(data)

    chartRef.current = chart

    // Handle resize
    const handleResize = () => {
      if (chartContainerRef.current) {
        chart.applyOptions({
          width: chartContainerRef.current.clientWidth,
        })
      }
    }

    window.addEventListener('resize', handleResize)

    return () => {
      window.removeEventListener('resize', handleResize)
      chart.remove()
    }
  }, [data, symbol])

  return (
    <div className="chart">
      <h3>{symbol} Chart</h3>
      <div ref={chartContainerRef} className="chart-container" />
    </div>
  )
}