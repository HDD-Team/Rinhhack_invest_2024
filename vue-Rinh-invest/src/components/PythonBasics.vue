<template>
  <div class="min-h-screen flex">
    <!-- Левая часть: Чат -->
    <div :class="['flex-grow p-6 shadow-md', backgroundClass, 'bg-transition']">
      <h2
        class="text-3xl font-bold mb-4 text-center bg-gray-800 rounded-lg bg-opacity-60 text-white p-4"
      >
        Чат RPG
      </h2>

      <!-- Чат с прокруткой -->
      <div ref="chatContainer" class="space-y-4 overflow-y-auto h-96">
        <div v-for="(message, index) in messages" :key="index" class="flex items-start">
          <div v-if="message.role === 'system'" class="flex-shrink-0">
            <img src="https://via.placeholder.com/40" alt="Game" class="rounded-full" />
          </div>
          <div v-if="message.role === 'user'" class="flex-shrink-0 ml-auto">
            <img
              src="https://via.placeholder.com/40/0000FF/FFFFFF"
              alt="User"
              class="rounded-full"
            />
          </div>
          <div
            :class="{
              'ml-4 p-3 bg-gray-100 rounded-lg':
                message.role === 'system' && !message.success && !message.failure,
              'mr-4 p-3 bg-blue-500 text-white rounded-lg': message.role === 'user',
              'ml-4 p-3 bg-yellow-100 border-l-4 border-yellow-500 rounded-lg': message.success,
              'ml-4 p-3 bg-red-100 border-l-4 border-red-500 rounded-lg': message.failure,
            }"
          >
            {{ message.text }}
          </div>
        </div>
      </div>
    </div>

    <!-- Правая часть: Интерактивная консоль -->
    <div class="w-1/3 bg-gray-100 p-6 border-l shadow-md flex flex-col">
      <h3 class="text-xl font-bold mb-4 text-center">Интерактивная консоль</h3>

      <!-- Консоль с прокруткой -->
      <div
        class="flex-grow bg-gray-800 text-white p-4 font-mono console-output overflow-y-auto h-64"
      >
        <div
          v-for="(command, index) in consoleCommands"
          :key="'console-' + index"
          class="whitespace-pre-line"
        >
          <span class="console-caret">></span> {{ command }}
        </div>
      </div>

      <div ref="codeMirrorContainer" class="mt-4"></div>

      <div class="mt-4 flex justify-center">
        <button
          @click="submitCode"
          class="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600"
        >
          Отправить
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import CodeMirror from 'codemirror'
import 'codemirror/lib/codemirror.css'
import 'codemirror/theme/dracula.css'
import 'codemirror/mode/python/python.js'

export default {
  data() {
    return {
      codeInput: '',
      messages: [],
      consoleCommands: [],
      currentEventIndex: 0,
      events: [
        {
          text: 'Вы оказались в темной комнате. Перед вами дверь. Попробуйте открыть её!',
          expectedCode: 'open_door()',
          successText: 'Вы открыли дверь и вышли из комнаты.',
          failureText: 'Неправильно. Попробуйте что-то другое.',
          backgroundClass: 'bg-dark-room',
        },
        {
          text: 'Вы оказались в лесу. На земле лежит ключ. Попробуйте его поднять.',
          expectedCode: 'pick_up_key()',
          successText: 'Вы подняли ключ. Возможно, он пригодится позже.',
          failureText: 'Вы не подняли ключ. Попробуйте снова.',
          backgroundClass: 'bg-forest',
        },
        {
          text: 'Перед вами замок с закрытыми воротами. Попробуйте использовать ключ, чтобы открыть их.',
          expectedCode: 'use_key()',
          successText: 'Ворота открылись, и вы завершили игру!',
          failureText: 'Это не сработало. Попробуйте снова.',
          backgroundClass: 'bg-castle',
        },
      ],
    }
  },
  computed: {
    currentEvent() {
      return this.events[this.currentEventIndex]
    },
    backgroundClass() {
      return this.currentEvent?.backgroundClass || ''
    },
  },
  methods: {
    submitCode() {
      if (!this.codeInput.trim()) return

      this.consoleCommands.push(this.codeInput.trim())

      if (this.codeInput.trim() === this.currentEvent.expectedCode) {
        const successMessage = {
          role: 'system',
          text: this.currentEvent.successText,
          success: true,
        }
        this.messages.push(successMessage)
        this.moveToNextEvent()
      } else {
        const failureMessage = {
          role: 'system',
          text: this.currentEvent.failureText,
          failure: true,
        }
        this.messages.push(failureMessage)
      }

      this.scrollToBottom('chatContainer')

      this.codeInput = ''
      this.codeMirror.setValue('')
    },

    moveToNextEvent() {
      if (this.currentEventIndex < this.events.length - 1) {
        this.currentEventIndex += 1
        this.messages.push({
          role: 'system',
          text: this.events[this.currentEventIndex].text,
        })
      } else {
        this.messages.push({
          role: 'system',
          text: 'Поздравляем! Вы прошли все задания!',
        })
      }
      this.scrollToBottom('chatContainer')
    },

    scrollToBottom(refName) {
      this.$nextTick(() => {
        const container = this.$refs[refName]
        container.scrollTop = container.scrollHeight
      })
    },
  },
  mounted() {
    this.messages.push({ role: 'system', text: this.currentEvent.text })
    this.codeMirror = CodeMirror(this.$refs.codeMirrorContainer, {
      value: '',
      mode: 'python',
      theme: 'dracula',
      lineNumbers: true,
      lineWrapping: true,
      matchBrackets: true,
      autoCloseBrackets: true,
      viewportMargin: Infinity,
      styleActiveLine: true,
    })

    this.codeMirror.on('keyup', (cm) => {
      this.codeInput = cm.getValue()
    })

    this.scrollToBottom('chatContainer')
  },
}
</script>

<style scoped>
body {
  font-family: 'Comic Sans MS', 'Comic Sans', cursive;
}

h2,
h3 {
  font-family: 'Comic Sans MS', 'Comic Sans', cursive;
  font-weight: bold;
}

.console-caret {
  color: #32cd32;
}

.bg-dark-room {
  background-image: url('@/assets/dark-room.jpg'); /* Укажите путь к вашему изображению */
  background-size: cover;
  background-position: center;
}

.bg-forest {
  background-image: url('@/assets/forest-image.jpg'); /* Укажите путь к вашему изображению */
  background-size: cover;
  background-position: center;
}

.bg-castle {
  background-image: url('path/to/castle-image.jpg'); /* Укажите путь к вашему изображению */
  background-size: cover;
  background-position: center;
}

.bg-transition {
  transition: background-image 1s ease-in-out;
}

.ml-4.p-3.bg-gray-100 {
  background-color: #f5f5f5;
}

.ml-4.p-3.bg-yellow-100 {
  background-color: #fffbe6;
}

.border-l-4.border-yellow-500 {
  border-color: #f59e0b;
}

.ml-4.p-3.bg-red-100 {
  background-color: #ffe5e5;
}

.border-l-4.border-red-500 {
  border-color: #dc2626;
}

/* Ограничение высоты и прокрутка */
.h-96 {
  height: 35rem; /* Ограничение высоты для чата */
}

.h-64 {
  height: 16rem; /* Ограничение высоты для консоли */
}

.overflow-y-auto {
  overflow-y: auto; /* Прокрутка по вертикали */
}
</style>
