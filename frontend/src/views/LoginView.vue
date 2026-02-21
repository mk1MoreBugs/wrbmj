<script setup lang="ts">
import LoginCard from "@/components/LoginCard.vue"
</script>

<template>
  <div
    class="text-caption"
  >
    <div class="size-5"></div>

    <div class="flex flex-col items-center">
      <div
        class="
          flex space-x-4
          items-center
          text-h1
        "
      >
        <h1>Войти</h1>
        <p>/</p>
        <router-link
          to="/registration"
          class="
          text-info hover:text-accent
            underline
            hover:underline-offset-2
            text-h3
          "
        >
          Регистрация
        </router-link>
      </div>

      <div class="size-3"></div>

      <LoginCard/>
    </div>
  </div>
</template>
