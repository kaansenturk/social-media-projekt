<template>
    <div class="row">
      <div class="col-md-2 account-info">
        <h2 class="title">Account Information</h2>
        <div class="info-item">
          <strong>Username:</strong> {{ username }}
        </div>
        <div class="info-item">
          <strong>Email:</strong> {{ email }}
        </div>
        <div class="info-item">
          <strong>Role:</strong> {{ role }}
        </div>
      </div>
      <PostCreator class="col-md-7"/>
      <FriendsList class="col-md-2" :friends="friendsList"/>
    </div>
      <FriendsMap v-if="userLocation && userLocation.length === 2" :user="this.userLocation" class="map-container"></FriendsMap>
    </template>
    <script>
import axios from 'axios';
import FriendsList from "./Friendslist.vue";
import PostCreator from "./postCreator.vue";
import FriendsMap from "./map.vue";

export default {
  name: 'HomePage',
  components: {
    FriendsList,
    PostCreator,
    FriendsMap,
  },
  data() {
    return {
      user: this.$store.state.logged_user_id,
      username: this.$store.state.logged_user,
      email: 'fredmetzler@battlenet.com',
      role: 'CEO',
      friendsList: [
        { id: 1, name: "Daniel" },
        { id: 2, name: "Johann" },
        { id: 3, name: "Kaan" },
      ],
      userLocation: [],  // Add this line to store user location
    };
  },
  async mounted() {
    document.addEventListener('drop', this.preventGlobalDrop, false);
    await this.fetchUserLocation();  // Fetch the user location when the component mounts
  },
  beforeUnmount() {
    document.removeEventListener('drop', this.preventGlobalDrop, false);
  },
  computed: {
    preventGlobalDrop() {
      return function(event) {
        event.preventDefault();
        event.stopPropagation();
      }
    },
  },
  methods: {
    fetchData() {
      // Datenzugriff regeln
    },
    async fetchUserLocation() {
      const userId = this.$store.state.logged_user_id;
      try {
        const response = await axios.get(`http://localhost:8000/get_user_location/${userId}`);
        console.log(response.data.location.lat, response.data.location.lng)
        this.userLocation = [response.data.location.lat, response.data.location.lng];
      } catch (error) {
        console.log("An error occurred:", error);
      }
    },
  },
};
</script>
    
    <style scoped>
    .map-container {
      position: fixed; ; right: 1vh;
      width: 15%;
    }
    .account-info {
      background-color: #2200cd;
      color: white;
      padding: 35px;
      margin-left: 15px;
    }
    
    .title {
      font-size: 24px;
      margin-bottom: 10px;
    }
    
    .info-item {
      margin-bottom: 5px;
    }
    </style>
    