<template>
  <div class="max-w-4xl mx-auto p-8">
    <!-- Основная карточка -->
    <div class="bg-white rounded-2xl shadow-xl overflow-hidden">
      <!-- Градиентный баннер -->
      <div class="h-32 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 relative">
        <h1 class="text-3xl font-extrabold text-white text-center pt-6">Ваш персонаж</h1>
        <!-- Аватар -->
        <div class="absolute left-1/2 transform -translate-x-1/2 translate-y-1/2 bottom-0">
          <div class="p-1 rounded-full bg-white shadow-lg">
            <div v-if="user?.avatar" class="w-24 h-24 rounded-full overflow-hidden">
              <img :src="user.avatar" alt="User Avatar" class="w-full h-full object-cover" />
            </div>
            <div
              v-else
              class="w-24 h-24 rounded-full bg-gradient-to-r from-indigo-400 to-purple-400 flex items-center justify-center"
            >
              <svg
                class="w-12 h-12 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Информация о пользователе -->
      <div class="pt-16 px-8 pb-8">
        <div class="text-center mb-8">
          <h2 class="text-2xl font-bold text-gray-800">
            {{ user?.child_first_name }} {{ user?.child_last_name }}
          </h2>
          <p class="text-indigo-600 font-medium mt-1">
            {{ user?.class_number || 'Класс не указан' }}
          </p>
        </div>

        <!-- Информация о преподавателе и родителе -->
        <div class="space-y-6 bg-gray-50 rounded-xl p-6">
          <h3
            class="text-xl font-semibold text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600"
          >
            Преподаватель и Родитель
          </h3>

          <div class="space-y-4">
            <!-- Преподаватель -->
            <div class="flex items-center space-x-4 p-4 bg-white rounded-lg shadow-sm">
              <div class="p-2 bg-indigo-100 rounded-lg">
                <img
                  width="32"
                  height="32"
                  src="https://img.icons8.com/windows/32/tuition.png"
                  alt="tuition"
                />
              </div>
              <div>
                <p class="text-sm text-gray-500">Преподаватель</p>
                <p class="font-medium text-gray-800">
                  {{ user?.teacher_first_name || 'Не указано' }}
                  {{ user?.teacher_last_name || 'Не указано' }}
                </p>
              </div>
            </div>

            <!-- Родитель -->
            <div class="flex items-center space-x-4 p-4 bg-white rounded-lg shadow-sm">
              <div class="p-2 bg-purple-100 rounded-lg">
                <svg
                  class="w-6 h-6 text-purple-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
                  />
                </svg>
              </div>
              <div>
                <p class="text-sm text-gray-500">Родитель</p>
                <p class="font-medium text-gray-800">
                  {{ user?.parent_first_name || 'Не указано' }}
                  {{ user?.parent_last_name || 'Не указано' }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Кнопка редактирования -->
        <div class="flex justify-center mt-8">
          <button
            @click="openEditModal"
            class="px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl hover:from-indigo-700 hover:to-purple-700 transform hover:scale-105 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Редактировать персонажа
          </button>
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
        class="relative bg-white rounded-2xl shadow-2xl w-96 transform transition-all duration-300 scale-100"
      >
        <div class="p-6">
          <h2
            class="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600 text-center mb-6"
          >
            Редактирование персонажа
          </h2>

          <div class="space-y-4">
            <label class="block">
              <span class="text-sm font-medium text-gray-700">Имя</span>
              <input
                v-model="editedUser.child_first_name"
                type="text"
                class="mt-1 block w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all duration-300"
                placeholder="Введите имя"
              />
            </label>
            <label class="block">
              <span class="text-sm font-medium text-gray-700">Фамилия</span>
              <input
                v-model="editedUser.child_last_name"
                type="text"
                class="mt-1 block w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all duration-300"
                placeholder="Введите фамилию"
              />
            </label>
          </div>

          <div class="flex justify-end mt-6 space-x-3">
            <button
              @click="closeEditModal"
              class="px-4 py-2 text-gray-700 bg-gray-100 rounded-xl hover:bg-gray-200 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
            >
              Отменить
            </button>
            <button
              @click="saveProfile"
              class="px-4 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl hover:from-indigo-700 hover:to-purple-700 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Сохранить
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Character',
  data() {
    return {
      user: null,
      isModalOpen: false,
      editedUser: {
        child_first_name: '',
        child_last_name: '',
      },
    }
  },
  methods: {
    async loadUserData() {
      const userData = JSON.parse(localStorage.getItem('user'))

      if (userData?.id) {
        try {
          const response = await fetch(`${import.meta.env.VITE_API_URL}/child?id=${userData.id}`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id: userData.id }),
          })

          if (response.ok) {
            const data = await response.json()
            if (data.success) {
              this.user = data.message
            } else {
              console.error('Ошибка в ответе от сервера:', data.message)
            }
          } else {
            console.error('Ошибка при отправке запроса:', response.statusText)
          }
        } catch (error) {
          console.error('Ошибка загрузки данных пользователя:', error)
        }
      } else {
        console.error('Не удалось найти id в localStorage.')
      }
    },

    openEditModal() {
      this.editedUser = {
        child_first_name: this.user?.child_first_name || '',
        child_last_name: this.user?.child_last_name || '',
      }
      this.isModalOpen = true
    },

    closeEditModal() {
      this.isModalOpen = false
      this.editedUser = {
        child_first_name: '',
        child_last_name: '',
      }
    },

    async saveProfile() {
      const userData = JSON.parse(localStorage.getItem('user'))
      const updatedUser = {
        id: userData?.id, // Достаем id из локального хранилища
        child_first_name: this.editedUser.child_first_name,
        child_last_name: this.editedUser.child_last_name,
      }

      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL}/child/edit`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(updatedUser),
        })

        if (response.ok) {
          const data = await response.json()
          if (data.success) {
            this.user = updatedUser
            this.closeEditModal()
          } else {
            alert('Ошибка при обновлении имени.')
          }
        }
      } catch (error) {
        console.error('Ошибка сохранения профиля:', error)
        alert('Ошибка при сохранении изменений.')
      }
    },
  },
  created() {
    this.loadUserData()
  },
}
</script>

<style scoped>
/* Добавляем плавную анимацию для всех transition эффектов */
* {
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

/* Анимация для модального окна */
.scale-100 {
  animation: modalAppear 0.3s ease-out;
}

@keyframes modalAppear {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
