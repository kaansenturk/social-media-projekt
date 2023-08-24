import { createStore } from 'vuex';

export default createStore({
    state: {
        count: 1, // das ist nur ein Beispiel zur Hilfe zur Erklärung
        logged_user: null,
        API: "http://localhost:8000",

    },
    mutations: {
      setUser(state, user) {
        state.logged_user = user;
      },
    },
    actions: {
      login({ commit }, user) {
        commit('setUser', user);
      },
      logout({ commit }) {
        commit('setUser', null);
      },
    },
    getters: {
      currentUser: (state) => state.logged_user,
      isLoggedIn: (state) => state.logged_user !== null,
    }

});