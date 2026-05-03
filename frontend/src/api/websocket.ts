import type { NoteContent } from "@/models/Notes"

type NoteUpdateCallback = (note: NoteContent) => void

class WebSocketClient {
  private ws: WebSocket | null = null
  private onNoteUpdate: NoteUpdateCallback | null = null

  connect(url: string, onNoteUpdate: NoteUpdateCallback): void {
    this.onNoteUpdate = onNoteUpdate

    if (this.ws?.readyState === WebSocket.OPEN) return

    this.ws = new WebSocket(url)

    this.ws.onopen = () => console.log("WS connected")

    this.ws.onmessage = (event) => {
      try {
        const message: NoteContent = JSON.parse(event.data)
        if (this.onNoteUpdate) {
          this.onNoteUpdate(message)
        }
      } catch (e) {
        console.error("WS parse error", e)
      }
    }

    this.ws.onerror = (error) => console.error("WS error", error)

    this.ws.onclose = () => console.log("WS closed")
  }

  sendMessage(data: NoteContent): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data))
      console.log("WS send message")
    } else {
      console.warn("WebSocket not connected, cannot send message")
    }
  }

  disconnect(): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.close()
    }
    this.ws = null
    this.onNoteUpdate = null
  }
}

export const wsClient = new WebSocketClient()
