import http from "@/api/http.ts"

import type {NoteResponse} from "@/models/ApiResponse.ts"

export const notesApi = {
  async getNotes(): Promise<NoteResponse[]> {
    const { data } = await http.get<NoteResponse[]>("/notes/")
    return data
  },

  async createNote(): Promise<NoteResponse> {
    const { data } = await http.post<NoteResponse>("/notes/")
    return data
  }
}

