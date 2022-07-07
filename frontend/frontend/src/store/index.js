import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import createPersistedState from "vuex-persistedstate"


Vue.use(Vuex)

export default new Vuex.Store({
  plugins: [createPersistedState({
      storage: window.sessionStorage
  })],
  state: {
    solitan: {}
  },
  getters: {
    getSolitan(state){
      return state.solitan
    },
  },
  mutations: {
    editSolitan(state, solitan){
        state.solitan = solitan

    },
    editWorkExperience(state, work_experience){ state.solitan.work_experience = work_experience }
  },
  actions: {
    fetchSolitan(state){
        console.log('fetching')
        const path = "http://localhost:5000/solitan";
            axios
              .get(path)
              .then((res) => {
                state.commit("editSolitan", res.data.data)
              })
              .catch((error) => {
                console.error(error);
              });
    }
  },
  modules: {
  }
})
