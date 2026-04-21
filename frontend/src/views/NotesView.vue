<script setup lang="ts">
import { useRoute } from 'vue-router'
import { computed } from "vue"

import NotesList from '@/components/NotesList.vue'
import NoteContentSurface from '@/components/NoteContentSurface.vue'

const route = useRoute()

const noteId = computed(() => {
  return Array.isArray(route.params.id) ? route.params.id[0] : route.params.id
})

</script>

<template>
  <div
    class="flex"
  >
    <NotesList/>
    <div class="size-6"></div>
    <NoteContentSurface :id="noteId"/>
  </div>
</template>
