<script setup lang="ts">
import { useRouter } from 'vue-router'
import { onMounted, ref, watch } from 'vue'
import { storeToRefs } from 'pinia'

import { useNotesListStore } from "@/stores/notesList"
import NoteCard from "@/components/NoteCard.vue"

import type { NoteEditedProps } from "@/models/Notes"

const props = defineProps<{currentEditedNote: NoteEditedProps | undefined}>()

const store = useNotesListStore()
const router = useRouter()

const { notes } = storeToRefs(store)

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
    store.fetchNotes()
  }
}, { immediate: true })

</script>

<template>
  <div class="flex flex-col gap-3">
    <div v-for="note in notes" :key="note.id">
      <NoteCard v-bind="note" @click="handleCardClick" />
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
