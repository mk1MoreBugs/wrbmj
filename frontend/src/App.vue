<script setup lang="ts">
</script>

<template>
    <div class="min-h-screen bg-base-100 font-sans text-body text-white">
    <header class="bg-gray-800 p-4 shadow">
      <nav class="container mx-auto flex justify-between items-center">
        <router-link to="/" class="text-xl font-bold">MyApp</router-link>
        <div class="space-x-4">
          <router-link to="/login" class="hover:text-blue-300">Войти</router-link>
        </div>
      </nav>
    </header>

    <main class="container mx-auto p-4">
      <router-view/>
    </main>
  </div>
</template>

<style scoped></style>
