<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import { useI18n } from 'vue-i18n'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  name: { type: String, default: '' },
  nameSecondary: { type: String, default: '' },
  address: { type: String, default: '' },
  addressSecondary: { type: String, default: '' },
})
const emit = defineEmits(['update:modelValue'])
const { t } = useI18n()

const visible = ref(props.modelValue)
watch(() => props.modelValue, v => visible.value = v)
watch(visible, v => emit('update:modelValue', v))

const scale = ref(1)
const minScale = 0.9
const maxScale = 1.4
let pinchStartDist = null

function close() { visible.value = false }

async function copyAddress() {
  try {
    if (props.address) {
      await navigator.clipboard.writeText(props.address)
      // Optional: lightweight feedback
    }
  } catch {}
}

function onOverlayClick(e) {
  if (e.target === e.currentTarget) close()
}

function onKeydown(e) {
  if (e.key === 'Escape') close()
}

function distance(touches) {
  const [a, b] = touches
  const dx = a.clientX - b.clientX
  const dy = a.clientY - b.clientY
  return Math.hypot(dx, dy)
}

function onTouchStart(e) {
  if (e.touches.length === 2) {
    pinchStartDist = distance(e.touches)
  }
}

function onTouchMove(e) {
  if (e.touches.length === 2 && pinchStartDist) {
    e.preventDefault()
    const d = distance(e.touches)
    const factor = d / pinchStartDist
    const next = Math.min(maxScale, Math.max(minScale, factor))
    scale.value = next
  }
}

function onTouchEnd(e) {
  if (e.touches.length < 2) {
    pinchStartDist = null
  }
}

function zoomIn() { scale.value = Math.min(maxScale, scale.value + 0.05) }
function zoomOut() { scale.value = Math.max(minScale, scale.value - 0.05) }

onMounted(() => {
  window.addEventListener('keydown', onKeydown)
})
onBeforeUnmount(() => {
  window.removeEventListener('keydown', onKeydown)
})
</script>

<template>
  <transition name="wf-fade">
    <div v-if="visible" class="wf-overlay" @click="onOverlayClick">
      <transition name="wf-zoom">
        <div
          class="wf-card"
          :style="{ transform: `scale(${scale})` }"
          @touchstart.passive="onTouchStart"
          @touchmove="onTouchMove"
          @touchend="onTouchEnd"
          role="dialog"
          aria-modal="true"
        >
          <div class="wf-head">
            <div class="wf-title">{{ name || t('attractions.name') }}</div>
          <button class="wf-close" @click="close" :aria-label="t('common.cancel')">✕</button>
          </div>
          <div class="wf-subtitle" v-if="nameSecondary">{{ nameSecondary }}</div>
          <div class="wf-address" :title="address">{{ address }}</div>
          <div class="wf-address secondary" v-if="addressSecondary">{{ addressSecondary }}</div>
          <div class="wf-actions">
            <button class="wf-btn" @click="copyAddress">{{ t('map.copyAddress') }}</button>
            <div class="wf-spacer"></div>
            <button class="wf-btn" @click="zoomOut">−</button>
            <button class="wf-btn" @click="zoomIn">＋</button>
          </div>
        </div>
      </transition>
    </div>
  </transition>
</template>

<style scoped>
.wf-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.45);
  display: grid;
  place-items: center;
  z-index: 1000;
  padding: 1rem;
}
.wf-card {
  width: min(1200px, 96vw);
  border-radius: 16px;
  background: #ffffff;
  color: #111;
  box-shadow: 0 12px 40px rgba(0,0,0,0.25);
  padding: 1.25rem;
  transition: transform 0.18s ease;
  max-height: 90vh;
  overflow: auto;
}
.wf-head { display: flex; align-items: center; gap: 0.75rem; }
.wf-title {
  font-size: clamp(1.1rem, 2.6vw, 1.6rem);
  font-weight: 800;
  line-height: 1.2;
  color: #111;
}
.wf-subtitle {
  margin-top: 0.25rem;
  font-size: clamp(0.95rem, 2.1vw, 1.15rem);
  color: #333;
}
.wf-close {
  margin-left: auto;
  border: none;
  background: #111;
  color: #fff;
  border-radius: 10px;
  width: 36px;
  height: 36px;
  cursor: pointer;
}
.wf-address {
  margin-top: 0.5rem;
  font-size: clamp(1rem, 2.2vw, 1.2rem);
  color: #222;
}
.wf-address.secondary { color: #444; }
.wf-actions { display: flex; align-items: center; gap: 0.5rem; margin-top: 0.9rem; }
.wf-spacer { flex: 1; }
.wf-btn {
  border: 1px solid #111;
  background: #fff;
  color: #111;
  border-radius: 999px;
  padding: 0.45rem 0.8rem;
  cursor: pointer;
}

/* Animations */
.wf-fade-enter-active, .wf-fade-leave-active { transition: opacity 0.18s ease; }
.wf-fade-enter-from, .wf-fade-leave-to { opacity: 0; }
.wf-zoom-enter-active, .wf-zoom-leave-active { transition: transform 0.2s ease, opacity 0.2s ease; }
.wf-zoom-enter-from, .wf-zoom-leave-to { transform: scale(0.96); opacity: 0; }

@media (max-width: 480px) {
  .wf-card { padding: 1rem; }
  .wf-close { width: 32px; height: 32px; }
}
</style>