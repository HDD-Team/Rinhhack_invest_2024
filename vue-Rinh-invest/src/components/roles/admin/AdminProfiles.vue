<template>
  <div class="p-6 bg-white rounded-lg shadow-lg">
    <h1 class="text-3xl font-bold text-indigo-700 mb-4">Управление профилями</h1>
    <ul>
      <li
        v-for="(profile, index) in profiles"
        :key="index"
        class="py-4 border-b flex justify-between items-center"
      >
        <span>{{ profile.name }} ({{ profile.role }})</span>
        <button
          @click="viewProfile(profile.id)"
          class="text-indigo-700 hover:text-indigo-900 underline"
        >
          Просмотр
        </button>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'AdminProfiles',
  data() {
    return {
      profiles: [
        { id: 1, name: 'Иван Иванов', role: 'child' },
        { id: 2, name: 'Анна Смирнова', role: 'teacher' },
      ],
    }
  },
  methods: {
    viewProfile(id) {
      console.log(`Просмотр профиля с ID: ${id}`)
      this.$router.push(`/profile/${id}`)
    },
  },
}
</script>
