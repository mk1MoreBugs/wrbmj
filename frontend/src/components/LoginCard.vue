<script setup lang="ts">
import { reactive } from "vue"
import type { UserCredentials } from "@/models/UserCredentials.ts"
import PasswordInput from "@/components/PasswordInput.vue"

const userCredentials = reactive<UserCredentials>({ username: "", password: "" })

const handlePasswordInput = (newValue: string) => {
  userCredentials.password = newValue;
};
</script>

<template>
  <div class="w-96 flex flex-col">
    <input 
      class="
        bg-neutral
        flex justify-between
        block m-1 min-h-[58px] h-[68px]
        rounded-field
        shadow-md/20
        overflow-hidden
        focus-within:border-neutral focus-within:outline-secondary focus-within:outline-3
      " 
      type="text"
      v-model.trim="userCredentials.username"
    />
    <PasswordInput
      id=""
      label=""
      :value=userCredentials.password
      @update:value="handlePasswordInput"
    />
  </div>

  <div class="w-96 flex flex-row">
    <p>username: {{ userCredentials.username }}</p>
    <p>password: {{ userCredentials.password }}</p>
  </div>
</template>
