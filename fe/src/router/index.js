import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/modules/index'
import Test from '@/modules/test/'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index
    },{
      path: '/test',
      name: 'Test',
      component: Test
    }
  ]
})
