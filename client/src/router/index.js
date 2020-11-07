import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/Login.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/:token1/:token2',
    name: 'Compare',
    component: () => import('../views/Compare.vue')
  },
  {
    path: '/:token1',
    name: 'Login',
    component: Login
  },
  {
    path: '/*',
    name: 'Login',
    component: Login
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
