<script setup lang="ts">
import { reactive } from "vue"
import type { UserCredentials } from "@/models/UserCredentials.ts"
const userCredentials = reactive<UserCredentials>({ username: "", password: "" })
</script>

<template>
  <div class="w-96 flex flex-col">
    <input class="border-2 border-solid" type="text" v-model="userCredentials.username" />
    <input class="border-2 border-solid" type="password" v-model="userCredentials.password" /> <!--Replace with a separate component -->
  </div>

  <div class="w-96 flex flex-row">
    <p>username: {{ userCredentials.username }}</p>
    <p>password: {{ userCredentials.password }}</p>
  </div>
</template>
