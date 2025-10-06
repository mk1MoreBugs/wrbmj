<script setup lang="ts">

const props = defineProps<{isFormValid: boolean}>()

</script>

<template>
    <button
        type="submit"
        :disabled="!props.isFormValid"
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