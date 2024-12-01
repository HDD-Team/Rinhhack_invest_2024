<template>
  <div
    class="min-h-screen flex justify-center items-center bg-gradient-to-r from-blue-500 via-indigo-500 to-green-500"
  >
    <div class="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
      <h1 class="text-4xl font-extrabold text-center text-indigo-700 mb-8">Вход в CodeRPG</h1>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div class="mb-5">
          <label for="email" class="block text-lg font-medium text-gray-700">Email</label>
          <input
            type="email"
            id="email"
            v-model="formData.email"
            required
            :disabled="isLoading"
            placeholder="Введите ваш email"
            class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 transition ease-in-out duration-300 disabled:bg-gray-100 disabled:cursor-not-allowed"
            @blur="validateEmail"
          />
          <p v-if="errors.email" class="mt-1 text-sm text-red-500">{{ errors.email }}</p>
        </div>

        <div class="mb-6">
          <label for="password" class="block text-lg font-medium text-gray-700">Пароль</label>
          <input
            type="password"
            id="password"
            v-model="formData.password"
            required
            :disabled="isLoading"
            placeholder="Введите ваш пароль"
            class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 transition ease-in-out duration-300 disabled:bg-gray-100 disabled:cursor-not-allowed"
            @blur="validatePassword"
          />
          <p v-if="errors.password" class="mt-1 text-sm text-red-500">{{ errors.password }}</p>
        </div>

        <div
          v-if="errorMessage"
          class="p-3 rounded bg-red-50 border border-red-200 text-red-600 text-center mb-4"
        >
          {{ errorMessage }}
        </div>

        <button
          type="submit"
          :disabled="isLoading || !isFormValid"
          class="relative w-full px-6 py-3 rounded-full text-white text-lg font-medium bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-300 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          <span
            v-if="isLoading"
            class="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2"
          >
            <svg class="animate-spin h-5 w-5" viewBox="0 0 24 24">
              <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
                fill="none"
              />
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
          </span>
          <span :class="{ invisible: isLoading }">Войти</span>
        </button>
      </form>

      <div class="mt-6 space-y-2">
        <p class="text-center text-sm text-gray-600">
          Нет аккаунта?
          <router-link
            to="/register"
            class="text-indigo-600 hover:text-indigo-800 hover:underline transition duration-200"
          >
            Регистрация
          </router-link>
        </p>

        <p class="text-center text-sm text-gray-600">
          <router-link
            to="/forgot-password"
            class="text-indigo-600 hover:text-indigo-800 hover:underline transition duration-200"
          >
            Забыли пароль?
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const isLoading = ref(false)
const errorMessage = ref('')

const formData = ref({
  email: '',
  password: '',
})

const errors = ref({
  email: '',
  password: '',
})

const validateEmail = () => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  errors.value.email = !emailRegex.test(formData.value.email)
    ? 'Пожалуйста, введите корректный email'
    : ''
}

const validatePassword = () => {
  errors.value.password =
    formData.value.password.length < 6 ? 'Пароль должен содержать минимум 6 символов' : ''
}

const isFormValid = computed(() => {
  return (
    formData.value.email && formData.value.password && !errors.value.email && !errors.value.password
  )
})

const handleLogin = async () => {
  if (!isFormValid.value) return

  isLoading.value = true
  errorMessage.value = ''

  try {
    const response = await axios.post(`${import.meta.env.VITE_API_URL}/token`, null, {
      params: {
        login: formData.value.email,
        password: formData.value.password,
      },
    })

    if (response.data?.success) {
      const { id, role } = response.data
      // Сохраняем данные в localStorage
      const userData = { id, role }
      localStorage.setItem('user', JSON.stringify(userData))

      // Выводим в консоль, чтобы проверить сохранение
      console.log('User data saved to localStorage:', userData)

      const routes = {
        child: `/character`,
        teacher: `/teacher/profile`,
        parent: `/statistics`,
        admin: `/admin/courses`,
      }

      await router.push(routes[role] || '/')
    } else {
      errorMessage.value = 'Неверные email или пароль'
    }
  } catch (error) {
    console.error('Ошибка при входе:', error)
    errorMessage.value =
      error.response?.data?.message || 'Произошла ошибка при входе. Пожалуйста, попробуйте позже.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.min-h-screen {
  background: linear-gradient(to right, #4f46e5, #9333ea, #10b981);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.bg-white {
  animation: fadeIn 0.3s ease-out;
}
</style>
