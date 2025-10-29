<template>
  <button
    class="chip"
    :class="{ selected }"
    type="button"
    role="button"
    :aria-pressed="selected"
    @click="$emit('toggle')"
  >
    <slot />
  </button>
</template>

<script setup>
defineProps({ selected: { type: Boolean, default: false } })
defineEmits(['toggle'])
</script>

<style scoped>
.chip {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.9rem;
  border-radius: 10px;
  border: 1px solid var(--border-color);
  background: var(--background-color);
  color: var(--primary-text-color);
  font-weight: 600;
  cursor: pointer;
  transition: background 150ms ease, color 150ms ease, border-color 150ms ease;
}
.chip:hover { background: #e5e5ea; }
.chip.selected {
  background: var(--accent-color);
  border-color: var(--accent-color);
  color: #fff;
}
</style>