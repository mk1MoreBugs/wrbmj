<script setup lang="ts">
import { useRouter } from 'vue-router'

import PasswordInput from "@/components/PasswordInput.vue"
import LoginButton from '@/components/LoginButton.vue'
import LoginInput from "@/components/LoginInput.vue"
import { useRegistrationStore } from "@/stores/registration.ts"

import type { UserRegistrationStoreModel, UserRegistrationApiModel } from "@/models/UserRegistration.ts"

const router = useRouter()
const store = useRegistrationStore()

const userRegistration: UserRegistrationStoreModel = store.userRegistration

const handleSubmit = async () => {
  if (store.isFormValid) {
    const userRegistrationApiModel: UserRegistrationApiModel = {
      username: store.userRegistration.username,
      plain_password: store.userRegistration.password,
      photo_file: store.userRegistration.photoFile ?? ''
    }
    try {
      await store.registration(userRegistrationApiModel)
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
        :value=userRegistration.username
        :error=store.loginError
        @update:value="store.handleUsernameInput"
      />
      <PasswordInput
        id="password-id"
        placeholder="Пароль"
        :value=userRegistration.password
        :error=store.passwordError
        @update:value=store.handlePasswordInput
      />
      <PasswordInput
        id="repeat-password-id"
        placeholder="Повторите пароль"
        :value=userRegistration.repeatPassword
        :error=store.passwordError
        @update:value=store.handleRepeatPasswordInput
      />

      <div class="size-3"></div>

      <LoginButton class="place-self-center">
        Регистрация
      </LoginButton>
    </div>
  </form>
</template>
