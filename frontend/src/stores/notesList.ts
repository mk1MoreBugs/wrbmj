import { defineStore } from "pinia"
import { ref } from "vue"
import axios from "axios"

import { notesApi } from "@/api/notes"

import type { NoteShortInfo, NoteContent } from "@/models/Notes"
import type { NoteResponse } from "@/models/ApiResponse"

export const useNotesListStore = defineStore("notesList", () => {
  const notes = ref<NoteShortInfo[]>()

  async function fetchNotes(): Promise<void> {
    try {
      const response: NoteResponse[] = await notesApi.getNotes()
      notes.value = response.map((it) => ({
        id: it.id,
        lastUpdate: new Date(it.last_update),
        titleName: it.title_name ?? "Без названия",
        shortDescription: it.short_description,
      }))
    } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        console.log("Error status:", error.response?.status)
        console.log("Error data:", error.response?.data)
      } else {
        console.error("Non-axios error:", error)
      }
      throw error
    }
  }

  function updateNoteInList(note: NoteContent) {
    let index = notes.value?.findIndex(it => it.id === note.id)
    if (index === undefined) {
      index = -1
    }

    const noteShortInfo = {
      id: note.id,
      lastUpdate: new Date(note.last_update),
      titleName: note.title_name,
      shortDescription: note.note_content.substring(0, 80)
    }

    if (index !== -1 && notes.value !== undefined) {
      notes.value[index] = noteShortInfo
    } else {
      notes.value?.unshift(noteShortInfo)
    }
  }

  async function createNote(): Promise<NoteShortInfo> {
    try {
      const response: NoteResponse = await notesApi.createNote()
      const newNote = {
        id: response.id,
        lastUpdate: new Date(response.last_update),
        titleName: response.title_name ?? "Без названия",
        shortDescription: response.short_description,
      }
      // notes.value?.unshift(newNote) // TODO: Нужно поменять ответ с сервера
      return newNote
    } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        console.log("Error status:", error.response?.status)
        console.log("Error data:", error.response?.data)
      } else {
        console.error("Non-axios error:", error)
      }
      throw error
    }
  }

  return {
    notes,
    fetchNotes,
    updateNoteInList,
    createNote,
  }
})
