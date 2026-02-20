<script setup lang="ts">
import RegistrationCard from '@/components/RegistrationCard.vue';

</script>

<template>
  <div class="flex flex-col">
    <div class="flex gap-2 text-caption">
      <p
        class="text-white"
      >
        Уже есть аккаунт?
      </p>

      <router-link
        to="/login"
        class="
        text-info hover:text-accent
          underline
          hover:underline-offset-2
        "
      >
        Войти
      </router-link>
    </div>
  </div>

  <div class="size-5"></div>

  <div class="flex flex-col items-center">
      <h1 class="text-h1">Регистрация</h1>
      <div class="size-3"></div>
       <RegistrationCard/>
  </div>

</template>
