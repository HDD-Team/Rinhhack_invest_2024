<template>
  <div
    class="min-h-screen flex justify-center items-center bg-gradient-to-r from-blue-500 via-indigo-500 to-green-500"
  >
    <div class="bg-white p-8 rounded-lg shadow-lg w-full max-w-md animate-fade-in">
      <h1 class="text-4xl font-extrabold text-center text-indigo-700 mb-8">
        Регистрация в CodeRPG
      </h1>

      <form @submit.prevent="handleRegister" class="space-y-5">
        <!-- Email поле -->
        <div class="mb-5">
          <label for="email" class="block text-lg font-medium text-gray-700">Email</label>
          <input
            type="email"
            id="email"
            v-model="email"
            required
            :disabled="isLoading"
            placeholder="Введите ваш email"
            @blur="validateEmail"
            class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 transition ease-in-out duration-300 disabled:bg-gray-100 disabled:cursor-not-allowed"
            :class="{ 'border-red-500': emailError }"
          />
          <p v-if="emailError" class="text-red-500 text-sm mt-1">{{ emailError }}</p>
        </div>

        <!-- Фамилия -->
        <div class="mb-5">
          <label for="last_name" class="block text-lg font-medium text-gray-700">Фамилия</label>
          <input
            type="text"
            id="last_name"
            v-model="last_name"
            required
            :disabled="isLoading"
            placeholder="Введите вашу фамилию"
            class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 transition ease-in-out duration-300 disabled:bg-gray-100 disabled:cursor-not-allowed"
          />
        </div>

        <!-- Имя -->
        <div class="mb-5">
          <label for="first_name" class="block text-lg font-medium text-gray-700">Имя</label>
          <input
            type="text"
            id="first_name"
            v-model="first_name"
            required
            :disabled="isLoading"
            placeholder="Введите ваше имя"
            class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 transition ease-in-out duration-300 disabled:bg-gray-100 disabled:cursor-not-allowed"
          />
        </div>

        <!-- Отчество -->
        <div class="mb-5">
          <label for="second_name" class="block text-lg font-medium text-gray-700">Отчество</label>
          <input
            type="text"
            id="second_name"
            v-model="second_name"
            required
            :disabled="isLoading"
            placeholder="Введите ваше отчество"
            class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 transition ease-in-out duration-300 disabled:bg-gray-100 disabled:cursor-not-allowed"
          />
        </div>

        <!-- Пароль -->
        <div class="mb-5">
          <label for="password" class="block text-lg font-medium text-gray-700">Пароль</label>
          <div class="relative">
            <input
              :type="showPassword ? 'text' : 'password'"
              id="password"
              v-model="password"
              required
              :disabled="isLoading"
              placeholder="Введите ваш пароль"
              @blur="validatePassword"
              class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 transition ease-in-out duration-300 disabled:bg-gray-100 disabled:cursor-not-allowed"
              :class="{ 'border-red-500': passwordError }"
            />
            <button
              type="button"
              @click="showPassword = !showPassword"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
            >
              <span class="sr-only">{{ showPassword ? 'Скрыть пароль' : 'Показать пароль' }}</span>
              <i class="text-xl" :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </button>
          </div>
          <p v-if="passwordError" class="text-red-500 text-sm mt-1">{{ passwordError }}</p>
        </div>

        <!-- Подтверждение пароля -->
        <div class="mb-5">
          <label for="confirmPassword" class="block text-lg font-medium text-gray-700">
            Подтверждение пароля
          </label>
          <div class="relative">
            <input
              :type="showConfirmPassword ? 'text' : 'password'"
              id="confirmPassword"
              v-model="confirmPassword"
              required
              :disabled="isLoading"
              placeholder="Подтвердите ваш пароль"
              @blur="validateConfirmPassword"
              class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 transition ease-in-out duration-300 disabled:bg-gray-100 disabled:cursor-not-allowed"
              :class="{ 'border-red-500': confirmPasswordError }"
            />
            <button
              type="button"
              @click="showConfirmPassword = !showConfirmPassword"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
            >
              <span class="sr-only">{{
                showConfirmPassword ? 'Скрыть пароль' : 'Показать пароль'
              }}</span>
              <i
                class="text-xl"
                :class="showConfirmPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"
              ></i>
            </button>
          </div>
          <p v-if="confirmPasswordError" class="text-red-500 text-sm mt-1">
            {{ confirmPasswordError }}
          </p>
        </div>

        <!-- Выбор роли -->
        <div class="mb-6">
          <label for="role" class="block text-lg font-medium text-gray-700">Роль</label>
          <select
            id="role"
            v-model="role"
            required
            :disabled="isLoading"
            class="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 transition ease-in-out duration-300 disabled:bg-gray-100 disabled:cursor-not-allowed"
          >
            <option value="child">Ребенок</option>
            <option value="teacher">Учитель</option>
            <option value="parent">Родитель</option>
          </select>
        </div>

        <!-- Поле для ввода кода подтверждения -->
        <div v-if="isRegistered" class="mb-5">
          <label for="verificationCode" class="block text-lg font-medium text-gray-700">
            Введите код подтверждения из email:
          </label>
          <div class="flex space-x-2 justify-center">
            <input
              v-for="(digit, index) in verificationCode"
              :key="index"
              v-model="verificationCode[index]"
              @input="moveToNext(index)"
              @keydown="handleKeydown($event, index)"
              maxlength="1"
              inputmode="numeric"
              type="text"
              ref="verificationCodeFields"
              :disabled="isLoading"
              :autofocus="index === 0"
              @paste="handlePaste"
              class="w-12 h-12 text-center text-xl border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 transition duration-200 disabled:bg-gray-100 disabled:cursor-not-allowed"
            />
          </div>
          <p v-if="verificationError" class="text-red-500 text-sm mt-2 text-center">
            {{ verificationError }}
          </p>
        </div>

        <!-- Кнопка регистрации -->
        <div v-if="!isRegistered" class="text-center">
          <button
            type="submit"
            :disabled="!isFormValid || isLoading"
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
            <span :class="{ invisible: isLoading }">Зарегистрироваться</span>
          </button>
        </div>
      </form>

      <!-- Кнопка подтверждения кода -->
      <div v-if="isRegistered" class="mt-5 space-y-4">
        <button
          @click="handleVerificationCode"
          :disabled="!isVerificationValid || isLoading"
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
          <span :class="{ invisible: isLoading }">Подтвердить</span>
        </button>

        <p class="text-sm text-gray-600 text-center">
          Не получили код?
          <button
            @click="resendCode"
            :disabled="isResendDisabled"
            class="text-indigo-600 hover:text-indigo-800 hover:underline disabled:text-gray-400"
          >
            Отправить повторно {{ resendTimer ? `(${resendTimer}с)` : '' }}
          </button>
        </p>
      </div>

      <p class="mt-6 text-center text-sm text-gray-600">
        Уже есть аккаунт?
        <router-link
          to="/login"
          class="text-indigo-600 hover:text-indigo-800 hover:underline transition duration-200"
        >
          Войти
        </router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const isLoading = ref(false)
const isRegistered = ref(false)
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const verificationError = ref('')
const resendTimer = ref(0)

// Данные формы
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const role = ref('child')
const userId = ref(null)
const verificationCode = ref(['', '', '', '', '', ''])
const last_name = ref('') // Фамилия
const first_name = ref('') // Имя
const second_name = ref('') // Отчество

// Ошибки валидации
const emailError = ref('')
const passwordError = ref('')
const confirmPasswordError = ref('')

// Валидация email
const validateEmail = () => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  emailError.value = emailRegex.test(email.value) ? '' : 'Неверный формат email'
}

// Валидация пароля
const validatePassword = () => {
  const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/
  passwordError.value = passwordRegex.test(password.value)
    ? ''
    : 'Пароль должен содержать минимум 8 символов, включая буквы и цифры'
}

// Валидация подтверждения пароля
const validateConfirmPassword = () => {
  confirmPasswordError.value = password.value === confirmPassword.value ? '' : 'Пароли не совпадают'
}

// Проверка валидности формы
const isFormValid = computed(() => {
  return (
    email.value &&
    password.value &&
    confirmPassword.value &&
    last_name.value &&
    first_name.value &&
    second_name.value &&
    !emailError.value &&
    !passwordError.value &&
    !confirmPasswordError.value
  )
})

// Проверка валидности кода подтверждения
const isVerificationValid = computed(() => {
  return verificationCode.value.every((digit) => /^\d$/.test(digit))
})

// Проверка возможности повторной отправки кода
const isResendDisabled = computed(() => resendTimer.value > 0)

// Таймер для повторной отправки
const startResendTimer = () => {
  resendTimer.value = 60
  const timer = setInterval(() => {
    resendTimer.value--
    if (resendTimer.value === 0) {
      clearInterval(timer)
    }
  }, 1000)
}

// Обработка регистрации
const handleRegister = async () => {
  validateEmail()
  validatePassword()
  validateConfirmPassword()

  if (!isFormValid.value) return

  isLoading.value = true
  try {
    const response = await axios.post(`${import.meta.env.VITE_API_URL}/register`, {
      login: email.value,
      password: password.value,
      role: role.value,
      last_name: last_name.value, // Передача фамилии на сервер
      first_name: first_name.value, // Передача имени на сервер
      second_name: second_name.value, // Передача отчества на сервер
    })

    userId.value = response.data.user_id
    isRegistered.value = true
    startResendTimer()
  } catch (error) {
    emailError.value = error.response?.data?.message || 'Ошибка регистрации'
  } finally {
    isLoading.value = false
  }
}

// Обработка подтверждения кода
const handleVerificationCode = async () => {
  if (!isVerificationValid.value) return

  isLoading.value = true
  try {
    const response = await axios.post(`${import.meta.env.VITE_API_URL}/register/verifi_code`, {
      id: userId.value,
      code: verificationCode.value.join(''),
    })

    if (response.data.success) {
      router.push('/login')
    } else {
      verificationError.value = 'Неверный код подтверждения'
    }
  } catch (error) {
    verificationError.value = 'Ошибка при проверке кода'
  } finally {
    isLoading.value = false
  }
}

// Повторная отправка кода
const resendCode = async () => {
  if (isResendDisabled.value) return

  isLoading.value = true
  try {
    await axios.post(`${import.meta.env.VITE_API_URL}/register/resend-code`, {
      id: userId.value,
    })
    startResendTimer()
  } catch (error) {
    verificationError.value = 'Ошибка при отправке кода'
  } finally {
    isLoading.value = false
  }
}

// Обработка вставки кода
const handlePaste = (event) => {
  event.preventDefault()
  const pasteData = event.clipboardData.getData('text').replace(/\D/g, '').slice(0, 6)

  verificationCode.value = Array.from(pasteData.padEnd(6, ''))
}

// Обработка ввода кода
const moveToNext = (index) => {
  if (verificationCode.value[index].length === 1 && index < 5) {
    document.querySelector(`input[data-index="${index + 1}"]`)?.focus()
  }
}

// Обработка клавиш при вводе кода
const handleKeydown = (event, index) => {
  if (event.key === 'Backspace' && !verificationCode.value[index] && index > 0) {
    document.querySelector(`input[data-index="${index - 1}"]`)?.focus()
  }
}

// Отслеживание изменений пароля
watch(password, () => {
  validatePassword()
  if (confirmPassword.value) {
    validateConfirmPassword()
  }
})

watch(confirmPassword, validateConfirmPassword)
</script>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.3s ease-out;
}
</style>
