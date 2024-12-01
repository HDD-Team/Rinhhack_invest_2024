import { createStore } from 'vuex'

const store = createStore({
  state: {
    user: JSON.parse(localStorage.getItem('user')) || null,
  },
  mutations: {
    setUser(state, user) {
      state.user = user
      localStorage.setItem('user', JSON.stringify(user))
    },
    removeUser(state) {
      state.user = null
      localStorage.removeItem('user')
    },
  },
  actions: {
    loadUser({ commit }) {
      const user = JSON.parse(localStorage.getItem('user'))
      if (user) {
        commit('setUser', user)
      }
    },
    logout({ commit }) {
      commit('removeUser')
    },
  },
})

export default store
