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
      class="block w-full p-2 pr-10 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm min-h-[54px]" 
      type="text"
      v-model.trim="userCredentials.username" />
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
