<template>
  <div
    class="min-h-screen flex flex-col items-center justify-center bg-gradient-to-r from-blue-500 via-indigo-500 to-green-500 text-white"
  >
    <h1 class="text-6xl font-extrabold text-center mb-6 animate__animated animate__fadeIn">404</h1>
    <p class="text-2xl text-center mb-4 animate__animated animate__fadeIn animate__delay-1s">
      Страницу украли :(
    </p>
    <p class="text-lg text-center animate__animated animate__fadeIn animate__delay-2s">
      Извините, но мы не можем найти запрашиваемую страницу. Вы можете
      <button @click="goBack" class="underline hover:text-indigo-300 focus:outline-none">
        вернуться назад</button
      >.
    </p>
  </div>
</template>

<script>
export default {
  name: 'NotFound',
  methods: {
    goBack() {
      // Возвращаемся на предыдущую страницу
      this.$router.go(-1)
    },
  },
}
</script>

<style scoped>
/* Используем анимацию для плавных переходов */
@import 'https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css';

/* Стиль для текста 404 */
h1 {
  font-family: 'Poppins', sans-serif;
  font-weight: 800;
  color: #fbd38d;
}

/* Стиль для параграфов */
p {
  font-family: 'Inter', sans-serif;
}

/* Стиль кнопки для возврата */
button {
  background: none;
  border: none;
  color: #44ff00;
  font-size: inherit;
  cursor: pointer;
  padding: 0;
  text-decoration: none;
}

button:hover {
  color: #585c60;
}

button:focus {
  outline: none;
}
</style>
