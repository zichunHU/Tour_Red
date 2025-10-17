import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import AttractionListPage from '../views/AttractionListPage.vue'
import AttractionDetailPage from '../views/AttractionDetailPage.vue'
import RouteListPage from '../views/RouteListPage.vue'
import RouteDetailPage from '../views/RouteDetailPage.vue'
import PersonalizationPage from '../views/PersonalizationPage.vue'
import LoginPage from '../views/LoginPage.vue' // 导入登录页面

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
  { path: '/login', name: 'Login', component: LoginPage }, // 登录路由

  // Admin Routes
  { path: '/admin', name: 'AdminDashboard', component: AdminDashboard, meta: { requiresAuth: true } },
  { path: '/admin/attractions', name: 'AdminAttractions', component: AdminAttractions, meta: { requiresAuth: true } },
  { path: '/admin/attractions/new', name: 'NewAttraction', component: AttractionForm, meta: { requiresAuth: true } },
  { path: '/admin/attractions/edit/:id', name: 'EditAttraction', component: AttractionForm, props: true, meta: { requiresAuth: true } },
  { path: '/admin/routes', name: 'AdminRoutes', component: AdminRoutes, meta: { requiresAuth: true } },
  { path: '/admin/routes/new', name: 'NewRoute', component: RouteForm, meta: { requiresAuth: true } },
  { path: '/admin/routes/edit/:id', name: 'EditRoute', component: RouteForm, props: true, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 全局导航守卫
router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'

  if (to.matched.some(record => record.meta.requiresAuth) && !isLoggedIn) {
    // 如果路由需要认证，但用户未登录，则重定向到登录页
    next({ name: 'Login' })
  } else if (to.name === 'Login' && isLoggedIn) {
    // 如果用户已登录，但尝试访问登录页，则重定向到管理后台首页
    next({ name: 'AdminDashboard' })
  } else {
    next() // 正常放行
  }
})

export default router