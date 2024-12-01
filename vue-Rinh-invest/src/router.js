import { createRouter, createWebHistory } from 'vue-router'

// Компоненты для маршрутов
import Login from '@/components/auth/Login.vue'
import Register from '@/components/auth/Register.vue'

// Ребенок
import Character from '@/components/roles/child/Character.vue'
import Courses from '@/components/roles/child/Courses.vue'
import CourseDetail from '@/components/roles/child/CourseDetail.vue'
import CoursePlay from '@/components/roles/child/CoursePlay.vue'

// Учитель
import TeacherProfile from '@/components/roles/teacher/TeacherProfile.vue'
import TeacherCourses from '@/components/roles/teacher/TeacherCourses.vue'
import TeacherClasses from '@/components/roles/teacher/TeacherClasses.vue'
import Statistics from '@/components/roles/teacher/Statistics.vue'

// Родитель
import ParentProfile from '@/components/roles/parent/ParentProfile.vue'
import ChildStatistics from '@/components/roles/parent/ChildStatistics.vue'

// Админ
import AdminCourses from '@/components/roles/admin/AdminCourses.vue'
import AdminProfiles from '@/components/roles/admin/AdminProfiles.vue'

const routes = [
  {
    path: '/',
    redirect: (to) => {
      const user = JSON.parse(localStorage.getItem('user'))
      if (!user) return '/login'

      const roleRoutes = {
        child: '/courses',
        teacher: '/teacher/profile',
        parent: '/parent/profile',
        admin: '/admin/courses',
      }

      return roleRoutes[user.role] || '/login'
    },
  },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },

  // Ребенок
  {
    path: '/courses',
    name: 'Courses',
    component: Courses,
    meta: { requiresAuth: true, role: 'child' },
  },
  {
    path: '/coursedetail',
    name: 'CourseDetail',
    component: CourseDetail,
    meta: { requiresAuth: true, role: 'child' },
  },

  {
    path: '/character',
    name: 'Character',
    component: Character,
    meta: { requiresAuth: true, role: 'child' },
  },
  {
    path: '/courseplay',
    name: 'CoursePlay',
    component: CoursePlay,
    meta: { requiresAuth: true, role: 'child' },
  },

  // Учитель
  {
    path: '/teacher/profile',
    name: 'TeacherProfile',
    component: TeacherProfile,
    meta: { requiresAuth: true, role: 'teacher' },
  },
  {
    path: '/teacher/courses',
    name: 'TeacherCourses',
    component: TeacherCourses,
    meta: { requiresAuth: true, role: 'teacher' },
  },
  {
    path: '/teacher/classes',
    name: 'TeacherClasses',
    component: TeacherClasses,
    meta: { requiresAuth: true, role: 'teacher' },
  },
  {
    path: '/teacher/statistics',
    name: 'Statistics',
    component: Statistics,
    meta: { requiresAuth: true, role: 'teacher' },
  },

  // Родитель
  {
    path: '/parent/profile',
    name: 'ParentProfile',
    component: ParentProfile,
    meta: { requiresAuth: true, role: 'parent' },
  },
  {
    path: '/parent/statistics',
    name: 'ChildStatistics',
    component: ChildStatistics,
    meta: { requiresAuth: true, role: 'parent' },
  },

  // Админ
  {
    path: '/admin/courses',
    name: 'AdminCourses',
    component: AdminCourses,
    meta: { requiresAuth: true, role: 'admin' },
  },
  {
    path: '/admin/profiles',
    name: 'AdminProfiles',
    component: AdminProfiles,
    meta: { requiresAuth: true, role: 'admin' },
  },

  // Страница 404
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: () => import('@/views/NotFound.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Глобальная защита маршрутов
router.beforeEach((to, from, next) => {
  const user = JSON.parse(localStorage.getItem('user'))

  // Если пользователь не авторизован и пытается получить доступ к защищенному маршруту
  if (to.meta.requiresAuth && !user) {
    next('/login')
    return
  }

  // Если пользователь авторизован и пытается получить доступ к страницам авторизации
  if (user && (to.path === '/login' || to.path === '/register')) {
    const roleRoutes = {
      child: '/courses',
      teacher: '/teacher/profile',
      parent: '/parent/profile',
      admin: '/admin/courses',
    }
    next(roleRoutes[user.role])
    return
  }

  // Проверка соответствия роли для защищенных маршрутов
  if (to.meta.role && user?.role !== to.meta.role) {
    const roleRoutes = {
      child: '/courses',
      teacher: '/teacher/profile',
      parent: '/parent/profile',
      admin: '/admin/courses',
    }
    next(roleRoutes[user.role] || '/login')
    return
  }

  next()
})

export default router
