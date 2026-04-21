import { defineStore } from "pinia"
import {ref} from "vue"

import axios from "axios"

import { notesApi } from "@/api/notes"

import type { NoteShortInfo } from "@/models/Notes"
import type { NoteResponse } from "@/models/ApiResponse"

export const useNotesStore = defineStore("notes", () => {

  const notes = ref<NoteShortInfo[]>()

  async function fetchNotes(): Promise<void> {
    try {
      const response: NoteResponse[] = await notesApi.getNotes()
      notes.value = response.map((it) => ({
        id: it.id,
        lastUpdate: new Date(it.last_update),
        titleName: it.title_name,
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

  async function createNote(): Promise<NoteShortInfo> {
    try {
      const response: NoteResponse = await notesApi.createNote()
      return {
        id: response.id,
        lastUpdate: new Date(response.last_update),
        titleName: response.title_name,
        shortDescription: response.short_description,
      }
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
    createNote,
  }
})
