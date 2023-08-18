import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import OfferListView from '../views/OfferListView.vue'
import FormView from '../views/FormView.vue'
import ProfileView from '../views/ProfileView.vue'
import DashboardView from '../views/DashboardView.vue'
import OfferView from '../views/OfferView.vue'
import GdprView from '../views/GdprView.vue'
import NotFoundView from '../views/NotFoundView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/offerList', name: 'offerList', component: OfferListView },
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
    { path: '/offer/:id', name: 'offer', component: OfferView },
    { path: '/gdpr', name: 'gdpr', component: GdprView },
    { path: '/:pathMatch(.*)*', name: 'not-found', component: NotFoundView }
  ]
})

export default router
