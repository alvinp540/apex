import { useEffect, useRef } from 'react'

export function useWebSocket(url, onMessage) {
  const wsRef = useRef(null)

  useEffect(() => {
    if (!url) return
    let ws
    let reconnectTimer
    let reconnectDelay = 1000
    let disconnected = false

    const connect = () => {
      const token = localStorage.getItem('access_token')
      const fullUrl = token ? `${url}?token=${encodeURIComponent(token)}` : url
      ws = new WebSocket(fullUrl)
      wsRef.current = ws

      ws.onmessage = (e) => {
        try {
          onMessage(JSON.parse(e.data))
        } catch (error) {
          console.error('Could not process a notification websocket message.', error)
        }
      }

      ws.onerror = () => console.error('Notification websocket connection failed.')

      ws.onclose = () => {
        if (disconnected) return
        reconnectTimer = setTimeout(connect, reconnectDelay)
        reconnectDelay = Math.min(reconnectDelay * 2, 30000)
      }
    }

    connect()

    return () => {
      disconnected = true
      clearTimeout(reconnectTimer)
      ws?.close()
      wsRef.current = null
    }
  }, [onMessage, url])

  return wsRef
}
