<template>
  <header
    class="bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-700 text-white shadow-xl"
  >
    <div class="container mx-auto px-4 py-3">
      <div class="flex justify-between items-center">
        <!-- Логотип -->
        <div class="flex items-center space-x-2">
          <router-link to="/" class="flex items-center space-x-2 group">
            <div
              class="w-10 h-10 bg-white rounded-lg flex items-center justify-center transform group-hover:rotate-6 transition-all duration-300"
            >
              <span
                class="text-2xl font-bold bg-gradient-to-br from-indigo-600 to-purple-600 bg-clip-text text-transparent"
                >C</span
              >
            </div>
            <span
              class="text-2xl font-bold tracking-tight group-hover:text-indigo-200 transition-colors"
              >odeRPG</span
            >
          </router-link>
        </div>

        <!-- Навигационное меню -->
        <nav class="hidden md:block">
          <ul class="flex items-center space-x-1">
            <!-- Для ребенка -->
            <template v-if="role === 'child'">
              <li>
                <router-link to="/character" class="nav-link group">Персонаж</router-link>
              </li>
              <li>
                <router-link to="/courses" class="nav-link group">Курсы</router-link>
              </li>
            </template>

            <!-- Для учителя -->
            <template v-if="role === 'teacher'">
              <li>
                <router-link to="/teacher/profile" class="nav-link group">Профиль</router-link>
              </li>
              <li>
                <router-link to="/teacher/classes" class="nav-link group">Классы</router-link>
              </li>
              <li>
                <router-link to="/teacher/statistics" class="nav-link group"
                  >Статистика</router-link
                >
              </li>
              <li>
                <router-link to="/teacher/courses" class="nav-link group">Курсы</router-link>
              </li>
            </template>

            <!-- Для родителя -->
            <template v-if="role === 'parent'">
              <li>
                <router-link to="/parent/profile" class="nav-link group"
                  >Профиль родителя</router-link
                >
              </li>
              <li>
                <router-link to="/parent/statistics" class="nav-link group"
                  >Статистика ребенка</router-link
                >
              </li>
            </template>

            <!-- Для администратора -->
            <template v-if="role === 'admin'">
              <li>
                <router-link to="/create-course" class="nav-link group">Создать курс</router-link>
              </li>
            </template>
          </ul>
        </nav>

        <!-- Кнопка выхода -->
        <button
          v-if="role"
          @click="logout"
          class="flex items-center px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg transform hover:scale-105 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 focus:ring-offset-indigo-700 shadow-lg"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
            />
          </svg>
          <span>Выйти</span>
        </button>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'Header',
  data() {
    return {
      role: null,
    }
  },
  created() {
    this.setRole()
  },
  watch: {
    $route: 'setRole',
  },
  methods: {
    setRole() {
      const user = JSON.parse(localStorage.getItem('user'))
      this.role = user ? user.role : null
    },
    logout() {
      localStorage.removeItem('user')
      this.setRole()
      this.$router.push('/login') // Изменено с '/home' на '/login'
    },
  },
}
</script>

<style scoped>
.nav-link {
  @apply flex items-center px-4 py-2 rounded-lg text-white/90 hover:text-white
    hover:bg-white/10 transition-all duration-300;
}

.nav-link.router-link-active {
  @apply bg-white/20 text-white;
}

/* Мобильная версия */
@media (max-width: 768px) {
  .container {
    @apply flex-col items-start space-y-4;
  }

  nav {
    @apply w-full;
  }

  nav ul {
    @apply flex-col space-y-2 w-full;
  }

  .nav-link {
    @apply w-full justify-start;
  }

  button {
    @apply w-full justify-center;
  }
}
</style>
