<script setup lang="ts">
import { ref, computed } from "vue"
import type { InputTypeHTMLAttribute } from "vue"
import EyeIcon from '@/assets/icons/eye.vue'
import EyeCloseIcon from '@/assets/icons/eye-close.vue'

const props = defineProps<{
  id: string
  value: string
  label: string
}>()

const emit = defineEmits<{
  (e: "update:value", value: string): void
}>()

const showPassword = ref(false)

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}

const inputType = computed<InputTypeHTMLAttribute>(() => {
  return showPassword.value ? "text" : "password"
})

const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit("update:value", target.value)
}
</script>

<template>
  <div class="relative">
    <input
      :id="id"
      :type="inputType"
      :value="value"
      @input="handleInput"
      class="block w-full p-2 pr-10 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm min-h-[54px]"
      v-bind="$attrs"
    />

    <button
      type="button"
      class="absolute inset-y-0 right-0 px-3 flex items-center justify-center max-w-[48px]"
      @click="togglePasswordVisibility"
      :title="showPassword ? 'Hide password' : 'Show password'"
      :aria-label="showPassword ? 'Hide password' : 'Show password'"
    >
      <EyeCloseIcon
        v-if="showPassword"/>
      <EyeIcon v-else/>
    </button>
  </div>
</template>
