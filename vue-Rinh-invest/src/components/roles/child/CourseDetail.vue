<template>
  <div class="max-w-7xl mx-auto p-8">
    <!-- Заголовок курса -->
    <div class="relative mb-12">
      <div
        class="h-48 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 rounded-3xl"
      ></div>
      <div class="absolute inset-x-0 bottom-0 transform translate-y-1/2 flex justify-center">
        <div class="bg-white rounded-full p-4 shadow-xl">
          <div
            class="w-20 h-20 rounded-full bg-gradient-to-r from-indigo-500 to-purple-500 flex items-center justify-center"
          >
            <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
              />
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Информация о курсе -->
    <div class="mt-16 text-center mb-12">
      <h1
        class="text-4xl font-extrabold mb-4 text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600"
      >
        Основы Python
      </h1>
      <p class="text-xl text-gray-600 max-w-2xl mx-auto">
        Изучите основы программирования на Python: от переменных до функций
      </p>
    </div>

    <!-- Прогресс курса -->
    <div class="max-w-2xl mx-auto mb-12 bg-white rounded-2xl shadow-lg p-6">
      <div class="space-y-4">
        <div class="flex justify-between items-center">
          <span class="text-lg font-semibold text-gray-700">Общий прогресс</span>
          <span class="text-lg font-bold text-indigo-600">50%</span>
        </div>
        <div class="h-3 bg-gray-200 rounded-full overflow-hidden">
          <div
            class="h-full bg-gradient-to-r from-indigo-500 to-purple-500 transition-all duration-500"
            style="width: 50%"
          ></div>
        </div>
      </div>
    </div>

    <!-- Список уроков -->
    <div class="space-y-6">
      <h2 class="text-2xl font-bold text-gray-800 mb-8">Уроки курса</h2>

      <div class="grid gap-6">
        <div
          v-for="(lesson, index) in lessons"
          :key="index"
          class="bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1"
        >
          <div class="p-6">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-4">
                <div
                  class="w-12 h-12 rounded-full flex items-center justify-center"
                  :class="[
                    lesson.completed
                      ? 'bg-green-100 text-green-600'
                      : lesson.active
                        ? 'bg-indigo-100 text-indigo-600'
                        : 'bg-gray-100 text-gray-400',
                  ]"
                >
                  <span class="text-xl font-bold">{{ index + 1 }}</span>
                </div>
                <div>
                  <h3 class="text-lg font-semibold text-gray-800">{{ lesson.title }}</h3>
                  <p class="text-sm text-gray-600">{{ lesson.duration }}</p>
                </div>
              </div>

              <div class="flex items-center">
                <span
                  class="px-4 py-2 rounded-full text-sm font-medium"
                  :class="[
                    lesson.completed
                      ? 'bg-green-100 text-green-800'
                      : lesson.active
                        ? 'bg-indigo-100 text-indigo-800'
                        : 'bg-gray-100 text-gray-600',
                  ]"
                >
                  {{ lesson.completed ? 'Завершено' : lesson.active ? 'В процессе' : 'Не начат' }}
                </span>
              </div>
            </div>

            <div class="mt-4">
              <button
                @click="startLesson(index)"
                class="w-full py-3 px-4 rounded-xl font-semibold text-white transition-all duration-300 disabled:bg-gray-300 disabled:cursor-not-allowed enabled:bg-gradient-to-r enabled:from-indigo-600 enabled:to-purple-600 enabled:hover:from-indigo-700 enabled:hover:to-purple-700 transform enabled:hover:scale-[1.02] enabled:active:scale-[0.98] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                :disabled="!lesson.active && !lesson.completed"
              >
                {{
                  lesson.completed
                    ? 'Повторить урок'
                    : lesson.active
                      ? 'Продолжить'
                      : 'Скоро будет доступен'
                }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CourseDetail',
  data() {
    return {
      lessons: [
        {
          title: 'Введение в Python',
          duration: '30 минут',
          completed: true,
          active: false,
        },
        {
          title: 'Переменные и типы данных',
          duration: '45 минут',
          completed: true,
          active: false,
        },
        {
          title: 'Условные операторы',
          duration: '60 минут',
          completed: false,
          active: true,
        },
        {
          title: 'Циклы',
          duration: '60 минут',
          completed: false,
          active: false,
        },
        {
          title: 'Функции',
          duration: '75 минут',
          completed: false,
          active: false,
        },
      ],
    }
  },
  methods: {
    startLesson(index) {
      // Переход на страницу CoursePlay с передачей информации о текущем уроке
      this.$router.push(`/courseplay`)
    },
  },
}
</script>

<style scoped>
/* Добавляем плавную анимацию для всех transition эффектов */
* {
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

/* Тень для карточек при наведении */
.hover\:shadow-xl:hover {
  box-shadow:
    0 20px 25px -5px rgba(0, 0, 0, 0.1),
    0 10px 10px -5px rgba(0, 0, 0, 0.04);
}
</style>
