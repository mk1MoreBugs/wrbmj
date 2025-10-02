<script setup lang="ts">
import PasswordInput from "@/components/PasswordInput.vue"
import {useAuthStore} from "@/stores/auth"

import type { UserCredentials } from "@/models/UserCredentials.ts"


const store = useAuthStore()

const userCredentials: UserCredentials = store.userCredentials

const handleSubmit = () => {
  store.login()
}

</script>

<template>
  <form @submit.prevent="handleSubmit">
    <div class="w-96 flex flex-col">
      <input class="
        bg-neutral
        flex justify-between
        m-1 min-h-[58px] h-[68px]
        rounded-field
        shadow-md/20
        overflow-hidden
        focus-within:border-neutral focus-within:outline-secondary focus-within:outline-3
      " type="text" v-model.trim="userCredentials.username" />

      <PasswordInput id="" label="" :value=userCredentials.password @update:value="store.handlePasswordInput" />

      <button
        type="submit"
        :disabled="!store.isFormValid"
      >
        {{ store.isFormValid ? 'Login' : 'Form is inValid' }}
    </button>
    </div>
  </form>

  <div class="w-96 flex flex-row">
    <p>username: {{ userCredentials.username }}</p>
    <p>password: {{ userCredentials.password }}</p>
  </div>
</template>
