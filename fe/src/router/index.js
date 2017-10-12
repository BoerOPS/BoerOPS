import Vue from 'vue'
import Router from 'vue-router'
import Hello from '@/components/Hello'
import Home from '@/views/Home'
import Login from '@/views/Login'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      redirect: '/home'
    },
    {
      path: '/login',
      iconCls: 'fa fa-id-card-o',
      name: 'Login',
      component: Login
    },
    {
      path: '/hello',
      iconCls: 'fa fa-id-card-o',
      name: 'Hello',
      component: Hello
    },
    {
      path: '/home',
      iconCls: 'fa fa-id-card-o',
      name: 'Home',
      component: Home
    }
  ]
})
