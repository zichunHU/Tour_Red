<template>
  <div class="lang-menu" ref="menuRoot">
    <button
      class="lang-trigger"
      :title="$t('nav.language')"
      @click="toggleOpen"
      aria-haspopup="true"
      :aria-expanded="open ? 'true' : 'false'"
    >
      <span class="icon">🌐</span>
      <span class="label">{{ currentLangName }}</span>
    </button>
    <div v-if="open" class="dropdown" role="menu">
      <button
        v-for="opt in supportedLocales"
        :key="opt.code"
        class="dropdown-item"
        role="menuitemradio"
        :aria-checked="opt.code === currentLocale"
        @click="selectLocale(opt.code)"
      >
        <span class="flag">{{ opt.flag }}</span>
        <span class="name">{{ opt.name }}</span>
        <span class="check" v-if="opt.code === currentLocale">✓</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useI18n } from 'vue-i18n'
import { setLocale, getCurrentLocale, getSupportedLocales } from '@/locales'

const { t } = useI18n()

const open = ref(false)
const menuRoot = ref(null)

const supportedLocales = getSupportedLocales()
const currentLocale = computed(() => getCurrentLocale())
const currentLangName = computed(() => {
  const cur = supportedLocales.find(l => l.code === currentLocale.value)
  return cur?.name || t('nav.language')
})

function toggleOpen() { open.value = !open.value }
function closeMenu() { open.value = false }
function selectLocale(code) {
  setLocale(code)
  closeMenu()
}

function onClickOutside(e) {
  if (menuRoot.value && !menuRoot.value.contains(e.target)) {
    closeMenu()
  }
}

function onKeydown(e) {
  if (e.key === 'Escape') closeMenu()
}

onMounted(() => {
  document.addEventListener('click', onClickOutside)
  window.addEventListener('keydown', onKeydown)
})
onBeforeUnmount(() => {
  document.removeEventListener('click', onClickOutside)
  window.removeEventListener('keydown', onKeydown)
})
</script>

<style scoped>
.lang-menu {
  position: relative;
  display: inline-block;
}

.lang-trigger {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  background: var(--card-background-color);
  color: var(--primary-text-color);
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: background 0.2s ease, box-shadow 0.2s ease;
}

.lang-trigger:hover {
  background: #f7f7f9;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

.icon { font-size: 16px; }
.label { font-size: 13px; }

.dropdown {
  position: absolute;
  right: 0;
  margin-top: 8px;
  width: 180px;
  background: var(--card-background-color);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  box-shadow: var(--card-shadow);
  z-index: 1000;
  padding: 6px;
}

.dropdown-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 10px;
  border: none;
  background: transparent;
  color: var(--primary-text-color);
  cursor: pointer;
  border-radius: 8px;
  font-size: 14px;
}

.dropdown-item:hover { background: #f5f6fa; }

.flag { font-size: 16px; }
.name { flex: 1; }
.check { color: var(--accent-color); font-weight: 700; }

@media (prefers-color-scheme: dark) {
  .lang-trigger {
    background: rgba(32,32,36,0.9);
    border-color: rgba(255,255,255,0.15);
    color: #fff;
  }
  .lang-trigger:hover { background: rgba(48,48,52,0.95); }
  .dropdown {
    background: rgba(32,32,36,0.98);
    border-color: rgba(255,255,255,0.12);
  }
  .dropdown-item { color: #fff; }
  .dropdown-item:hover { background: rgba(255,255,255,0.06); }
}

@media (max-width: 768px) {
  .label { display: none; }
  .dropdown { width: 160px; }
}
</style>