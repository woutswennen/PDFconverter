import '@babel/polyfill'
import 'mutationobserver-shim'
import Vue from 'vue'
import './plugins/bootstrap-vue'
import './plugins/bootstrap-vue'
import './plugins/bootstrap-vue'
import './plugins/bootstrap-vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import store from './store'
import { routes } from '@/router/index.js'


Vue.config.productionTip = false
Vue.prototype.$store = store

new Vue({
  router,
  vuetify,
  routes,
  store,
  render: h => h(App)
}).$mount('#app')
