<template>
  <div class="max-w-4xl mx-auto p-8">
    <h1 class="text-3xl font-bold text-indigo-700 mb-4">Профиль родителя</h1>

    <div class="bg-white rounded-lg shadow-lg p-6 mb-6">
      <h2 class="text-xl font-semibold mb-4">Информация о родителе</h2>
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700">Имя</label>
        <input
          v-model="user.name"
          type="text"
          placeholder="Введите имя"
          class="mt-1 block w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
      </div>
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700">Фамилия</label>
        <input
          v-model="user.lastName"
          type="text"
          placeholder="Введите фамилию"
          class="mt-1 block w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
      </div>
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700">Email</label>
        <input
          v-model="user.email"
          type="email"
          placeholder="Введите email"
          class="mt-1 block w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
      </div>
    </div>

    <div class="bg-white rounded-lg shadow-lg p-6">
      <h2 class="text-xl font-semibold mb-4">Информация о ребенке</h2>
      <p v-if="child.name && child.class">
        <strong>Ребенок:</strong> {{ child.name }}<br />
        <strong>Класс:</strong> {{ child.class }}<br />
        <strong>Учитель:</strong> {{ child.teacher }}
      </p>
      <p v-else>Данных о ребенке нет.</p>

      <div class="mt-4">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Поиск ребенка..."
          class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
        <button
          @click="addChild"
          class="mt-2 bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition duration-300"
        >
          Добавить ребенка
        </button>
      </div>
    </div>

    <!-- Модальное окно добавления ребенка -->
    <div
      v-if="isModalOpen"
      class="fixed inset-0 flex items-center justify-center z-50"
      @click.self="closeAddChildModal"
    >
      <div class="absolute inset-0 bg-black bg-opacity-50 backdrop-blur-sm"></div>
      <div class="relative bg-white rounded-2xl shadow-2xl w-96 p-6">
        <h2 class="text-2xl font-bold text-indigo-700 text-center mb-4">Добавить ребенка</h2>
        <input
          v-model="newChildName"
          type="text"
          placeholder="Имя ребенка"
          class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 mb-4"
        />
        <input
          v-model="newChildClass"
          type="text"
          placeholder="Класс ребенка"
          class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 mb-4"
        />
        <input
          v-model="newChildTeacher"
          type="text"
          placeholder="Учитель ребенка"
          class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 mb-4"
        />
        <div class="flex justify-end mt-4">
          <button
            @click="saveChild"
            class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition duration-300"
          >
            Сохранить
          </button>
          <button
            @click="closeAddChildModal"
            class="ml-2 px-4 py-2 bg-gray-300 text-black rounded-lg hover:bg-gray-400"
          >
            Отменить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ParentProfile',
  data() {
    return {
      user: JSON.parse(localStorage.getItem('user')) || {
        name: 'Родитель',
        lastName: '',
        email: 'parent@example.com',
      },
      child: { name: '', class: '', teacher: '' }, // Данные о ребенке
      searchQuery: '',
      isModalOpen: false,
      newChildName: '',
      newChildClass: '',
      newChildTeacher: '',
    }
  },
  methods: {
    addChild() {
      this.isModalOpen = true
    },
    closeAddChildModal() {
      this.isModalOpen = false
      this.newChildName = ''
      this.newChildClass = ''
      this.newChildTeacher = ''
    },
    saveChild() {
      if (this.newChildName.trim() && this.newChildClass.trim() && this.newChildTeacher.trim()) {
        this.child = {
          name: this.newChildName.trim(),
          class: this.newChildClass.trim(),
          teacher: this.newChildTeacher.trim(),
        }
        this.closeAddChildModal()
        alert(`Ребенок ${this.child.name} добавлен.`)
      } else {
        alert('Пожалуйста, заполните все поля.')
      }
    },
  },
}
</script>

<style scoped>
/* Анимации */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.animate-fadeIn {
  animation: fadeIn 0.5s ease-in-out;
}

/* Кастомный скроллбар */
.custom-scrollbar::-webkit-scrollbar {
  width: 8px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}
</style>
