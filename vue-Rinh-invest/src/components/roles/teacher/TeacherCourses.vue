<template>
  <div class="max-w-4xl mx-auto p-8">
    <h1 class="text-3xl font-bold text-indigo-700 mb-4">Курсы учителя</h1>
    <p class="mb-6">Здесь вы можете управлять курсами, которые вы ведете.</p>

    <!-- Список курсов -->
    <div class="space-y-4">
      <div
        v-for="course in courses"
        :key="course.id"
        class="bg-white rounded-lg shadow-lg p-4 flex justify-between items-center"
      >
        <div>
          <h2 class="text-xl font-semibold text-gray-800">{{ course.name }}</h2>
          <p class="text-gray-600">Описание: {{ course.description }}</p>
        </div>
        <div class="flex items-center space-x-2">
          <button
            @click="openSettingsModal(course)"
            class="text-gray-600 hover:text-indigo-600 transition duration-300"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 8v4m0 0v4m0-4h4m-4 0H8"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Кнопка добавления нового курса -->
    <div class="mt-6">
      <button
        @click="openAddCourseModal"
        class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition duration-300"
      >
        Добавить новый курс
      </button>
    </div>

    <!-- Модальное окно настройки курса -->
    <div
      v-if="isSettingsModalOpen"
      class="fixed inset-0 flex items-center justify-center z-50"
      @click.self="closeSettingsModal"
    >
      <div class="absolute inset-0 bg-black bg-opacity-50 backdrop-blur-sm"></div>
      <div class="relative bg-white rounded-2xl shadow-2xl w-96 p-6">
        <h2 class="text-2xl font-bold text-indigo-700 text-center mb-4">Настройки курса</h2>
        <input
          v-model="selectedCourse.name"
          type="text"
          placeholder="Название курса"
          class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 mb-4"
        />
        <textarea
          v-model="selectedCourse.description"
          placeholder="Описание курса"
          class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 mb-4"
        ></textarea>
        <div class="flex justify-end mt-4">
          <button
            @click="saveCourseSettings"
            class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition duration-300"
          >
            Сохранить
          </button>
          <button
            @click="closeSettingsModal"
            class="ml-2 px-4 py-2 bg-gray-300 text-black rounded-lg hover:bg-gray-400"
          >
            Отменить
          </button>
        </div>
      </div>
    </div>

    <!-- Модальное окно добавления курса -->
    <div
      v-if="isAddCourseModalOpen"
      class="fixed inset-0 flex items-center justify-center z-50"
      @click.self="closeAddCourseModal"
    >
      <div class="absolute inset-0 bg-black bg-opacity-50 backdrop-blur-sm"></div>
      <div class="relative bg-white rounded-2xl shadow-2xl w-96 p-6">
        <h2 class="text-2xl font-bold text-indigo-700 text-center mb-4">Добавить курс</h2>
        <input
          v-model="newCourseName"
          type="text"
          placeholder="Название курса"
          class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 mb-4"
        />
        <textarea
          v-model="newCourseDescription"
          placeholder="Описание курса"
          class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 mb-4"
        ></textarea>
        <div class="flex justify-end mt-4">
          <button
            @click="addCourse"
            class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition duration-300"
          >
            Добавить
          </button>
          <button
            @click="closeAddCourseModal"
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
  name: 'TeacherCourses',
  data() {
    return {
      courses: [
        {
          id: 1,
          name: 'Курс по программированию',
          description: 'Изучение основ программирования.',
          students: [],
        },
        {
          id: 2,
          name: 'Курс по математике',
          description: 'Углубленное изучение математики.',
          students: [],
        },
        {
          id: 3,
          name: 'Курс по науке',
          description: 'Научные эксперименты и исследования.',
          students: [],
        },
      ],
      isSettingsModalOpen: false,
      isAddCourseModalOpen: false,
      selectedCourse: {},
      newCourseName: '',
      newCourseDescription: '',
    }
  },
  methods: {
    openSettingsModal(course) {
      this.selectedCourse = { ...course } // Копируем курс для редактирования
      this.isSettingsModalOpen = true
    },
    closeSettingsModal() {
      this.isSettingsModalOpen = false
      this.selectedCourse = {}
    },
    saveCourseSettings() {
      const index = this.courses.findIndex((course) => course.id === this.selectedCourse.id)
      if (index !== -1) {
        this.courses[index] = this.selectedCourse // Обновляем курс
        this.closeSettingsModal()
        alert(`Курс "${this.selectedCourse.name}" обновлен.`)
      }
    },
    openAddCourseModal() {
      this.isAddCourseModalOpen = true
    },
    closeAddCourseModal() {
      this.isAddCourseModalOpen = false
      this.newCourseName = ''
      this.newCourseDescription = ''
    },
    addCourse() {
      if (this.newCourseName.trim() && this.newCourseDescription.trim()) {
        const newCourse = {
          id: this.courses.length + 1,
          name: this.newCourseName.trim(),
          description: this.newCourseDescription.trim(),
          students: [],
        }
        this.courses.push(newCourse)
        this.closeAddCourseModal()
        alert(`Курс "${newCourse.name}" добавлен.`)
      } else {
        alert('Пожалуйста, введите название и описание курса.')
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
