<script setup lang="ts">
import { useRouter } from 'vue-router'

import PasswordInput from "@/components/PasswordInput.vue"
import LoginButton from '@/components/LoginButton.vue'
import LoginInput from "@/components/LoginInput.vue"
import {useAuthStore} from "@/stores/auth"

import type { UserCredentials } from "@/models/UserCredentials.ts"

const router = useRouter()
const store = useAuthStore()

const userCredentials: UserCredentials = store.userCredentials

const handleSubmit = async () => {
  if (store.isFormValid) {
    try {
      await store.login(store.userCredentials)
      router.push('/users/me')
    } catch(error) {
      console.error('Login failed', error)
    }
  } else {
    console.log("Form is not Valid")
  }
}
</script>

<template>
  <form @submit.prevent="handleSubmit">
    <div class="w-96 flex flex-col">

      <LoginInput
        id="login-id"
        placeholder="Login"
        :value=userCredentials.username
        :error=store.loginError
        @update:value="store.handleUsernameInput"
      />
      <PasswordInput
        id="password-id"
        placeholder="Пароль"
        :value=userCredentials.password
        :error=store.passwordError
        @update:value=store.handlePasswordInput
      />

      <div class="size-3"></div>

      <LoginButton class="place-self-center">
          Login
      </LoginButton>
    </div>
  </form>
</template>
