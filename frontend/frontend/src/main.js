import Vue from "vue";
import App from "./App.vue";
import router from "./router";
// install bootstrap first
import 'bootstrap/dist/css/bootstrap.css';

// Importing the bootstrapvue library
import BootstrapVue from 'bootstrap-vue';

import vuetify from './plugins/vuetify'
import '@mdi/font/css/materialdesignicons.css'
import store from './store'
// javascript import for when you're importing the css directly in your javascript




Vue.config.productionTip = false;
Vue.use(BootstrapVue)

new Vue({
  router,
  vuetify,
  store,
  render: (h) => h(App)
}).$mount("#app");
