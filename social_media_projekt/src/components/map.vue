<template>
        
        <div :class="{'popup-mode': isPopupMode}" id="map">
    <LMap :zoom="mapOptions.zoom" 
  :center="mapOptions.center"
  ref="mapRef"
  @ready="fitBounds"
  :zoom-control="true">
      <LTileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      <LMarker  
        v-for="friend in processedFriends" 
        :key="friend.id"
        :lat-lng="friend.latlng"
        :icon="darkBlueIcon"
        v-b-tooltip.hover :title="friend.name"
      >
      </LMarker>
      <LMarker  
        :lat-lng="userLatLng"
        :icon="brightGreenIcon"
        v-b-tooltip.hover title="You"
      >
      </LMarker>
    </LMap>
    <button class="map-button" @click="centerOnUser">Find me</button>
    <button class="map-button" @click="zoomIn"><i class="fa-solid fa-magnifying-glass-plus"></i></button>
<button class="map-button" @click="zoomOut"><i class="fa-solid fa-magnifying-glass-minus"></i></button>
    <button class="map-button" @click="toggleMapMode">
            {{ isPopupMode ? 'Minimieren' : 'Maximieren' }}
        </button>
  </div>
</template>

  
  <script>
  import { LMap, LTileLayer, LMarker } from 'vue3-leaflet';
  import L from 'leaflet';
  import { ref, computed } from 'vue';
  
  export default {
    name: 'FriendsMap',
    components: {
      LMap,
      LTileLayer,
      LMarker,
    },
    props: {
      user: {type: Array, required: true},
      friendsList: {type: Array, required: true,
        default: () => [{
  name: "Imaginärer Freund",
  lat: 53.5587, 
  lng: 9.9276}, {
  name: "realer Freund",
  lat: 53.7123, 
  lng: 9.9999}],},
    },
    setup(props) {

        
      const mapOptions = {
        zoom: 12,
        center: [53.5587, 9.9276], 
      };

      const mapRef = ref(null);
      const marker = ref(null);
      const isPopupMode = ref(false);

      const darkBlueIcon = new L.Icon({
      iconUrl: 'path_to_dark_blue_icon.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41],
    });
    const brightGreenIcon = new L.Icon({
      iconUrl: 'brightGreenIcon.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41],
    });
    const bounds = computed(() => {
    let boundObj = L.latLngBounds();
    props.friendsList.forEach(friend => {
      boundObj.extend([friend.lat, friend.lng]);
    });
    return boundObj;
  });
  const fitBounds = () => {
    if (mapRef.value && bounds.value.isValid()) {
      mapRef.value.fitBounds(bounds.value);
    }
  };
    const processedFriends = props.friendsList.map((friend, idx) => {
      return {
        id: idx,
        latlng: [friend.lat, friend.lng],
        name: friend.name 
      };
    });
    const userLatLng = [props.user[0], props.user[1]]
    const toggleMapMode = () => {
    isPopupMode.value = !isPopupMode.value;
};
const zoomIn = () => {
    if (mapRef.value) {
        const currentZoom = mapRef.value.getZoom();
        mapRef.value.setZoom(currentZoom + 1);
    }
};

const zoomOut = () => {
    if (mapRef.value) {
        const currentZoom = mapRef.value.getZoom();
        mapRef.value.setZoom(currentZoom - 1);
    }
};
const centerOnUser = () => {
    if (mapRef.value) {
      mapRef.value.setView(userLatLng);
    }
};

    return {
      toggleMapMode,
      isPopupMode,
      mapOptions,
      darkBlueIcon,
      brightGreenIcon,
      processedFriends,
      marker,
    fitBounds,
    mapRef,
    zoomIn,
    zoomOut,
    centerOnUser,
    userLatLng,
    };
  
    },
  };
  </script>
  
  <style>
  #map {
    width: 22%;
    height: 25%;
    margin-right: 3px;
  }
  #map.popup-mode {
    position: fixed;
    top: 10%;
    left: 10%;
    right: 10%;
    bottom: 10%;
    width: 80vw;  /* viewport width */
    height: 80vh; /* viewport height */
    z-index: 1000; /* high z-index to ensure it's on top */
    background-color: rgba(255, 255, 255, 0.9); /* Optional: slightly white background to make underlying content less prominent */
}
.map-button {
  border-radius: 7px;
  background-color: #2200cd;
  color: #fff;
}
  </style>
  