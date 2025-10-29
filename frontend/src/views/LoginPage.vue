<template>
  <div class="login-container">
    <form @submit.prevent="handleLogin" class="login-form">
      <h2>{{ $t('auth.login') }}</h2>
      <div class="form-group">
        <label for="username">{{ $t('auth.username') }}:</label>
        <input type="text" id="username" v-model="username" required>
      </div>
      <div class="form-group">
        <label for="password">{{ $t('auth.password') }}:</label>
        <input type="password" id="password" v-model="password" required>
      </div>
      <button type="submit" class="login-button" :disabled="loading">{{ loading ? $t('common.loading') : $t('auth.login') }}</button>
      <p v-if="error" class="error-message">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const error = ref(null)
const loading = ref(false)
const router = useRouter()

const handleLogin = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await fetch('/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
      }),
    })

    if (!response.ok) {
      const errData = await response.json()
      throw new Error(errData.message || t('auth.loginFailed'))
    }

    // For simplicity, store a flag in localStorage
    localStorage.setItem('isLoggedIn', 'true')
    router.push('/admin') // Redirect to admin dashboard
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh; /* Adjust as needed */
}

.login-form {
  background-color: var(--card-background-color);
  padding: 3rem;
  border-radius: var(--card-border-radius);
  box-shadow: var(--card-shadow);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

.login-form h2 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 2rem;
  color: var(--primary-text-color);
}

.form-group {
  margin-bottom: 1.5rem;
  text-align: left;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: var(--primary-text-color);
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  font-size: 1rem;
  background-color: var(--background-color);
  color: var(--primary-text-color);
}

.login-button {
  width: 100%;
  padding: 1rem;
  border: none;
  border-radius: 8px;
  background-color: var(--accent-color);
  color: white;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s ease;
  margin-top: 1rem;
}

.login-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.login-button:hover:not(:disabled) {
  opacity: 0.9;
}

.error-message {
  color: var(--accent-color);
  margin-top: 1.5rem;
  font-size: 0.9rem;
}
</style>
const { t } = useI18n()
