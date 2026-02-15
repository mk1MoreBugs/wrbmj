<script setup lang="ts">
import PasswordInput from "@/components/PasswordInput.vue"
import LoginButton from '@/components/LoginButton.vue'
import LoginInput from "@/components/LoginInput.vue"
import { useRegistrationStore } from "@/stores/registration.ts"

import type { UserRegistration } from "@/models/UserRegistration.ts"


const store = useRegistrationStore()

const userRegistration: UserRegistration = store.userRegistration

const handleSubmit = () => {
  if (store.isFormValid) {
    store.registration(store.userRegistration)
  } else {
    console.log("Form is not Valid")
  }
}
</script>

<template>
  <form @submit.prevent="handleSubmit">
    <div class="w-96 flex flex-col">

      <LoginInput id="login-id" :value=userRegistration.username :error=store.loginError
        @update:value="store.handleUsernameInput" />
      <PasswordInput id="password-id" :value=userRegistration.password :error=store.passwordError
        @update:value="store.handlePasswordInput" />

      <LoginButton class="place-self-center">
        Login
      </LoginButton>
    </div>
  </form>
</template>
