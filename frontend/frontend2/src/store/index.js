import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    solitan: {}
  },
  getters: {
    getSolitan(state){
        return state.solitan
    }

  },
  mutations: {
    setSolitan(state, solitan){
        state.solitan = solitan
    },
    setWorkExperience(state,work_experience){
        state.solitan.work_experience = work_experience
    }
  },
  actions: {
    fetchSolitan(context){
        console.log("ewa broer")
        return fetch("http://localhost:5000/solitan")
        .then((response) => response.json())
        .then((data) => {
          console.log(data)
          context.commit("setSolitan", data);
        })
        .catch((err) => console.error(err));
    }
  },
  modules: {
  }
})
