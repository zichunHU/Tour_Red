
<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

const route = useRoute()
const router = useRouter()
const { t } = useI18n()

const tourRoute = ref({
  name: '',
  description: '',
  attraction_ids: []
})

const loading = ref(false)
const error = ref(null)

const apiUrl = '/api';
const isEditMode = computed(() => !!route.params.id)

// Fetch existing route data in edit mode
onMounted(async () => {
  if (isEditMode.value) {
    loading.value = true
    try {
      // We need to fetch the raw route data, not the enriched one
      const response = await fetch(`${apiUrl}/routes`)
      if (!response.ok) throw new Error('Failed to fetch routes list')
      const allRoutes = await response.json()
      const currentRoute = allRoutes.find(r => r.id == route.params.id)
      if (!currentRoute) throw new Error('Route not found')
      tourRoute.value = currentRoute
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }
})

const handleSubmit = async () => {
  loading.value = true
  error.value = null
  try {
    const url = isEditMode.value 
      ? `${apiUrl}/routes/${route.params.id}` 
      : `${apiUrl}/routes`;

    const method = isEditMode.value ? 'PUT' : 'POST';

    // Ensure attraction_ids are numbers
    const payload = {
      ...tourRoute.value,
      attraction_ids: tourRoute.value.attraction_ids.map(id => Number(id)).filter(id => !isNaN(id))
    }

    const response = await fetch(url, {
      method: method,
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })

    if (!response.ok) {
      const errData = await response.json()
      throw new Error(errData.error || 'Save operation failed')
    }

    alert(t('messages.success'))
    router.push('/admin/routes')

  } catch (e) {
    error.value = e.message
  }
  finally {
    loading.value = false
  }
}

</script>

<template>
  <div>
    <h1>{{ isEditMode ? t('routes.editRoute') : t('routes.createRoute') }}</h1>
    <div v-if="loading && isEditMode">{{ t('common.loading') }}</div>
    <div v-if="error" class="error-message">{{ error }}</div>

    <form @submit.prevent="handleSubmit" class="admin-form">
      <div class="form-group">
        <label for="name">{{ t('routes.routeName') }}</label>
        <input id="name" v-model="tourRoute.name" type="text" required>
      </div>
      <div class="form-group">
        <label for="description">{{ t('routes.routeDescription') }}</label>
        <textarea id="description" v-model="tourRoute.description" rows="5"></textarea>
      </div>
      <div class="form-group">
        <label for="attraction_ids">{{ t('routes.attractionIdsLabel') }}</label>
        <input id="attraction_ids" :value="tourRoute.attraction_ids.join(', ')" @input="tourRoute.attraction_ids = $event.target.value.split(',').map(t => t.trim())" type="text">
        <small>{{ t('routes.attractionIdsExample') }}</small>
      </div>

      <div class="form-actions">
        <button type="submit" class="btn btn-primary" :disabled="loading">{{ loading ? t('common.loading') : t('common.save') }}</button>
        <router-link to="/admin/routes" class="btn btn-secondary">{{ t('common.cancel') }}</router-link>
      </div>
    </form>
  </div>
</template>

<style scoped>
/* Using the same styles as AttractionForm.vue for consistency */
.admin-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 2rem;
  background-color: var(--card-background-color);
  border-radius: var(--card-border-radius);
  box-shadow: var(--card-shadow);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
}

.form-group input,
.form-group textarea {
  font-family: var(--system-font);
  font-size: 1rem;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 10px;
  background-color: var(--background-color);
}

.form-group small {
  font-size: 0.9rem;
  color: var(--secondary-text-color);
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  text-decoration: none;
  cursor: pointer;
  font-weight: 600;
  font-family: var(--system-font);
  transition: opacity 0.2s ease;
  text-align: center;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background-color: var(--accent-color);
  color: white;
}

.btn-secondary {
  background-color: #e5e5ea;
  color: var(--primary-text-color);
}

.error-message {
  color: var(--accent-color);
  margin-bottom: 1rem;
}
</style>
