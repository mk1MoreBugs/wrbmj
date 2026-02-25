<script setup lang="ts">
import { ref, computed } from "vue"
import type { InputTypeHTMLAttribute } from "vue"
import EyeIcon from '@/assets/icons/eye.vue'
import EyeIconClose from '@/assets/icons/eye-close.vue'

interface InputProps {
  id: string
  value: string
  label: string
  type?: InputTypeHTMLAttribute
  error?: string
  placeholder?: string
}

const props = withDefaults(defineProps<InputProps>(),
  {type: 'text'}
)

const emit = defineEmits<{
  (e: "update:value", value: string): void
}>()

const showPassword = ref(false)
const isPasswordField = props.type === 'password'

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}

const inputType = computed<InputTypeHTMLAttribute>(() => {
  if (!isPasswordField) return props.type
  return showPassword.value ? "text" : "password"
})

const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit("update:value", target.value)
}

const conainerDivClasses = computed(() => [
   'bg-neutral',
    'flex justify-between',
    'm-1 min-h-[58px] h-[68px]',
    'rounded-field',
    'shadow-md/20',
    'overflow-hidden',
    (props.error ? 'outline-error ' : 'focus-within:outline-secondary focus-within:') + 'outline-3'
])
</script>

<template>
  <div :class="conainerDivClasses">
    <input
      :placeholder="placeholder"
      :id="id"
      :type="inputType"
      :value="value"
      @input="handleInput"
      class="
        grow
        outline-none
        font-sans text-body text-white
        px-3
      "
      v-bind="$attrs"
    />

    <button
      v-if="isPasswordField"
      type="button"
      class="m-2 flex items-center size-[48px]"
      @click="togglePasswordVisibility"
      :title="showPassword ? 'Hide password' : 'Show password'"
      :aria-label="showPassword ? 'Hide password' : 'Show password'"
    >
      <EyeIconClose class="size-fit fill-white" v-if="showPassword"/>
      <EyeIcon class="size-fit fill-white"  v-else/>
    </button>
  </div>
</template>
