import type { NoteContent } from "@/models/Notes"

export type WebSocketMessage = {
  data: NoteContent
}

type NoteUpdateCallback = (note: NoteContent) => void

class WebSocketClient {
  private ws: WebSocket | null = null
  private onNoteUpdate: NoteUpdateCallback | null = null

  connect(url: string): void {
    if (this.ws?.readyState === WebSocket.OPEN) return

    this.ws = new WebSocket(url)

    this.ws.onopen = () => console.log("WS connected")

    this.ws.onmessage = (event) => {
      try {
        const message: WebSocketMessage = JSON.parse(event.data)
        if (this.onNoteUpdate) {
          this.onNoteUpdate(message.data)
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
    } else {
      console.warn("WebSocket not connected, cannot send message")
    }
  }

  onNotesUpdate(callback: NoteUpdateCallback): void {
    this.onNoteUpdate = callback
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
