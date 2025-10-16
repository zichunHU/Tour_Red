
<template>
  <div class="admin-dashboard">
    <h1>后台管理</h1>
    <p>请选择要管理的内容：</p>
    <nav class="dashboard-nav">
      <router-link to="/admin/attractions" class="nav-card">景点管理</router-link>
      <router-link to="/admin/routes" class="nav-card">路线管理</router-link>
    </nav>
  </div>
</template>

<style scoped>
.admin-dashboard {
  text-align: center;
}

.admin-dashboard h1 {
  font-weight: 700;
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.dashboard-nav {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-top: 2rem;
}

.nav-card {
  display: block;
  padding: 2rem 3rem;
  background-color: var(--card-background-color);
  border-radius: var(--card-border-radius);
  box-shadow: var(--card-shadow);
  text-decoration: none;
  color: var(--primary-text-color);
  font-size: 1.5rem;
  font-weight: 600;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.nav-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.1), 0 4px 8px rgba(0,0,0,0.07);
  color: var(--accent-color);
}
</style>
