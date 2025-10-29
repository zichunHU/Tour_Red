<template>
  <div ref="mapContainer" class="map-viewer"></div>
  <div v-if="!amapLoaded" class="map-fallback">{{ $t('map.loadError') }}</div>
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted } from 'vue';

const props = defineProps({
  latitude: Number,
  longitude: Number,
  waypoints: {
    type: Array,
    default: () => []
  },
  selectedIds: { // Set of selected waypoint IDs
    type: Set,
    default: () => new Set()
  },
  interactionEnabled: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['marker-click']);

const mapContainer = ref(null);
const amapLoaded = ref(false);
let map = null; // To hold the map instance
const markers = []; // To keep track of added markers
let resizeObserver = null; // Observe container size changes
let lastView = { type: 'none', points: [] }; // Track current view mode for refitting on resize

// A reactive ref to hold a normalized list of points
const points = ref([]);

// Watch for any prop changes and update the internal 'points' array
watch(() => [props.latitude, props.longitude, props.waypoints], () => {
  const newPoints = [];
  if (props.latitude && props.longitude) {
    newPoints.push({ latitude: props.latitude, longitude: props.longitude });
  } else if (props.waypoints && props.waypoints.length > 0) {
    newPoints.push(...props.waypoints);
  }
  points.value = newPoints;
}, { immediate: true, deep: true });

const initMap = () => {
  if (typeof AMap === 'undefined') {
    console.error('AMap SDK is not loaded.');
    amapLoaded.value = false;
    return;
  }
  amapLoaded.value = true;
  const rect = mapContainer.value?.getBoundingClientRect();
  console.debug('[MapViewer] initMap container rect:', rect, 'DPR:', window.devicePixelRatio);
  map = new AMap.Map(mapContainer.value, {
    zoom: 11,
    viewMode: '3D',
    resizeEnable: true,
    center: [121.4737, 31.2304]
  });
  updateMap(points.value);
  // Ensure map reflows when container size changes
  if (mapContainer.value && typeof ResizeObserver !== 'undefined') {
    resizeObserver = new ResizeObserver(() => {
      if (map) {
        console.debug('[MapViewer] ResizeObserver trigger: resizing map');
        map.resize();
        // Refit view after resize to avoid perceived marker drift
        refitView();
      }
    });
    resizeObserver.observe(mapContainer.value);
  }
  // Additional resilience: handle orientation and visibility changes
  window.addEventListener('orientationchange', () => { if (map) { map.resize(); refitView(); } });
  document.addEventListener('visibilitychange', () => { if (!document.hidden && map) { map.resize(); refitView(); } });
};

const updateMap = (currentPoints) => {
  if (!map) return;

  map.clearMap();
  markers.length = 0;

  if (!currentPoints || currentPoints.length === 0) return;

  const amapPoints = currentPoints.map(p => {
    const lat = p.location ? p.location.latitude : p.latitude;
    const lon = p.location ? p.location.longitude : p.longitude;
    return {...p, lnglat: new AMap.LngLat(lon, lat)};
  });

  if (amapPoints.length === 1 && !props.interactionEnabled) {
    // Original single point logic (non-interactive)
    map.setCenter(amapPoints[0].lnglat);
    map.setZoom(15);
    const marker = new AMap.Marker({
      position: amapPoints[0].lnglat,
      anchor: 'bottom-center'
    });
    map.add(marker);
    lastView = { type: 'single', points: amapPoints };
  } else if (amapPoints.length > 1 && !props.interactionEnabled) {
    // Original multi-point route planning logic
    const driving = new AMap.Driving({ map: map, policy: AMap.DrivingPolicy.LEAST_TIME });
    const start = amapPoints[0].lnglat;
    const end = amapPoints[amapPoints.length - 1].lnglat;
    const waypoints = amapPoints.slice(1, -1).map(p => p.lnglat);
    driving.search(start, end, { waypoints: waypoints }, (status, result) => {
      if (status !== 'complete') console.error('Failed to get driving route:', result);
    });
    lastView = { type: 'route', points: amapPoints };
  } else {
    // New interactive marker logic
    amapPoints.forEach(point => {
      const isSelected = props.selectedIds.has(point.id);
      const marker = new AMap.Marker({
        position: point.lnglat,
        icon: new AMap.Icon({
          size: isSelected ? new AMap.Size(30, 40) : new AMap.Size(25, 34),
          image: isSelected ? '//a.amap.com/jsapi_demos/static/demo-center/icons/poi-marker-red.png' : '//a.amap.com/jsapi_demos/static/demo-center/icons/poi-marker-default.png',
          imageSize: isSelected ? new AMap.Size(30, 40) : new AMap.Size(25, 34),
        }),
        anchor: 'bottom-center',
        extData: { id: point.id } // Store ID for click events
      });

      if (props.interactionEnabled) {
        marker.on('click', (e) => {
          emit('marker-click', e.target.getExtData().id);
        });
      }
      markers.push(marker);
    });
    map.add(markers);
    if (markers.length > 0) {
      map.setFitView(markers);
    }
    lastView = { type: 'markers', points: amapPoints };
  }
  const size = map.getSize();
  console.debug('[MapViewer] updateMap points:', amapPoints.length, 'map size:', size?.width, size?.height, 'DPR:', window.devicePixelRatio);
};

const refitView = () => {
  if (!map) return;
  if (lastView.type === 'single' && lastView.points.length) {
    map.setCenter(lastView.points[0].lnglat);
  } else if (lastView.type === 'markers' && markers.length) {
    map.setFitView(markers);
  } else if (lastView.type === 'route') {
    // Driving layer manages its own view; calling resize is sufficient
  }
};

onMounted(() => {
  setTimeout(initMap, 150);
  // Fallback: resize on window size changes
  const onWindowResize = () => { if (map) map.resize(); };
  window.addEventListener('resize', onWindowResize);
  // Cleanup on unmount
  onUnmounted(() => {
    window.removeEventListener('resize', onWindowResize);
    if (resizeObserver && mapContainer.value) {
      try { resizeObserver.unobserve(mapContainer.value); } catch {}
      resizeObserver = null;
    }
  });
});

// Watch for changes in points or selectedIds to update the map
watch([points, () => props.selectedIds], () => {
  if (map) updateMap(points.value);
}, { deep: true });


</script>

<style scoped>
.map-viewer {
  width: 100%;
  height: 100%; /* Fill parent container height */
  min-height: 360px; /* Sensible minimum to avoid collapse */
  position: relative; /* Ensure proper absolute child positioning */
  display: block;
  border-radius: var(--card-border-radius);
}
.map-fallback {
  margin-top: 0.5rem;
  color: var(--secondary-text-color);
  font-size: 0.85rem;
}
</style>
