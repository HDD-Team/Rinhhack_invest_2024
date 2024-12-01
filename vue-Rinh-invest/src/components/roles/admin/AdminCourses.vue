<template>
  <div class="p-6 bg-white rounded-lg shadow-lg">
    <h1 class="text-3xl font-bold text-indigo-700 mb-4">Управление курсами</h1>
    <button
      @click="createCourse"
      class="bg-indigo-700 text-white py-2 px-4 rounded-lg hover:bg-indigo-800 mb-6"
    >
      Создать курс
    </button>
    <ul>
      <li
        v-for="(course, index) in courses"
        :key="index"
        class="py-4 border-b flex justify-between items-center"
      >
        <span>{{ course.name }}</span>
        <button
          @click="editCourse(course.id)"
          class="text-indigo-700 hover:text-indigo-900 underline"
        >
          Редактировать
        </button>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'AdminCourses',
  data() {
    return {
      courses: [
        { id: 1, name: 'Основы Python' },
        { id: 2, name: 'Алгоритмы' },
      ],
    }
  },
  methods: {
    createCourse() {
      console.log('Создание нового курса')
      this.$router.push('/create-course')
    },
    editCourse(id) {
      console.log(`Редактирование курса с ID: ${id}`)
      this.$router.push(`/edit-course/${id}`)
    },
  },
}
</script>
