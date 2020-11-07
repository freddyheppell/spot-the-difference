import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/Login.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/:share_code_1/:share_code_2',
    name: 'Compare',
    component: () => import('../views/Compare.vue')
  },
  {
    path: '/:share_code_1',
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
