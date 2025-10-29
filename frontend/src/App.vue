<template>
  <div id="app-layout">
    <header>
      <nav>
        <div class="nav-left">
          <router-link to="/">{{ $t('nav.home') }}</router-link>
          <router-link to="/attractions">{{ $t('attractions.title') }}</router-link>
          <router-link to="/routes">{{ $t('routes.title') }}</router-link>
          <router-link to="/customize">{{ $t('personalization.title') }}</router-link>

          <span class="nav-separator">|</span>
          <router-link to="/admin">{{ $t('nav.admin') }}</router-link>
        </div>

        <div class="nav-right">
          <LanguageMenu />
          <button v-if="isLoggedIn" @click="handleLogout" class="logout-button">{{ $t('nav.logout') }}</button>
        </div>
      </nav>
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import LanguageMenu from './components/LanguageMenu.vue'

const router = useRouter()
const route = useRoute()
const isLoggedIn = ref(false)

const checkLoginStatus = () => {
  isLoggedIn.value = localStorage.getItem('isLoggedIn') === 'true'
}

const handleLogout = () => {
  localStorage.removeItem('isLoggedIn')
  checkLoginStatus()
  router.push('/login')
}

onMounted(() => {
  checkLoginStatus()
})

// Watch for route changes to update login status (e.g., after login/logout)
watch(route, () => {
  checkLoginStatus()
})
</script>

<style>
/* Apple-inspired Design System */
:root {
  --system-font: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
  --background-color: #f5f6fa; /* A slightly cool off-white */
  --card-background-color: #ffffff;
  --primary-text-color: #1d1d1f; /* Near black for high contrast */
  --secondary-text-color: #6e6e73;
  --accent-color: #c0392b; /* The project's red, used as an accent */
  --border-color: #d1d1d6;
  --card-border-radius: 16px;
  --card-shadow: 0 4px 12px rgba(0, 0, 0, 0.08), 0 2px 4px rgba(0, 0, 0, 0.05);
}

body {
  font-family: var(--system-font);
  background-color: var(--background-color);
  color: var(--primary-text-color);
  margin: 0;
}

#app-layout header {
  background-color: var(--card-background-color);
  padding: 1rem 2rem;
  text-align: center;
  border-bottom: 1px solid var(--border-color);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
}

#app-layout nav {
  display: flex;
  align-items: center; /* Align items vertically */
  justify-content: space-between; /* 左右分布 */
}

.nav-left, .nav-right {
  display: flex;
  align-items: center;
}

.nav-right {
  gap: 10px;
}

#app-layout nav a {
  color: var(--secondary-text-color);
  font-weight: 600;
  font-size: 1rem;
  text-decoration: none;
  margin: 0 1rem;
  padding: 0.5rem 0;
  transition: color 0.3s ease;
}

#app-layout nav a:hover {
  color: var(--primary-text-color);
}

#app-layout nav a.router-link-exact-active {
  color: var(--accent-color);
  box-shadow: 0 2px 0 var(--accent-color);
}

#app-layout main {
  max-width: 960px;
  margin: 2rem auto;
  padding: 1rem;
}

.nav-separator {
  color: var(--border-color);
  margin: 0 0.5rem;
}

.logout-button {
  background: none;
  border: none;
  color: var(--secondary-text-color);
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  margin-left: 1rem;
  transition: color 0.3s ease;
}

.logout-button:hover {
  color: var(--primary-text-color);
}
</style>