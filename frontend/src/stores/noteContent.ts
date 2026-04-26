import { defineStore } from "pinia"
import { ref } from "vue"

import { wsClient } from "@/api/websocket"

import type { NoteContent } from "@/models/Notes"

export const useNoteContentStore = defineStore("noteContent", () => {
  const noteContent = ref<NoteContent>()

  function updateNote(note: NoteContent) {
    noteContent.value = note
  }

  function updateNoteInServer(note: NoteContent) {
      wsClient.sendMessage(note)
  }

  function initWebSocket(url: string) {
    const token: string | null = localStorage.getItem("token") || null
    if (!token) {
      throw Error("Token is invalid!")
    }

    // Закрываем предыдущее соединение (важно при смене заметки)
    wsClient.disconnect()

    wsClient.connect(url + `?token=${encodeURIComponent(`Bearer ${token}`)}`)
    wsClient.onNotesUpdate(updateNote)
  }

  function closeWebSocket() {
    wsClient.disconnect()
  }

  return {
    noteContent,
    initWebSocket,
    closeWebSocket,
    updateNote: updateNoteInServer,
  }
})
