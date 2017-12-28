// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from './api'
import Vuex from 'vuex'
import ElementUI from 'element-ui'
// import 'bulma'
import 'font-awesome/scss/font-awesome.scss'
// import './assets/css/element-variables.scss'
import 'element-ui/lib/theme-chalk/index.css'

Vue.prototype.$http = axios
Vue.use(Vuex)
Vue.use(ElementUI)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: { App }
})
