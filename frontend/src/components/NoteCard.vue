<script setup lang="ts">
import { computed } from "vue"

import type { NoteShortInfo } from "@/models/Notes"

const props = defineProps<NoteShortInfo>()

const emit = defineEmits<{
  (e: 'click', id: number): void
  (e: 'delete', id: number): void
}>()

const formattedDate = computed(() => {
  if (!props.lastUpdate) return 'Дата неизвестна'
  return new Intl.DateTimeFormat('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(new Date(props.lastUpdate))
})

const handleCardClick = () => {
  emit('click', props.id)
}

const handleDelete = (event: MouseEvent) => {
  event.stopPropagation() // чтобы клик по кнопке не вызывал открытие карточки
  emit('delete', props.id)
}
</script>

<template>
  <div
    class="group relative flex flex-col gap-2 rounded-xl border border-gray-200 bg-white p-4 shadow-sm transition-all duration-200 hover:shadow-md hover:border-gray-300 cursor-pointer"
    @click="handleCardClick"
  >
    <div class="flex justify-between items-start gap-2">
      <h3 class="text-lg font-semibold text-gray-900 line-clamp-1">
        {{ titleName }}
      </h3>
      <button
        @click="handleDelete"
        class="text-gray-400 hover:text-red-500 transition-colors opacity-0 group-hover:opacity-100 focus:opacity-100"
        aria-label="Удалить заметку"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
        </svg>
      </button>
    </div>

    <p class="text-sm text-gray-600 line-clamp-3">
      {{ shortDescription }}
    </p>

    <div class="mt-1 text-xs text-gray-400 flex items-center gap-1">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <span>Обновлено {{ formattedDate }}</span>
    </div>
  </div>
</template>

<style scoped>
/* Обрезаем текст до 3 строк */
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
