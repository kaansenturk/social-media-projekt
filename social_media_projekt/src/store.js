import { createStore } from 'vuex';

export default createStore({
    state: {
        count: 1, // das ist nur ein Beispiel zur Hilfe zur Erklärung
        logged_user: null,
        API: "http://localhost:8000",
    },
    mutations: {
      setUser(state, user) {
        state.user = user;
      },
    },
    actions: {
      login({ commit }, user) {
        // Perform authentication logic here
        // Once authentication is successful, commit the user to the store
        commit('setUser', user);
      },
      logout({ commit }) {
        // Perform logout logic here
        // Once logout is successful, clear the user from the store
        commit('setUser', null);
      },
    },
    getters: {
      currentUser: (state) => state.user,
      isLoggedIn: (state) => state.user !== null,
    }

});