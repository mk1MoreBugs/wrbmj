<script setup lang="ts">

import InputField from "@/components/InputField.vue"

interface InputProps {
  id: string
  value: string
  error?: string
}

const props = withDefaults(defineProps<InputProps>(), {
    error: ''
})

const emit = defineEmits<{
  (e: "update:value", value: string): void
}>()

const handleInput = (value: string) => {
  emit("update:value", value)
}

</script>

<template>
    <InputField :id=props.id :error=props.error label="Paste password" type="password" :value=props.value @update:value="handleInput"/>
</template>
