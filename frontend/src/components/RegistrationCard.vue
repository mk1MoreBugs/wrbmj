<script setup lang="ts">
import PasswordInput from "@/components/PasswordInput.vue"
import LoginButton from '@/components/LoginButton.vue'
import LoginInput from "@/components/LoginInput.vue"
import { useRegistrationStore } from "@/stores/registration.ts"

import type { UserRegistrationStoreModel, UserRegistrationApiModel } from "@/models/UserRegistration.ts"


const store = useRegistrationStore()

const userRegistration: UserRegistrationStoreModel = store.userRegistration

const handleSubmit = () => {
  if (store.isFormValid) {
    const userRegistrationApiModel: UserRegistrationApiModel = {
      username: store.userRegistration.username,
      plain_password: store.userRegistration.password,
      photo_file: store.userRegistration.photoFile ?? ''
    }
    store.registration(userRegistrationApiModel)
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
      <PasswordInput id="repeat-password-id" :value=userRegistration.repeatPassword :error=store.passwordError
        @update:value="store.handleRepeatPasswordInput" />

      <div class="size-3"></div>
      
      <LoginButton class="place-self-center">
        Регистрация
      </LoginButton>
    </div>
  </form>
</template>
