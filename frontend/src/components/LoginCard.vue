<script setup lang="ts">
import PasswordInput from "@/components/PasswordInput.vue"
import LoginInput from "@/components/LoginInput.vue"
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
      
      <LoginInput id="login-id" :value=userCredentials.username :error=store.loginError @update:value="store.handleUsernameInput" />
      <PasswordInput id="password-id" :value=userCredentials.password :error=store.passwordError @update:value="store.handlePasswordInput" />

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
