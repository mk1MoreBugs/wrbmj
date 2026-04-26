<script setup lang="ts">
import {ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { storeToRefs } from 'pinia'

import { useNoteContentStore } from "@/stores/noteContent"

const props = defineProps<{id: string}>()

const store = useNoteContentStore()

const { noteContent } = storeToRefs(store)

// Локальная копия для редактирования
const localNote = ref({ ...noteContent.value })

onMounted(() => {
  const wsUrl = `ws://localhost/api/v1/notes/${props.id}/edit`
  store.initWebSocket(wsUrl)
})

onBeforeUnmount(() => {
  store.closeWebSocket()
})

watch(noteContent, (newVal) => {
  localNote.value = { ...newVal }
}, { immediate: true })

watch(localNote, (newValue) => {
  store.updateNote({
    id: newValue.id ?? 0,
    last_update: newValue.last_update ?? '',
    title_name: newValue.title_name ?? '',
    note_content: newValue.note_content ?? '',
  })
})

</script>

<template>
  <div class="flex flex-col">
    <p>
      Тема:
    </p>
    <input
        v-model="localNote.title_name"
        type="text"
        class="mt-1 block w-full border rounded-md p-2"
        placeholder="Заголовок заметки"
      />
    <p>
      Контент:
    </p>
    <textarea
      v-model="localNote.note_content"
      placeholder="Содержимое заметки..."
      rows="10"
      class="mt-1 block w-full border rounded-md p-2 font-mono"
    />

  </div>

</template>
