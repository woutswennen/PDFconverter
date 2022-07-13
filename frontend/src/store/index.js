import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate';

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
    }

  },
  mutations: {
    setSolitan(state, solitan){
        state.solitan = solitan
    },
    setWorkExperience(state,work_experience){
        state.solitan.work_experience = work_experience
    },
    setCertifications(state, certificates){
        state.solitan.certifications = certificates
    },
    setTechSkills(state, tech_skills){
        state.solitan.tech_skills = tech_skills
    },
    setProjects(state, projects){
        state.solitan.projects = projects
    },
    setEducations(state, education){
        state.solitan.education = education
    }
  },
  actions: {
    fetchSolitan(context){
        return fetch("http://localhost:5000/solitan")
        .then((response) => response.json())
        .then((data) => {
          context.commit("setSolitan", data.data);
        })
        .catch((err) => console.error(err));
    }
  },
  modules: {
  }
})