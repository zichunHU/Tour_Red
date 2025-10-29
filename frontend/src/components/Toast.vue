<template>
  <div v-if="visible" class="toast" :class="type">
    <span>{{ message }}</span>
    <button class="close" @click="$emit('close')">×</button>
  </div>
</template>

<script setup>
defineProps({
  message: { type: String, default: '' },
  type: { type: String, default: 'error' },
  visible: { type: Boolean, default: false }
})
defineEmits(['close'])
</script>

<style scoped>
.toast {
  position: fixed;
  right: 20px;
  bottom: 20px;
  background: var(--card-background-color);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  box-shadow: var(--card-shadow);
  padding: 0.75rem 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.toast.error { border-color: var(--accent-color); }
.close {
  border: none;
  background: transparent;
  font-size: 1.2rem;
  cursor: pointer;
  color: var(--secondary-text-color);
}
.close:hover { color: var(--primary-text-color); }
</style>