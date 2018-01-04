import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/views/Login'
import Home from '@/views/Home'
import Project from '@/views/Project'
import Base from '@/views/Base'
import Deploy from '@/views/Deploy'
import Host from "@/views/Host";
import axios from 'axios'
import { isNull } from 'util';

Vue.use(Router)

// export default new Router({
//   routes: [
//     {
//       path: '/',
//       name: 'Home',
//       component: Home
//       // redirect: {name: 'Login'}
//     },
//     {
//       path: '/login',
//       name: 'Login',
//       component: Login
//     }
//   ]
// })

var router = new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
      // redirect: {name: 'Login'}
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/project',
      name: 'Project',
      component: Project
    },
    {
      path: '/base',
      name: 'Base',
      component: Base
    },
    {
      path: '/deploy',
      name: 'Deploy',
      component: Deploy
    },
    {
      path: '/host',
      name: 'Host',
      component: Host
    }
  ]
})

// router.beforeEach((to, from, next) => {
//   let access_token = localStorage.getItem('access_token');
//   if (!access_token || access_token === 'null') {
//     if (to.name != 'Login') {
//       next({ path: '/login' });
//     } else {
//       next();
//     }
//   } else {
//     if (to.name == 'Login') {
//       next('/');
//     } else {
//       next();
//     }
//   }
// })

export default router;
