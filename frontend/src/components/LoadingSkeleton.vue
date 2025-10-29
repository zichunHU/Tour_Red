<template>
  <div class="skeleton-grid">
    <div v-for="n in count" :key="n" class="skeleton-card">
      <div class="image"></div>
      <div class="line short"></div>
      <div class="line"></div>
    </div>
  </div>
</template>

<script setup>
defineProps({ count: { type: Number, default: 6 } })
</script>

<style scoped>
.skeleton-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}
.skeleton-card {
  background: var(--card-background-color);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1rem;
}
.image {
  height: 140px;
  background: linear-gradient(90deg, #eee, #f5f5f5, #eee);
  border-radius: 8px;
  animation: shimmer 1.2s infinite;
}
.line {
  height: 12px;
  background: linear-gradient(90deg, #eee, #f5f5f5, #eee);
  border-radius: 6px;
  margin-top: 12px;
  animation: shimmer 1.2s infinite;
}
.line.short { width: 60%; }

@keyframes shimmer {
  0% { background-position: -200px 0; }
  100% { background-position: 200px 0; }
}
</style>