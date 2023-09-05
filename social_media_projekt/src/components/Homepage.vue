<template>
  <div class="row">
    <div class="col-md-2 account-info">
      <div class="title">
        <img :src="profileImageUrl" alt="Profilbild" class="profile-picture" />
        <div>{{ username }}</div>
      </div>
    </div>
    <PostCreator class="col-md-7"/>
    <FriendsList class="col-md-2" :friends="friendsList"/>
  </div>
  <FriendsMap v-if="userLocation && userLocation.length ===  2 && friendsList.length > 0" :user="userLocation" :friendsList="this.$store.state.friendsList" class="map-container"></FriendsMap>
</template>
<script>
import axios from 'axios';
import FriendsList from "./Friendslist.vue";
import PostCreator from "./postCreator.vue";
import FriendsMap from "./map.vue";
import { watch } from 'vue';

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
      userLocation: [],
      friendsList: [],
      profileImageUrl: 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png', 
    };
  },
  // in the mounted lifecycle we prevent the global drop event so that users don't get annoying behaviour when importing images
  async mounted() {
    document.addEventListener('drop', this.preventGlobalDrop, false);
    await this.fetchUserLocation(); 
    watch(() => this.$store.state.friendsList, (newVal) => {
      if (newVal.length > 0) {
        this.friendsList = newVal;
      }
    }, { immediate: true });
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
    // method to get the location of the logged user based on his login
    async fetchUserLocation() {
      const userId = this.$store.state.logged_user_id;
      try {
        const response = await axios.get(`http://localhost:8000/get_user_location/${userId}`);
        this.userLocation = [response.data.location.lat, response.data.location.lng];
        this.friendsList = this.$store.getters.getFriends
      } catch (error) {
        console.log("An error occurred:", error);
      }
    },
  },
};
</script>
    
<style scoped>
.map-container {
  position: fixed; right: 1vh; bottom: 4vh;
  width: 15%;
}
.account-info {
  background-color: #2200cd;
  color: white;
  padding: 35px;
  margin-left: 15px;
  height: fit-content;
}

.title {
  font-size: 24px;
  margin-bottom: 10px;
}

.info-item {
  margin-bottom: 5px;
}


.profile-picture {
  width: 70px; 
  height: 70px; 
  border-radius: 50%;
  margin-bottom: 10px; 
}
</style>
