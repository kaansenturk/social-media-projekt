<template>
  <div :class="{ 'popup-mode': isPopupMode, animate: isPopupMode }" id="map">
    <LMap
      :zoom="mapOptions.zoom"
      :center="mapOptions.center"
      ref="mapRef"
      @ready="fitBounds"
      :zoom-control="true">
      <LTileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      <LMarker v-if="userLatLng[0] !== null" :lat-lng="userLatLng" title="You">
      </LMarker>
      <LMarker
        v-for="friend in processedFriends"
        :key="friend.id"
        :lat-lng="friend.latlng"
        :title="friend.name"
        @click="visitFriend(friend)">
      </LMarker>
    </LMap>

    <button
      v-if="userLatLng[0] !== null"
      class="map-button"
      @click="centerOnUser">
      Find me
    </button>
    <button class="map-button" @click="zoomIn">
      <i class="fa-solid fa-magnifying-glass-plus"></i>
    </button>
    <button class="map-button" @click="zoomOut">
      <i class="fa-solid fa-magnifying-glass-minus"></i>
    </button>
    <button class="map-button" @click="toggleMapMode">
      {{ isPopupMode ? "Minimize" : "Maximize" }}
    </button>
  </div>
</template>

<script>
import { LMap, LTileLayer, LMarker } from "vue3-leaflet";
import L from "leaflet";
import { ref, computed, watchEffect } from "vue";
import "leaflet/dist/leaflet.css";
import { useRouter } from "vue-router";

export default {
  name: "FriendsMap",
  components: {
    LMap,
    LTileLayer,
    LMarker,
  },
  props: {
    user: { type: Array, required: true },
    friendsList: {
      type: Array,
      required: true,
      default() {
        [
          {
            email: "fred@fred",

            location: { location: { lat: 0, lng: 0 } },
            userId: 1,
            username: "fred",
          },
        ];
      },
    },
  },

  // Setup function for the map to be initialized
  setup(props) {
    // VUE passes a proxy object so to handle it we convert it into a regular object
    const plainFriendsList = ref([]);
    watchEffect(() => {
      plainFriendsList.value = props.friendsList.map((friend) => {
        return JSON.parse(JSON.stringify(friend));
      });
    });
    console.log(plainFriendsList);
    const mapOptions = {
      zoom: 12,
      center: [53.5587, 9.9276],
    };

    const mapRef = ref(null);
    const marker = ref(null);
    const isPopupMode = ref(false);
    // Wanted to implement nicely looking markers, but vue3-leaflet does not seem to support this option.
    //   const brightGreenIcon =
    //   L.icon({
    //     iconUrl: '../assets/greenIcon.png',
    //     iconSize: [20, 41],
    //     iconAnchor: [12, 41],
    //     popupAnchor: [1, -34],
    //     shadowSize: [41, 41],
    //   })
    // ;
    // const darkBlueIcon =
    //   L.icon({
    //     iconUrl:'../assets/blueIcon.png',
    //     iconSize: [25, 41],
    //     iconAnchor: [12, 41],
    //     popupAnchor: [1, -34],
    //     shadowSize: [41, 41],
    //   })
    // ;
    // set the initial view on the map between the locations of all friends
    const bounds = computed(() => {
      let boundObj = L.latLngBounds();
      plainFriendsList.value.forEach((friend) => {
        if (friend.location.location.lat && friend.location.location.lng) {
          boundObj.extend([
            friend.location.location.lat,
            friend.location.location.lng,
          ]);
        }
      });
      return boundObj;
    });
    const fitBounds = () => {
      if (mapRef.value && bounds.value.isValid()) {
        mapRef.value.fitBounds(bounds.value);
      }
    };
    // converting friends to the objecttype we call in the map itself
    const processedFriends = plainFriendsList.value
      .filter(
        (friend) =>
          friend.location.location.lat !== null &&
          friend.location.location.lng !== null
      )
      .map((friend, idx) => {
        return {
          id: idx,
          latlng: [friend.location.location.lat, friend.location.location.lng],
          name: friend.username,
          email: friend.email,
          userId: friend.userId,
        };
      });
    // setting the location for the user based on the prop
    console.log(props.user);
    const userLatLng = [props.user[0], props.user[1]];
    const toggleMapMode = () => {
      isPopupMode.value = !isPopupMode.value;
    };
    // functions for the buttons to zoom in and out and to center the view on the users location
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
    const router = useRouter();
    const visitFriend = (friend) => {
      console.log(friend);
      const friendId = friend.userId;
      const username = friend.name;
      const email = friend.email;
      router.push({ name: "friend", query: { friendId, username, email } });
    };
    return {
      toggleMapMode,
      isPopupMode,
      mapOptions,
      processedFriends,
      marker,
      fitBounds,
      mapRef,
      zoomIn,
      zoomOut,
      centerOnUser,
      userLatLng,
      visitFriend,
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
  top: 10.8%;
  left: 10%;
  right: 10%;
  bottom: 10%;
  width: 80vw;
  height: 80vh;
  z-index: 1000;
}

.animate {
  -webkit-animation: animatezoom 0.6s;
  animation: animatezoom 0.6s;
}

@-webkit-keyframes animatezoom {
  from {
    -webkit-transform: scale(0);
  }
  to {
    -webkit-transform: scale(1);
  }
}

@keyframes animatezoom {
  from {
    transform: scale(0);
  }
  to {
    transform: scale(1);
  }
}

.map-button {
  border-radius: 7px;
  background-color: #2200cd;
  color: #fff;
}
</style>
