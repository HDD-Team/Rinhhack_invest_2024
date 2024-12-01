<template>
  <div class="max-w-4xl mx-auto p-8">
    <h1 class="text-3xl font-bold text-indigo-700 mb-4">Статистика ребенка</h1>
    <div class="bg-white rounded-lg shadow-lg p-6 mb-6">
      <p><strong>Имя ребенка:</strong> {{ child.name }}</p>
      <p><strong>Класс:</strong> {{ child.class }}</p>
      <p><strong>Группа:</strong> {{ child.group }}</p>
    </div>

    <h2 class="text-2xl font-bold mt-6 text-indigo-700">Курсы</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
      <div
        v-for="(course, index) in courses"
        :key="index"
        class="bg-white rounded-lg shadow-md p-4 flex justify-between items-center transition-transform transform hover:scale-105"
      >
        <div>
          <h3 class="text-lg font-semibold text-gray-800">{{ course.name }}</h3>
          <p class="text-gray-600">Прогресс: {{ course.progress }}%</p>
          <p v-if="course.grade" class="text-gray-500">Оценка: {{ course.grade }}</p>
        </div>
        <div class="flex items-center">
          <svg
            class="w-6 h-6 text-indigo-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 8v4m0 0v4m0-4h4m-4 0H8"
            />
          </svg>
        </div>
      </div>
    </div>

    <div class="mt-6">
      <button
        @click="openAddCourseModal"
        class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition duration-300"
      >
        Добавить курс
      </button>
    </div>

    <!-- Модальное окно добавления курса -->
    <div
      v-if="isModalOpen"
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
        <input
          v-model="newCourseProgress"
          type="number"
          placeholder="Прогресс (%)"
          class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 mb-4"
        />
        <input
          v-model="newCourseGrade"
          type="text"
          placeholder="Оценка"
          class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 mb-4"
        />
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
  name: 'ChildStatistics',
  data() {
    return {
      child: {
        name: 'Иван Иванов',
        class: '5А',
        group: 'Группа 1',
      },
      courses: [
        { name: 'Основы Python', progress: 75, grade: '4' },
        { name: 'Алгоритмы', progress: 50, grade: '3' },
      ],
      isModalOpen: false,
      newCourseName: '',
      newCourseProgress: '',
      newCourseGrade: '',
    }
  },
  methods: {
    openAddCourseModal() {
      this.isModalOpen = true
    },
    closeAddCourseModal() {
      this.isModalOpen = false
      this.newCourseName = ''
      this.newCourseProgress = ''
      this.newCourseGrade = ''
    },
    addCourse() {
      if (
        this.newCourseName.trim() &&
        this.newCourseProgress.trim() &&
        this.newCourseGrade.trim()
      ) {
        const newCourse = {
          name: this.newCourseName.trim(),
          progress: parseInt(this.newCourseProgress.trim()),
          grade: this.newCourseGrade.trim(),
        }
        this.courses.push(newCourse)
        this.closeAddCourseModal()
        alert(`Курс "${newCourse.name}" добавлен.`)
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
