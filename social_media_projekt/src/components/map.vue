<template>
    <div id="map" style="height: 400px;"></div>
    <LMap :zoom="mapOptions.zoom" :center="mapOptions.center">
  <LTileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
  <LMarker :lat-lng="mapOptions.center"></LMarker>
</LMap>
  </template>
  
  <script>
 // import { ref, onMounted } from 'vue';
  import { LMap, LTileLayer, LMarker } from 'vue3-leaflet';
  
  export default {
    name: 'FriendsMap',
    components: {
      LMap,
      LTileLayer,
      LMarker,
    },
    setup() {
      const mapOptions = {
        zoom: 13,
        center: [54.001, 9.6123], 
      };
  
      return {
        mapOptions,
      };
    },
  };
  </script>
  
  <style>
  /* You can add some styling for the map container here */
  #map {
    width: 20%;
  }
  </style>
  