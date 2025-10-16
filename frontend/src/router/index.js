
import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import AttractionListPage from '../views/AttractionListPage.vue'
import AttractionDetailPage from '../views/AttractionDetailPage.vue'
import RouteListPage from '../views/RouteListPage.vue'
import RouteDetailPage from '../views/RouteDetailPage.vue'
import PersonalizationPage from '../views/PersonalizationPage.vue'

const routes = [
  { path: '/', name: 'Home', component: HomePage },
  { path: '/attractions', name: 'AttractionList', component: AttractionListPage },
  { path: '/attractions/:id', name: 'AttractionDetail', component: AttractionDetailPage, props: true },
  { path: '/routes', name: 'RouteList', component: RouteListPage },
  { path: '/routes/:id', name: 'RouteDetail', component: RouteDetailPage, props: true },
  { path: '/customize', name: 'Personalization', component: PersonalizationPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
