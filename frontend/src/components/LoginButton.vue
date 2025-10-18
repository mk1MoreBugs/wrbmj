<script setup lang="ts">
const emit = defineEmits<{
  (e: "onClick"): void
}>()

const handleClick = (): void => {
    emit("onClick")
}
</script>

<template>
    <button
        type="submit"
        @click="handleClick"
        class="
          w-80 h-15 m-2
          flex justify-center items-center
          rounded-xl
          font-sans text-h2 text-secondary-content
          bg-secondary
        "
    >
        <slot></slot>

    </button>

</template>
