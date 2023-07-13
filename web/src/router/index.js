import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import OfferListView from '../views/OfferListView.vue'
import ProductDetailView from '../views/ProductDetailView.vue'
import FormView from '../views/FormView.vue'
import ProfileView from '../views/ProfileView.vue'
import DashboardView from '../views/DashboardView.vue'
import NotFoundView from '../views/NotFoundView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/offerList', name: 'offerList', component: OfferListView },
    { path: '/productDetail', name: 'productDetail', component: ProductDetailView },
    { path: '/form', name: 'form', component: FormView },
    { path: '/profile', name: 'profile', component: ProfileView,
      children: [
        { path: ':id', name: 'profileWithId', component: ProfileView },
      ]
    },
    { path: '/dashboard', name: 'dashboard', component: DashboardView, 
      children: [
        { path: 'product/:id', name: 'dashboardProduct', component: DashboardView },
        { path: 'selectionsGroup/:id', name: 'dashboardSelectionsGroup', component: DashboardView },
      ]
    },
    { path: '/:pathMatch(.*)*', name: 'not-found', component: NotFoundView }
  ]
})

export default router
