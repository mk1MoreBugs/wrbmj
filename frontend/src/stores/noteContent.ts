import { defineStore } from "pinia"
import { ref } from "vue"

import { wsClient } from "@/api/websocket"

import type { NoteContent } from "@/models/Notes"

export const useNoteContentStore = defineStore("noteContent", () => {
  const noteItem = ref<NoteContent>()

  function updateNote(note: NoteContent) {
    noteItem.value = note
  }

  function updateNoteInServer(note: NoteContent) {
      wsClient.sendMessage(note)
  }

  function initWebSocket(url: string) {
    // Удаляем старые данные
    noteItem.value = undefined

    const token: string | null = localStorage.getItem("token") || null
    if (!token) {
      throw Error("Token is invalid!")
    }

    // Закрываем предыдущее соединение (важно при смене заметки)
    wsClient.disconnect()

    wsClient.connect(url + `?token=${encodeURIComponent(`${token}`)}`, updateNote)
  }

  function closeWebSocket() {
    wsClient.disconnect()
  }

  return {
    noteItem,
    initWebSocket,
    closeWebSocket,
    updateNote: updateNoteInServer,
  }
})
