<script setup lang="ts">
import LoginCard from "@/components/LoginCard.vue"
</script>

<template>
  <div
    class="text-caption"
  >
    <router-link
      to="/registration"
      class="
      text-info hover:text-accent
        underline
        hover:underline-offset-2
      "
    >
      Регистрация
    </router-link>

    <LoginCard/>
  </div>
</template>
