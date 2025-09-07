import { useState, useEffect, useCallback } from 'react'

interface WebSocketMessage {
  type: string
  data: any
}

export function useWebSocket() {
  const [socket, setSocket] = useState<WebSocket | null>(null)
  const [messages, setMessages] = useState<WebSocketMessage[]>([])
  const [isConnected, setIsConnected] = useState(false)

  const connect = useCallback((url: string) => {
    const ws = new WebSocket(url)
    
    ws.onopen = () => {
      setIsConnected(true)
      console.log('WebSocket connected')
    }
    
    ws.onmessage = (event) => {
      try {
        const message: WebSocketMessage = JSON.parse(event.data)
        setMessages(prev => [...prev, message])
      } catch (error) {
        console.error('Error parsing WebSocket message:', error)
      }
    }
    
    ws.onclose = () => {
      setIsConnected(false)
      console.log('WebSocket disconnected')
    }
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
    }
    
    setSocket(ws)
  }, [])

  const send = useCallback((message: WebSocketMessage) => {
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify(message))
    }
  }, [socket])

  useEffect(() => {
    return () => {
      if (socket) {
        socket.close()
      }
    }
  }, [socket])

  return {
    connect,
    send,
    messages,
    isConnected
  }
}