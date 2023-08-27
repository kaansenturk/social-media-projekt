import { createStore } from 'vuex';

export default createStore({
    state: {
        count: 1, // das ist nur ein Beispiel zur Hilfe zur Erklärung
        logged_user: null,
        logged_user_id: null,
        API: "http://localhost:8000",

    },
    mutations: {
      setUser(state, user) {
        state.logged_user = user;
      },
      setUserId(state, user_id) {
        state.logged_user_id = user_id;
      },
    },
    actions: {
      login({ commit }, { user, user_id }) {
        commit('setUser', user);
        commit('setUserId', user_id);
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