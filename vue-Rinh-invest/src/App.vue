<template>
  <div>
    <!-- Показываем Header только если не на странице логина -->
    <Header v-if="!isLoginPage" @logout="handleLogout" />

    <!-- Контент страницы -->
    <router-view />
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue' // Добавили импорт watch
import { useRoute } from 'vue-router' // Импортируем useRoute для получения информации о текущем маршруте
import Header from './components/common/Header.vue'

export default {
  name: 'App',
  components: {
    Header,
  },
  setup() {
    const user = ref(null)
    const route = useRoute() // Получаем информацию о текущем маршруте
    const isLoginPage = ref(false)

    // Функция для загрузки данных пользователя
    const loadUser = () => {
      const storedUser = JSON.parse(localStorage.getItem('user'))
      if (storedUser) {
        user.value = storedUser
      }
    }

    // Проверка, если текущий маршрут - это страница логина
    onMounted(() => {
      loadUser() // Загружаем данные при монтировании компонента
      isLoginPage.value = route.name === 'login' // Сравниваем имя текущего маршрута с 'login'
    })

    // Следим за изменением маршрута
    watch(route, (newRoute) => {
      isLoginPage.value = newRoute.name === 'login'
    })

    // Обработчик для выхода
    const handleLogout = () => {
      localStorage.removeItem('user')
      user.value = null
      // Можно перенаправить на страницу логина
      this.$router.push('/login')
    }

    return {
      user,
      handleLogout,
      isLoginPage,
    }
  },
}
</script>
