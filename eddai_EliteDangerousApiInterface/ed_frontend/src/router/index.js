import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory("/"),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/ScrollTextAnimation',
      name: 'ScrollTextAnimation',
      component: () => import("../views/ScrollTextAnimation.vue")
    }
  ],
})

export default router
