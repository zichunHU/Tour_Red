import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import AttractionListPage from '../views/AttractionListPage.vue'
import AttractionDetailPage from '../views/AttractionDetailPage.vue'
import RouteListPage from '../views/RouteListPage.vue'
import RouteDetailPage from '../views/RouteDetailPage.vue'
import PersonalizationPage from '../views/PersonalizationPage.vue'

// Admin Components
import AdminDashboard from '../views/AdminDashboard.vue'
import AdminAttractions from '../views/AdminAttractions.vue'
import AttractionForm from '../views/AttractionForm.vue'
import AdminRoutes from '../views/AdminRoutes.vue'
import RouteForm from '../views/RouteForm.vue'

const routes = [
  // Public Routes
  { path: '/', name: 'Home', component: HomePage },
  { path: '/attractions', name: 'AttractionList', component: AttractionListPage },
  { path: '/attractions/:id', name: 'AttractionDetail', component: AttractionDetailPage, props: true },
  { path: '/routes', name: 'RouteList', component: RouteListPage },
  { path: '/routes/:id', name: 'RouteDetail', component: RouteDetailPage, props: true },
  { path: '/customize', name: 'Personalization', component: PersonalizationPage },

  // Admin Routes
  { path: '/admin', name: 'AdminDashboard', component: AdminDashboard },
  { path: '/admin/attractions', name: 'AdminAttractions', component: AdminAttractions },
  { path: '/admin/attractions/new', name: 'NewAttraction', component: AttractionForm },
  { path: '/admin/attractions/edit/:id', name: 'EditAttraction', component: AttractionForm, props: true },
  { path: '/admin/routes', name: 'AdminRoutes', component: AdminRoutes },
  { path: '/admin/routes/new', name: 'NewRoute', component: RouteForm },
  { path: '/admin/routes/edit/:id', name: 'EditRoute', component: RouteForm, props: true },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router