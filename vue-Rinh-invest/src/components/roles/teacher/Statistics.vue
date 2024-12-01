<template>
  <div class="p-6 bg-white rounded-lg shadow-lg">
    <h1 class="text-3xl font-bold text-indigo-700 mb-4">Статистика</h1>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div
        v-for="stat in statistics"
        :key="stat.class"
        class="p-4 bg-yellow-50 rounded-lg shadow-md hover:bg-yellow-100"
      >
        <h2 class="text-xl font-bold text-yellow-800">Класс: {{ stat.class }}</h2>
        <p class="text-sm text-gray-700 mt-2">Средний прогресс: {{ stat.averageProgress }}%</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Statistics',
  data() {
    return {
      statistics: [
        { class: '5А', averageProgress: 75 },
        { class: '6Б', averageProgress: 62 },
      ],
    }
  },
}
</script>
