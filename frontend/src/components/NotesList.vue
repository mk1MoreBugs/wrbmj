<script setup lang="ts">
  import { useRouter } from 'vue-router'
  import { computed, onMounted, ref } from 'vue'

  import {useNotesStore} from "@/stores/notes"
  import NoteCard from "@/components/NoteCard.vue"

  const store = useNotesStore()
  const router = useRouter()

  const notes = computed(() => store.notes)
  const isCreating = ref(false)

  onMounted(() => {
    store.fetchNotes()
  })

  const handleCardClick = (id: number) => {
    try {
      router.push(`/notes/${id}`)
    } catch(error) {
      console.error('Notes fetch failed', error)
    }
  }

  const handleAddNoteClick = async () => {
    if (isCreating.value) return

    isCreating.value = true

    try {
      const note = await store.createNote()
      if (note?.id != null) {
        router.push(`/notes/${note.id}`)
      }
    } catch(error) {
      console.error('Create note is failed', error)
    } finally {
      isCreating.value = false
    }
  }
</script>

<template>
  <div
    class="flex flex-col"
  >
    <li
      v-for="note in notes"
      :key="note.id"
    >
      <NoteCard
        v-bind="note"
        @click="handleCardClick"
      />
    </li>

    <!-- todo: add class="" -->
    <div>
      <button
        type="button"
        @click="handleAddNoteClick"
        title="Add Note"
        aria-label="Add Note"
        :disabled="isCreating"
      >
      + Добавить заметку
    </button>
    </div>
  </div>
</template>
