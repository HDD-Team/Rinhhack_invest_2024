<template>
  <div class="max-w-4xl mx-auto p-8">
    <!-- Основная карточка профиля -->
    <div class="bg-white rounded-2xl shadow-xl overflow-hidden">
      <div class="h-32 bg-gradient-to-r from-indigo-500 to-purple-500 relative">
        <h1 class="text-3xl font-extrabold text-white text-center pt-6">Профиль учителя</h1>
      </div>

      <div class="p-6" v-if="user">
        <div class="text-center mb-6">
          <h2 class="text-2xl font-bold text-gray-800">
            {{ user.first_name }} {{ user.last_name }} {{ user.second_name }}
          </h2>
          <p class="text-indigo-600 font-medium mt-1">{{ user.email }}</p>
        </div>

        <div class="flex justify-center space-x-4 mb-4">
          <!-- Кнопка редактирования -->
          <button
            @click="openEditModal"
            class="flex items-center px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl hover:from-indigo-700 hover:to-purple-700 transform hover:scale-105 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
          >
            <i class="fas fa-edit mr-2"></i>
            Редактировать ФИО
          </button>

          <!-- Кнопка настройки безопасности -->
          <router-link
            to="/settings/security"
            class="flex items-center px-6 py-3 bg-gradient-to-r from-green-600 to-blue-600 text-white rounded-xl hover:from-green-700 hover:to-blue-700 transform hover:scale-105 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
          >
            <i class="fas fa-cog mr-2"></i>
            Настройки безопасности
          </router-link>
        </div>
      </div>
    </div>

    <!-- Модальное окно редактирования -->
    <div
      v-if="isModalOpen"
      class="fixed inset-0 flex items-center justify-center z-50"
      @click.self="closeEditModal"
    >
      <div class="absolute inset-0 bg-black bg-opacity-50 backdrop-blur-sm"></div>
      <div
        class="relative bg-white rounded-2xl shadow-2xl w-96 p-6 transform transition-all duration-300 scale-100"
      >
        <h2
          class="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600 text-center mb-6"
        >
          Редактирование профиля
        </h2>

        <div class="space-y-4">
          <label class="block">
            <span class="text-sm font-medium text-gray-700">Имя</span>
            <input
              v-model="editedUser.first_name"
              type="text"
              class="mt-1 block w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all duration-300"
              placeholder="Введите имя"
            />
          </label>
          <label class="block">
            <span class="text-sm font-medium text-gray-700">Фамилия</span>
            <input
              v-model="editedUser.last_name"
              type="text"
              class="mt-1 block w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all duration-300"
              placeholder="Введите фамилию"
            />
          </label>
        </div>

        <div class="flex justify-end mt-6 space-x-3">
          <button
            @click="closeEditModal"
            class="px-4 py-2 text-gray-700 bg-gray-200 rounded-xl hover:bg-gray-300 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-gray-500"
          >
            Отменить
          </button>
          <button
            @click="saveProfile"
            class="px-4 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl hover:from-indigo-700 hover:to-purple-700 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
          >
            Сохранить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TeacherProfile',
  data() {
    return {
      user: null, // Начальная инициализация как null
      isModalOpen: false,
      editedUser: {
        first_name: '',
        last_name: '',
      },
    }
  },
  mounted() {
    this.fetchUserData() // Загрузка данных с сервера при монтировании компонента
  },
  methods: {
    async fetchUserData() {
      try {
        const userId = JSON.parse(localStorage.getItem('user')).id // Получаем ID пользователя из localStorage

        // Отправляем POST-запрос, но ID передаем через query string в URL
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/teacher?teacher_id=${userId}`,
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json', // Указываем, что отправляем JSON
            },
          },
        )

        const data = await response.json() // Ожидаем ответ от сервера

        if (data.success) {
          this.user = data.message // Получаем данные пользователя
          this.editedUser.first_name = this.user.first_name // Заполняем форму редактирования
          this.editedUser.last_name = this.user.last_name
        } else {
          alert('Не удалось загрузить данные пользователя')
        }
      } catch (error) {
        console.error('Ошибка при загрузке данных пользователя:', error) // Логируем ошибку
        alert('Ошибка при загрузке данных')
      }
    },
    openEditModal() {
      this.editedUser.first_name = this.user.first_name
      this.editedUser.last_name = this.user.last_name || ''
      this.isModalOpen = true
    },
    closeEditModal() {
      this.isModalOpen = false
      this.editedUser = { first_name: '', last_name: '' }
    },
    async saveProfile() {
      try {
        const updatedUser = {
          ...this.user,
          first_name: this.editedUser.first_name,
          last_name: this.editedUser.last_name,
        }

        // Отправка POST-запроса на сервер
        const userId = JSON.parse(localStorage.getItem('user')).id
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/teacher?teacher_id=${userId}`,
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedUser),
          },
        )

        if (!response.ok) {
          throw new Error('Ошибка при сохранении профиля')
        }

        this.user = updatedUser // Обновляем локально
        this.closeEditModal()
        alert('Профиль успешно обновлен!')
      } catch (error) {
        console.error('Ошибка сохранения профиля:', error)
        alert('Ошибка при сохранении изменений.')
      }
    },
  },
}
</script>
