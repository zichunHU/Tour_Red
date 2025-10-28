<template>
  <div ref="mapContainer" class="map-viewer"></div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';

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
let map = null; // To hold the map instance
const markers = []; // To keep track of added markers

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
    return;
  }
  map = new AMap.Map(mapContainer.value, {
    zoom: 11, // Adjusted default zoom
    viewMode: '3D',
    center: [121.4737, 31.2304] // Center on Shanghai
  });
  updateMap(points.value);
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
    const marker = new AMap.Marker({ position: amapPoints[0].lnglat, offset: new AMap.Pixel(-13, -30) });
    map.add(marker);
  } else if (amapPoints.length > 1 && !props.interactionEnabled) {
    // Original multi-point route planning logic
    const driving = new AMap.Driving({ map: map, policy: AMap.DrivingPolicy.LEAST_TIME });
    const start = amapPoints[0].lnglat;
    const end = amapPoints[amapPoints.length - 1].lnglat;
    const waypoints = amapPoints.slice(1, -1).map(p => p.lnglat);
    driving.search(start, end, { waypoints: waypoints }, (status, result) => {
      if (status !== 'complete') console.error('Failed to get driving route:', result);
    });
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
        offset: isSelected ? new AMap.Pixel(-15, -40) : new AMap.Pixel(-13, -34),
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
      map.setFitView();
    }
  }
};

onMounted(() => {
  setTimeout(initMap, 150);
});

// Watch for changes in points or selectedIds to update the map
watch([points, () => props.selectedIds], () => {
  if (map) updateMap(points.value);
}, { deep: true });


</script>

<style scoped>
.map-viewer {
  width: 100%;
  height: 100%; /* Changed from 400px to fill container */
  border-radius: var(--card-border-radius);
}
</style>
