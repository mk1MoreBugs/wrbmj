<script setup lang="ts">
import { useRouter } from 'vue-router'
import { onMounted, ref, watch } from 'vue'

import { useNotesListStore } from "@/stores/notesList"
import NoteCard from "@/components/NoteCard.vue"

import type { NoteContent } from "@/models/Notes"

const props = defineProps<{currentEditedNote: NoteContent | undefined}>()

const store = useNotesListStore()
const router = useRouter()


const isCreating = ref(false)

onMounted(() => {
  store.fetchNotes()
})

const handleCardClick = (id: number) => {
  try {
    router.push(`/notes/${id}`)
  } catch (error) {
    console.error('Notes fetch failed', error)
  }
}

const handleAddNoteClick = async () => {
  if (isCreating.value) return

  isCreating.value = true

  try {
    const note = await store.createNote()
    if (note?.id != null) {
      store.fetchNotes()
      router.push(`/notes/${note.id}`)
    }
  } catch (error) {
    console.error('Create note is failed', error)
  } finally {
    isCreating.value = false
  }
}

// Костыль для обновления заметок при редактировании
// TODO: fix me
watch(() => props.currentEditedNote, (newNote) => {
  if (newNote?.title_name !== undefined && newNote?.note_content !== undefined) {
    store.updateNoteInList(newNote)
  }
}, { immediate: true })

</script>

<template>
  <div class="flex flex-col gap-3">
    <div v-for="note in store.notes" :key="note.id">
      <NoteCard
        :id="note.id"
        :last-update="note.lastUpdate"
        :title-name="note.titleName"
        :short-description="note.shortDescription"
        @click="handleCardClick"
      />
    </div>

    <div>
      <button type="button" @click="handleAddNoteClick" title="Add Note" aria-label="Add Note" class="
          w-80 h-15 m-2
          flex justify-center items-center
          rounded-xl
          font-sans text-h2 text-secondary-content
          bg-secondary
        " :disabled="isCreating">
        + Добавить заметку
      </button>
    </div>
  </div>
</template>
