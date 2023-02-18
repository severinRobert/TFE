import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ProductListView from '../views/ProductListView.vue'
import ProductDetailView from '../views/ProductDetailView.vue'
import FormView from '../views/FormView.vue'
import ProfileView from '../views/ProfileView.vue'
import DashboardView from '../views/DashboardView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/productList', name: 'productList', component: ProductListView },
    { path: '/productDetail', name: 'productDetail', component: ProductDetailView },
    { path: '/form', name: 'form', component: FormView },
    { path: '/profile', name: 'profile', component: ProfileView },
    { path: '/dashboard', name: 'dashboard', component: DashboardView }
  ]
})

export default router
