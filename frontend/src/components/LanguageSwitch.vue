<template>
  <div class="language-switch">
    <button 
      @click="toggleLanguage" 
      class="language-btn"
      :title="$t('nav.language')"
    >
      <span class="flag">{{ currentFlag }}</span>
      <span class="lang-code">{{ currentLangName }}</span>
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { setLocale, getCurrentLocale, getSupportedLocales } from '@/locales'

const { locale } = useI18n()

const supportedLocales = getSupportedLocales()

const currentLocale = computed(() => getCurrentLocale())

const currentFlag = computed(() => {
  const current = supportedLocales.find(l => l.code === currentLocale.value)
  return current?.flag || '🌐'
})

const currentLangName = computed(() => {
  const current = supportedLocales.find(l => l.code === currentLocale.value)
  return current?.name || 'Language'
})

const toggleLanguage = () => {
  const currentIndex = supportedLocales.findIndex(l => l.code === currentLocale.value)
  const nextIndex = (currentIndex + 1) % supportedLocales.length
  const nextLocale = supportedLocales[nextIndex].code
  
  setLocale(nextLocale)
}
</script>

<style scoped>
.language-switch {
  display: inline-block;
}

.language-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
  font-weight: 500;
}

.language-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
  transform: translateY(-1px);
}

.language-btn:active {
  transform: translateY(0);
}

.flag {
  font-size: 16px;
  line-height: 1;
}

.lang-code {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* 深色主题适配 */
@media (prefers-color-scheme: dark) {
  .language-btn {
    background: rgba(0, 0, 0, 0.3);
    border-color: rgba(255, 255, 255, 0.1);
  }
  
  .language-btn:hover {
    background: rgba(0, 0, 0, 0.5);
    border-color: rgba(255, 255, 255, 0.2);
  }
}

/* 移动端适配 */
@media (max-width: 768px) {
  .language-btn {
    padding: 6px 10px;
    font-size: 13px;
  }
  
  .lang-code {
    display: none;
  }
}
</style>