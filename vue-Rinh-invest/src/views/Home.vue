<template>
  <div
    class="min-h-screen flex flex-col items-center justify-center bg-gradient-to-r from-blue-400 via-indigo-400 to-green-400"
  >
    <h1 class="text-4xl font-extrabold text-center text-indigo-700 mb-6">
      🌟 Добро пожаловать в CodeQuest 🌟
    </h1>
    <p class="text-lg text-gray-700 mb-6 text-center">
      Присоединяйтесь к нам, чтобы начать увлекательное путешествие в мир программирования!
    </p>
    <div class="flex space-x-4">
      <router-link
        to="/login"
        class="bg-indigo-700 text-white px-6 py-2 rounded-full hover:bg-indigo-800 focus:outline-none"
      >
        Войти
      </router-link>
      <router-link
        to="/register"
        class="bg-green-700 text-white px-6 py-2 rounded-full hover:bg-green-800 focus:outline-none"
      >
        Регистрация
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
}
</script>

<style scoped>
/* Стили для главной страницы */
</style>
