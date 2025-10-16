<template>
  <div id="app-layout">
    <header>
      <nav>
        <router-link to="/">首页</router-link>
        <router-link to="/attractions">景点列表</router-link>
        <router-link to="/routes">路线列表</router-link>
        <router-link to="/customize">个性化定制</router-link>

        <span class="nav-separator">|</span>
        <router-link to="/admin">后台管理</router-link>
      </nav>
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>

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
</style>