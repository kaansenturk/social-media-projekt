<template>
  <div class="row">
    <div class="col-md-2 account-info">
      <div class="title">
        <img v-if="this.profileImageUrl == null" src="../assets/blank_profile_pic.webp" alt="Kein Profilbild" class="profile-picture" />
        <img v-else :src="this.profileImageUrl" alt="Profilbild" class="profile-picture">
        <div>{{ username }}</div>
      </div>
    </div>
    <PostCreator class="col-md-7"/>
    <FriendsList class="col-md-2" :friends="friendsList"/>
  </div>
  <FriendsMap v-if="userLocation && userLocation.length ===  2 && friendsList.length > 0" :user="userLocation" :friendsList="this.$store.state.friendsList" class="map-container"></FriendsMap>
  <UserFeed v-if="friendsList.length > 0"></UserFeed>
</template>
<script>
import axios from 'axios';
import FriendsList from "./Friendslist.vue";
import PostCreator from "./postCreator.vue";
import FriendsMap from "./map.vue";
import UserFeed from './UserFeed.vue';
import { watch } from 'vue';

export default {
  name: 'HomePage',
  components: {
    FriendsList,
    PostCreator,
    FriendsMap,
    UserFeed,
  },
  data() {
    return {
      user: this.$store.state.logged_user_id,
      username: this.$store.state.logged_user,
      API: this.$store.state.API,
      email: 'fredmetzler@battlenet.com',
      role: 'CEO',
      userLocation: [],
      friendsList: [],
      profileImageUrl: null, 
      userObject: null,
    };
  },
  // in the mounted lifecycle we prevent the global drop event so that users don't get annoying behaviour when importing images
  async mounted() {
    document.addEventListener('drop', this.preventGlobalDrop, false);
    await this.fetchUserLocation(); 
    await this.fetchUserData();
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
  // watch: {
  //   async profileImageUrl(newProfilePicId, oldProfilePicId) {
  //     if (newProfilePicId !== oldProfilePicId) {
  //       this.profileImageUrl = newProfilePicId
  //     }
  //   },
  // },
  methods: {
    // method to get initial Userdata
    async fetchUserData(){
      try {
        const response = await axios.get(this.$store.state.API + `/users/${this.$store.state.logged_user_id}`);
        this.userObject = response.data
        if (this.userObject.photo_id != null) {
        try {
          this.profileImageUrl = await this.getPhoto(this.userObject.photo_id)
        } catch (error){
          console.log(error)
        }
      }
      } catch (error){
        console.log(error)
      }
    },
    // method to get the location of the logged user based on his login
    async fetchUserLocation() {
      const userId = this.$store.state.logged_user_id;
      try {
        const response = await axios.get(this.API + `/get_user_location/${userId}`);
        this.userLocation = [response.data.location.lat, response.data.location.lng];
        this.friendsList = this.$store.getters.getFriends
      } catch (error) {
        console.log(error);
      }
    },
    async getPhoto(photoId) {
      try {
        const response = await axios.get(this.$store.state.API + `/getPhoto`, {params: {id: photoId}, responseType: 'arraybuffer'});
        const base64 = btoa(
        new Uint8Array(response.data).reduce(
          (data, byte) => data + String.fromCharCode(byte),
          '',
        ),
      );
      const imageSrc = `data:image/png;base64,${base64}`;
        return imageSrc
      } catch (error) {
        console.error("Error fetching posts:", error);
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
