<script setup lang="ts">
import {onBeforeUnmount, watch, computed } from 'vue'

import { useNoteContentStore } from "@/stores/noteContent"

import type { NoteContent } from "@/models/Notes"


const props = defineProps<{id: string}>()

const emit = defineEmits<{
  (e: "update-note", updatedNote: NoteContent): void
}>()

const store = useNoteContentStore()

const noteTitleName = computed(() => store.noteItem?.title_name ?? '')

const noteContent = computed(() => store.noteItem?.note_content ?? '')

const handleInputTitleName = (event: Event) => {
  const target = event.target as HTMLInputElement

  const updatedNote: NoteContent = {
    id: store.noteItem?.id as number,
    last_update: store.noteItem?.last_update as string,
    title_name: target.value,
    note_content: store.noteItem?.note_content as string,
  }

  store.updateNote(updatedNote)
  emit('update-note', updatedNote)
}

const handleInputContentNote = (event: Event) => {
  const target = event.target as HTMLInputElement

  const updatedNote: NoteContent = {
    id: store.noteItem?.id as number,
    last_update: store.noteItem?.last_update as string,
    title_name: store.noteItem?.title_name as string,
    note_content: target.value,
  }

  store.updateNote(updatedNote)
  emit('update-note', updatedNote)
}

onBeforeUnmount(() => {
  store.closeWebSocket()
})

// Костыль, чтобы при переключении заметок открывалась нужная
// (тут по сути 1 компонент для редактирования множества заметок)
watch(props, () => {
  if (props.id !== undefined && props.id !== null) {
    const wsUrl = `ws://localhost/api/v1/notes/${props.id}/edit`
    store.initWebSocket(wsUrl)
  }
}, { immediate: true })
</script>

<template>
  <div class="flex flex-col">
    <p>
      Тема:
    </p>
    <input
      :value="noteTitleName"
      @input="handleInputTitleName"
      type="text"
      class="mt-1 block w-full border rounded-md p-2"
      placeholder="Заголовок заметки"
    />
    <p>
      Контент:
    </p>
    <textarea
      :value="noteContent"
      @input="handleInputContentNote"
      placeholder="Содержимое заметки..."
      rows="10"
      class="mt-1 block w-full border rounded-md p-2 font-mono"
    />

  </div>

</template>
