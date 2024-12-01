import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Импорт VueKonva
import VueKonva from 'vue-konva'

const app = createApp(App)

// Подключение маршрутизатора
app.use(router)

// Подключение VueKonva
app.use(VueKonva)

// Монтируем приложение
app.mount('#app')
