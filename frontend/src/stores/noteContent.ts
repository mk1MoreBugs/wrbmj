import { defineStore } from "pinia"
import { ref } from "vue"

import { wsClient } from "@/api/websocket"

import type { NoteContent } from "@/models/Notes"

export const useNoteContentStore = defineStore("noteContent", () => {
  const noteItem = ref<NoteContent>()

  function updateNote(note: NoteContent) {
    // Если уже загружена заметка, то обновляем в случае, когда id совпадают
    if (noteItem.value != undefined && note.id === noteItem.value?.id) {
      noteItem.value = note
    }
    // При инициализации заметки
    if (noteItem.value == undefined) {
      noteItem.value = note
    }
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
