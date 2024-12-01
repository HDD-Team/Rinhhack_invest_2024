<template>
  <div class="max-w-4xl mx-auto p-8">
    <h1 class="text-3xl font-bold text-indigo-700 mb-4">Классы учителя</h1>

    <button
      @click="openAddClassModal"
      class="mb-4 bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition duration-300"
    >
      Добавить класс
    </button>

    <div class="space-y-4">
      <div
        v-for="(classItem, index) in classes"
        :key="index"
        class="bg-white rounded-lg shadow-lg p-4"
      >
        <div class="flex justify-between items-center">
          <h2 class="text-xl font-semibold text-gray-800">{{ classItem.name }}</h2>
          <button
            @click="toggleClass(classItem)"
            class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition duration-300"
          >
            {{ classItem.showStudents ? 'Скрыть учеников' : 'Показать учеников' }}
          </button>
        </div>

        <div v-if="classItem.showStudents" class="mt-4">
          <h3 class="text-lg font-bold">Ученики:</h3>
          <ul class="list-disc pl-5">
            <li v-for="(student, index) in classItem.students" :key="index" class="text-gray-700">
              {{ student }}
            </li>
            <li v-if="classItem.students.length === 0" class="text-gray-500">
              Нет учеников в классе.
            </li>
          </ul>
        </div>

        <button
          @click="openAddStudentModal(classItem)"
          class="mt-4 bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition duration-300"
        >
          Добавить ученика
        </button>
      </div>
    </div>

    <!-- Модальное окно для добавления ученика -->
    <div
      v-if="isModalOpen"
      class="fixed inset-0 flex items-center justify-center z-50"
      @click.self="closeAddStudentModal"
    >
      <div class="absolute inset-0 bg-black bg-opacity-50 backdrop-blur-sm"></div>
      <div class="relative bg-white rounded-2xl shadow-2xl w-96 p-6">
        <h2 class="text-2xl font-bold text-indigo-700 text-center mb-4">Добавить ученика</h2>
        <input
          v-model="newStudentName"
          type="text"
          placeholder="Введите email ученика"
          class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 mb-4"
        />
        <div class="flex justify-end mt-4">
          <button
            @click="addStudent"
            class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition duration-300"
          >
            Добавить
          </button>
          <button
            @click="closeAddStudentModal"
            class="ml-2 px-4 py-2 bg-gray-300 text-black rounded-lg hover:bg-gray-400"
          >
            Отменить
          </button>
        </div>
      </div>
    </div>

    <!-- Модальное окно для добавления класса -->
    <div
      v-if="isClassModalOpen"
      class="fixed inset-0 flex items-center justify-center z-50"
      @click.self="closeAddClassModal"
    >
      <div class="absolute inset-0 bg-black bg-opacity-50 backdrop-blur-sm"></div>
      <div class="relative bg-white rounded-2xl shadow-2xl w-96 p-6">
        <h2 class="text-2xl font-bold text-indigo-700 text-center mb-4">Добавить класс</h2>
        <input
          v-model="newClassName"
          type="text"
          placeholder="Имя класса"
          class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 mb-4"
        />
        <div class="flex justify-end mt-4">
          <button
            @click="addClass"
            class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition duration-300"
          >
            Добавить
          </button>
          <button
            @click="closeAddClassModal"
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
  name: 'TeacherClasses',
  data() {
    return {
      classes: [],
      isModalOpen: false,
      isClassModalOpen: false,
      newStudentName: '',
      newClassName: '',
      selectedClass: null,
    }
  },
  methods: {
    // Загружаем классы учителя
    async fetchTeacherClasses() {
      const teacherId = JSON.parse(localStorage.getItem('user')).id

      try {
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/teacher?teacher_id=${teacherId}`,
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
          },
        )
        const data = await response.json()

        console.log('Ответ от сервера:', data) // Логируем ответ от сервера

        // Проверка на наличие clases_owner внутри message
        if (data.success && Array.isArray(data.message.clases_owner)) {
          console.log('Классы владельца:', data.message.clases_owner) // Логируем clases_owner

          // Преобразуем clases_owner, проверяя, что каждый элемент массива корректен
          this.classes = data.message.clases_owner.map((classItem, index) => {
            if (!Array.isArray(classItem)) {
              console.error(`Некорректный элемент в clases_owner на индексе ${index}:`, classItem)
              return {
                name: 'Некорректный класс',
                students: [],
                showStudents: false,
              }
            }

            // Убедимся, что каждый элемент массива имеет минимум три элемента
            const className = classItem[0] || 'Без названия'
            const students = Array.isArray(classItem[1]) ? classItem[1] : []
            const classId = classItem[2] || null // 3-й элемент — class_id

            // Сохраняем class_id в localStorage
            if (classId) {
              localStorage.setItem(`class_id_${index}`, classId) // Уникальный ключ для каждого класса
            }

            return {
              name: className,
              students: students,
              class_id: classId, // Добавляем class_id в объект
              showStudents: false,
            }
          })
        } else {
          console.error('Не удалось загрузить классы или clases_owner не является массивом')
          alert('Не удалось загрузить классы')
        }
      } catch (error) {
        console.error('Ошибка при загрузке классов:', error)
        alert('Ошибка при загрузке классов')
      }
    },
    // Добавляем новый класс
    // Добавляем нового ученика
    async addStudent() {
      if (this.newStudentName.trim()) {
        const classId = this.selectedClass.class_id // Получаем class_id из текущего выбранного класса
        const login = this.newStudentName.trim() // Логин — это email ученика

        if (classId) {
          try {
            const response = await fetch(
              `${import.meta.env.VITE_API_URL}/teacher/edit_class?class_id=${classId}&login=${login}`,
              {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
              },
            )
            const data = await response.json()

            if (data.success) {
              this.selectedClass.students.push(login) // Добавляем ученика локально
              this.newStudentName = '' // Очищаем поле ввода
              this.closeAddStudentModal() // Закрываем модальное окно
              alert('Ученик успешно добавлен')

              // После добавления ученика, обновляем список классов
              this.fetchTeacherClasses()
            } else {
              alert('Не удалось добавить ученика')
            }
          } catch (error) {
            console.error('Ошибка при добавлении ученика:', error)
            alert('Ошибка при добавлении ученика')
          }
        } else {
          alert('Ошибка: class_id не найден.')
        }
      } else {
        alert('Пожалуйста, введите email ученика.')
      }
    },

    // Переключаем видимость учеников
    toggleClass(classItem) {
      classItem.showStudents = !classItem.showStudents
    },

    // Открываем модальное окно для добавления ученика
    openAddStudentModal(classItem) {
      this.selectedClass = classItem
      this.isModalOpen = true
    },

    // Закрываем модальное окно для добавления ученика
    closeAddStudentModal() {
      this.isModalOpen = false
      this.selectedClass = null
    },

    // Открываем модальное окно для добавления класса
    openAddClassModal() {
      this.isClassModalOpen = true
    },

    // Закрываем модальное окно для добавления класса
    closeAddClassModal() {
      this.isClassModalOpen = false
      this.newClassName = ''
    },
  },
  mounted() {
    this.fetchTeacherClasses() // Загружаем классы при монтировании компонента
  },
}
</script>

<style scoped>
/* Добавьте любые дополнительные стили здесь */
</style>
