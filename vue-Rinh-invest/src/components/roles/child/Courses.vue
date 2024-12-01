<template>
  <div class="max-w-7xl mx-auto p-8">
    <h1
      class="text-4xl font-extrabold text-center mb-12 text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600"
    >
      Доступные курсы
    </h1>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
      <div
        v-for="course in courses"
        :key="course.id"
        class="group relative bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2"
      >
        <!-- Градиентный фон верхней части карточки -->
        <div class="h-24 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500"></div>

        <!-- Основной контент карточки -->
        <div class="p-6 -mt-8">
          <!-- Иконка курса -->
          <div
            class="w-16 h-16 rounded-full bg-white shadow-lg flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-300"
          >
            <svg
              class="w-8 h-8 text-indigo-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
              />
            </svg>
          </div>

          <!-- Название курса -->
          <h2 class="text-2xl font-bold text-gray-800 text-center mb-4">{{ course.name }}</h2>

          <!-- Описание -->
          <p class="text-gray-600 text-center mb-6">{{ course.description }}</p>

          <!-- Прогресс -->
          <div class="space-y-2 mb-6">
            <div class="flex justify-between items-center">
              <span class="text-sm font-medium text-gray-600">Прогресс курса</span>
              <span class="text-sm font-semibold text-indigo-600">{{ course.progress }}%</span>
            </div>
            <div class="h-2 bg-gray-200 rounded-full overflow-hidden">
              <div
                class="h-full bg-gradient-to-r from-indigo-500 to-purple-500 transition-all duration-500"
                :style="{ width: `${course.progress}%` }"
              ></div>
            </div>
          </div>

          <!-- Статус -->
          <div class="flex items-center justify-center mb-6">
            <span
              :class="[
                'px-3 py-1 rounded-full text-sm font-medium',
                course.progress === 100
                  ? 'bg-green-100 text-green-800'
                  : course.progress > 0
                    ? 'bg-yellow-100 text-yellow-800'
                    : 'bg-blue-100 text-blue-800',
              ]"
            >
              {{
                course.progress === 100
                  ? 'Завершено'
                  : course.progress > 0
                    ? 'В процессе'
                    : 'Не начат'
              }}
            </span>
          </div>

          <!-- Кнопка -->
          <button
            @click="startCourse"
            :disabled="course.progress === 100"
            class="w-full py-3 px-4 rounded-xl font-semibold text-white transition-all duration-300 disabled:bg-gray-300 disabled:cursor-not-allowed enabled:bg-gradient-to-r enabled:from-indigo-600 enabled:to-purple-600 enabled:hover:from-indigo-700 enabled:hover:to-purple-700 transform enabled:hover:scale-[1.02] enabled:active:scale-[0.98] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            {{ course.progress === 100 ? 'Курс пройден' : 'Начать обучение' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Courses',
  data() {
    return {
      courses: [
        {
          id: 1,
          name: 'Основы Python',
          description: 'Изучите основы программирования на Python: от переменных до функций',
          progress: 50,
        },
        {
          id: 2,
          name: 'Алгоритмы',
          description: 'Развивайте логическоке мышление через изучение базовых алгоритмов',
          progress: 20,
        },
        {
          id: 3,
          name: 'Веб-разработка',
          description: 'Создавайте современные веб-сайты с помощью HTML, CSS и JavaScript',
          progress: 0,
        },
      ],
    }
  },
  methods: {
    startCourse() {
      this.$router.push('/coursedetail')
    },
  },
}
</script>

<style scoped>
/* Добавляем плавную анимацию для всех transition эффектов */
* {
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

/* Добавляем тень для карточек при наведении */
.group:hover {
  box-shadow:
    0 20px 25px -5px rgba(0, 0, 0, 0.1),
    0 10px 10px -5px rgba(0, 0, 0, 0.04);
}
</style>
