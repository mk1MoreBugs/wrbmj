<script setup lang="ts">
import { useRoute } from 'vue-router'
import { computed, ref } from "vue"

import NotesList from '@/components/NotesList.vue'
import NoteContentSurface from '@/components/NoteContentSurface.vue'

import type { NoteContent } from "@/models/Notes"

const route = useRoute()

const noteId = computed(() => {
  return Array.isArray(route.params.id) ? route.params.id[0] : route.params.id
})

const currentEditedNote = ref<NoteContent | undefined>(undefined)

const handleInput = (value: NoteContent) => {
  currentEditedNote.value = value
}

</script>

<template>
  <div
    class="flex"
  >
    <NotesList :currentEditedNote=currentEditedNote ?? {}/>
    <div class="size-6"></div>
    <NoteContentSurface :id="noteId" @update-note="handleInput"/>
  </div>
</template>
