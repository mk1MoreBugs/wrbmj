import { defineStore } from "pinia"
import axios from "axios"

import { notesApi } from "@/api/notes"

import type { NoteShortInfo } from "@/models/Notes"
import type { NoteResponse } from "@/models/ApiResponse"

export const useNotesStore = defineStore("notes", () => {

  async function getNotes(): Promise<NoteShortInfo[]> {
      try {
        const response: NoteResponse[] = await notesApi.getNotes()
        const notes: NoteShortInfo[] = response.map((it) => ({
          id: it.id,
          lastUpdate: new Date(it.last_update),
          titleName: it.title_name,
          shortDescription: it.short_description,
        }))
        return notes
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
      getNotes
     }
})
