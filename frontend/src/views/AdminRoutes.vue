
<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

const routes = ref([])
const loading = ref(true)
const error = ref(null)
const router = useRouter()
const { t } = useI18n()

const apiUrl = '/api';

const fetchRoutes = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await fetch(`${apiUrl}/routes`)
    if (!response.ok) throw new Error('Failed to fetch routes')
    routes.value = await response.json()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

const deleteRoute = async (id) => {
  if (!confirm(t('messages.deleteConfirmRoute'))) {
    return
  }
  try {
    const response = await fetch(`${apiUrl}/routes/${id}`, {
      method: 'DELETE',
    })
    if (!response.ok) throw new Error('Failed to delete route')
    await fetchRoutes()
  } catch (e) {
    alert(t('messages.deleteFailed', { error: e.message }))
  }
}

onMounted(fetchRoutes)

</script>

<template>
  <div>
    <div class="header-container">
      <h1>{{ t('admin.manageRoutes') }}</h1>
      <router-link to="/admin/routes/new" class="btn btn-primary">{{ t('routes.createRoute') }}</router-link>
    </div>

    <div v-if="loading">{{ t('common.loading') }}</div>
    <div v-if="error" class="error-message">{{ error }}</div>

    <table v-if="routes.length > 0" class="admin-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>{{ t('routes.routeName') }}</th>
          <th>{{ t('routes.attractionCount') }}</th>
          <th>{{ t('common.actions') }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="route in routes" :key="route.id">
          <td>{{ route.id }}</td>
          <td>{{ route.name }}</td>
          <td>{{ route.attraction_ids.length }}</td>
          <td class="actions">
            <router-link :to="`/admin/routes/edit/${route.id}`" class="btn btn-secondary">{{ t('common.edit') }}</router-link>
            <button @click="deleteRoute(route.id)" class="btn btn-danger">{{ t('common.delete') }}</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else-if="!loading">{{ t('routes.noResults') }}</p>
  </div>
</template>

<style scoped>
/* Using the same styles as AdminAttractions.vue for consistency */
.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.admin-table {
  width: 100%;
  border-collapse: collapse;
  background-color: var(--card-background-color);
  border-radius: var(--card-border-radius);
  box-shadow: var(--card-shadow);
  overflow: hidden;
}

.admin-table th, .admin-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

.admin-table thead {
  background-color: var(--background-color);
}

.admin-table th {
  font-weight: 600;
  color: var(--primary-text-color);
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 8px;
  text-decoration: none;
  cursor: pointer;
  font-weight: 500;
  font-family: var(--system-font);
  transition: opacity 0.2s ease;
}

.btn:hover {
  opacity: 0.8;
}

.btn-primary {
  background-color: var(--accent-color);
  color: white;
}

.btn-secondary {
  background-color: #e5e5ea;
  color: var(--primary-text-color);
}

.btn-danger {
  background-color: #ff3b30;
  color: white;
}

.error-message {
  color: var(--accent-color);
}
</style>
