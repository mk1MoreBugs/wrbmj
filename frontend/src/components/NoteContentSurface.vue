<script setup lang="ts">

const props = defineProps<{id: string}>()

</script>

<template>
  <div class="flex flex-col">
    Note content {{ props.id }}
  </div>

</template>
