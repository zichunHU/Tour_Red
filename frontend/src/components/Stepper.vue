<template>
  <div class="stepper">
    <div v-for="(s, i) in steps" :key="s.key" class="step">
      <div class="dot" :class="{ active: s.key === current }"></div>
      <span class="label" :class="{ active: s.key === current }">{{ s.label }}</span>
      <div v-if="i < steps.length - 1" class="divider"></div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  steps: { type: Array, required: true }, // [{ key:'selection', label:'选择' }, ...]
  current: { type: String, required: true }
})
</script>

<style scoped>
.stepper {
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--card-background-color);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 0.5rem 1rem;
  margin-bottom: 1.5rem;
}
.step {
  display: flex;
  align-items: center;
}
.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--border-color);
  transition: background 150ms ease;
}
.dot.active { background: var(--accent-color); }
.label {
  margin-left: 0.5rem;
  margin-right: 0.75rem;
  color: var(--secondary-text-color);
  font-weight: 600;
}
.label.active { color: var(--primary-text-color); }
.divider {
  width: 24px;
  height: 2px;
  background: var(--border-color);
  margin: 0 0.75rem;
}
</style>