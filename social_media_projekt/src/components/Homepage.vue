<template>
  <div class="row mx-auto">
    <div class="account-info">
      <div class="title">
        <img
          v-if="this.profileImageUrl == null"
          src="../assets/blank_profile_pic.webp"
          alt="Kein Profilbild"
          class="profile-picture" />
        <img
          v-else
          :src="this.profileImageUrl"
          alt="Profilbild"
          class="profile-picture" />
        <div>{{ username }}</div>
      </div>
    </div>
    <PostCreator class="col-md-6" style="margin-left: 25%" />
    <FriendsList :friends="friendsList" />
  </div>
  <FriendsMap
    v-if="userLocation && userLocation.length === 2 && friendsList.length > 0"
    :user="userLocation"
    :friendsList="this.$store.state.friendsList"
    class="map-container"></FriendsMap>
  <UserFeed v-if="friendsList.length >= 0" class="userFeed"></UserFeed>
</template>
<script>
import axios from "axios";
import FriendsList from "./Friendslist.vue";
import PostCreator from "./postCreator.vue";
import FriendsMap from "./map.vue";
import UserFeed from "./UserFeed.vue";
import { watch } from "vue";

export default {
  name: "HomePage",
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
      email: "fredmetzler@battlenet.com",
      role: "CEO",
      userLocation: [],
      friendsList: [],
      profileImageUrl: null,
      userObject: null,
    };
  },
  // in the mounted lifecycle we prevent the global drop event so that users don't get annoying behaviour when importing images
  async mounted() {
    document.addEventListener("drop", this.preventGlobalDrop, false);
    await this.fetchUserLocation();
    await this.fetchUserData();
    watch(
      () => this.$store.state.friendsList,
      (newVal) => {
        if (newVal.length > 0) {
          this.friendsList = newVal;
        }
      },
      { immediate: true }
    );
  },
  beforeUnmount() {
    document.removeEventListener("drop", this.preventGlobalDrop, false);
  },
  computed: {
    preventGlobalDrop() {
      return function (event) {
        event.preventDefault();
        event.stopPropagation();
      };
    },
  },
  methods: {
    // method to get initial Userdata
    async fetchUserData() {
      try {
        const response = await axios.get(
          this.$store.state.API + `/users/${this.$store.state.logged_user_id}`
        );
        this.userObject = response.data;
        if (this.userObject.photo_id != null) {
          try {
            this.profileImageUrl = await this.getPhoto(
              this.userObject.photo_id
            );
          } catch (error) {
            console.log(error);
          }
        }
      } catch (error) {
        console.log(error);
      }
    },
    // method to get the location of the logged user based on his login
    async fetchUserLocation() {
      const userId = this.$store.state.logged_user_id;
      try {
        const response = await axios.get(
          this.API + `/get_user_location/${userId}`
        );
        this.userLocation = [
          response.data.location.lat,
          response.data.location.lng,
        ];
        this.friendsList = this.$store.getters.getFriends;
      } catch (error) {
        console.log(error);
      }
    },
    async getPhoto(photoId) {
      try {
        const response = await axios.get(this.$store.state.API + `/getPhoto`, {
          params: { id: photoId },
          responseType: "arraybuffer",
        });
        const base64 = btoa(
          new Uint8Array(response.data).reduce(
            (data, byte) => data + String.fromCharCode(byte),
            ""
          )
        );
        const imageSrc = `data:image/png;base64,${base64}`;
        return imageSrc;
      } catch (error) {
        console.error("Error fetching posts:", error);
      }
    },
  },
};
</script>

<style scoped>
.row {
  background-color: #3c4e74;
}

.map-container {
  position: fixed;
  right: 4vh;
  bottom: 5vh;
}

.account-info {
  position: fixed;
  top: 10vh;
  background-color: #142957;
  color: white;
  padding: 80px;
  width: 16%;
  height: 100%;
  z-index: 1;
  display: flex;
  flex-direction: column;
  justify-content: top;
  align-items: center;
  border-radius: 8px;
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

.userFeed {
  z-index: 1;
  background-color: #3c4e74;
  padding: 40px;
  min-height: 70vh;
}
</style>
