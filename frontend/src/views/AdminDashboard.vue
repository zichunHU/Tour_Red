
<template>
  <div class="admin-dashboard-container">
    <header class="admin-dashboard-header">
      <h1>后台管理面板</h1>
      <p>欢迎回来，管理员！在这里管理您的景点和路线。</p>
    </header>

    <section class="dashboard-cards-grid">
      <router-link to="/admin/attractions" class="dashboard-card">
        <div class="card-icon">🏛️</div>
        <h2 class="card-title">景点管理</h2>
        <p class="card-description">添加、编辑或删除景点信息。</p>
      </router-link>
      <router-link to="/admin/routes" class="dashboard-card">
        <div class="card-icon">🗺️</div>
        <h2 class="card-title">路线管理</h2>
        <p class="card-description">创建、修改或移除推荐路线。</p>
      </router-link>
    </section>
  </div>
</template>

<style scoped>
.admin-dashboard-container {
  max-width: 960px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

.admin-dashboard-header {
  margin-bottom: 3rem;
}

.admin-dashboard-header h1 {
  font-weight: 700;
  font-size: 2.8rem;
  color: var(--primary-text-color);
  margin-bottom: 0.8rem;
}

.admin-dashboard-header p {
  font-size: 1.1rem;
  color: var(--secondary-text-color);
}

.dashboard-cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  justify-content: center;
}

.dashboard-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2.5rem 2rem;
  background-color: var(--card-background-color);
  border-radius: var(--card-border-radius);
  box-shadow: var(--card-shadow);
  text-decoration: none;
  color: var(--primary-text-color);
  transition: transform 0.3s ease, box-shadow 0.3s ease, color 0.3s ease;
}

.dashboard-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 25px rgba(0,0,0,0.15), 0 6px 12px rgba(0,0,0,0.1);
  color: var(--accent-color); /* Highlight text on hover */
}

.card-icon {
  font-size: 3.5rem;
  margin-bottom: 1rem;
  line-height: 1;
}

.card-title {
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: inherit; /* Inherit color from parent, changes on hover */
}

.card-description {
  font-size: 1rem;
  color: var(--secondary-text-color);
  line-height: 1.5;
}
</style>
