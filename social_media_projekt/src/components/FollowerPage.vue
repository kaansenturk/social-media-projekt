<template>
  <div class="row">
    <div class="col-md-3 account-info">
      <div v-if="profilePicId !== null"><img class="profile-picture" :src="profilePicData"></div>
      <div v-else><img src="../assets/blank_profile_pic.webp" alt="Profilbild" class="profile-picture" /></div>
      <h2 class="title">Account Information</h2>
      <div>
        <div class="info-item">
          <strong>Username:</strong> {{ username }}
        </div>
        <div class="info-item">
          <strong>Email:</strong> {{ email }}
        </div>
        <div class="info-item">
          <strong>{{ currentList }}:</strong> {{ currentList === 'Followers' ? followerNumber : followeeNumber }}
        </div>
      </div>
    </div>
    <div class="col-md-7 follower-list">
      <h2>Your {{ currentList === 'Followers' ? 'Follower' : 'Followees' }}</h2>

      <button @click="toggleList">Switch to {{ currentList === 'Followers' ? 'Followees' : 'Followers' }}</button>
      <div v-if="currentList === 'Followers'">
        <div v-if="followerList.length === 0" class="no-follower">
          <p>Nobody's following you yet</p>
        </div>
        <div v-for="(follower, index) in followerList" :key="'follower-' + index" class="follower-item">
          <div v-if="follower.profilePicData">
            <img :src="follower.profilePicData" alt="Follower Profile Picture" class="profile-picture">
          </div>
          <div v-else>
            <img src="../assets/blank_profile_pic.webp" alt="Default Profile Picture" class="profile-picture">
          </div>
          <div @click="visitUserProfile(follower.id, follower.username, follower.email)" class="follower-name">{{ index +
            1 }}. {{ follower.username }}</div>
          <div class="follower-email">{{ follower.email }}</div>
        </div>
      </div>
      <div v-if="currentList === 'Followees'">
        <div v-if="followeeList.length === 0" class="no-follower">
          <p>You're not following anybody yet.</p>
        </div>
        <div v-for="(followee, index) in followeeList" :key="'Followee-' + index" class="follower-item">
          <div v-if="followee.profilePicData">
            <img :src="followee.profilePicData" alt="Follower Profile Picture" class="profile-picture">
          </div>
          <div v-else>
            <img src="../assets/blank_profile_pic.webp" alt="Default Profile Picture" class="profile-picture">
          </div>
          <div class="follower-name">{{ index + 1 }}. {{ followee.username }}</div>
          <div class="follower-email">{{ followee.email }}</div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import { toRaw } from 'vue';
export default {
  name: "FollowerPage",
  components: {
  },
  data() {
    return {
      username: this.$store.state.logged_user,
      email: "",
      followerList: [],
      profilePicId: null,
      followerNumber: null,
      followeeNumber: null,
      profilePicData: {},
      followeeList: [],
      currentList: 'Followers',

    };
  },
  async mounted() {
    await this.fetchData();

    if (this.profilePicId != null) {
      this.profilePicData = await this.getPhoto(this.profilePicId);
    }

    await this.loadFollowerDetails();
    await this.loadFolloweeDetails();
  },
  methods: {
    toggleList() {
      this.currentList = this.currentList === 'Followers' ? 'Followees' : 'Followers';
    },
    visitUserProfile(friendId, username, email) {
      this.$router.push({ name: 'friend', query: { friendId, username, email } });
    },
    async loadFolloweeDetails() {
      try {
        console.log(this.followeeList)
        const rawFolloweeList = toRaw(this.followeeList);
        const followeeDetailsPromises = rawFolloweeList.map(async (user_id) => {
          const response = await axios.get(`${this.$store.state.API}/users/${user_id.followee_id}`);
          const followeeData = response.data;
          if (followeeData.photo_id) {
            followeeData.profilePicData = await this.getPhoto(followeeData.photo_id);
          }
          return followeeData;
        });
        this.followeeList = await Promise.all(followeeDetailsPromises);
      } catch (error) {
        console.log("Error loading followee details:", error);
      }
    },
    async loadFollowerDetails() {
      try {
        const rawFollowerList = toRaw(this.followerList);
        const followerDetailsPromises = rawFollowerList.map(async (user_id) => {
          console.log(user_id);
          const response = await axios.get(`${this.$store.state.API}/users/${user_id.user_id}`);
          const followerData = response.data;
          followerData.profilePicData = null;

          if (followerData.photo_id) {
            followerData.profilePicData = await this.getPhoto(followerData.photo_id);
          }
          return followerData;
        });
        this.followerList = await Promise.all(followerDetailsPromises);
      } catch (error) {
        console.log("Error loading follower details:", error);
      }
    },
    async fetchData() {
      try {
        const response = await axios.get(this.$store.state.API + `/users/${this.$store.state.logged_user_id}`);
        const response2 = await axios.get(this.$store.state.API + `/getAllFollowers/${this.$store.state.logged_user_id}`);
        const response3 = await axios.get(this.$store.state.API + `/readFollowers/${this.$store.state.logged_user_id}`);
        const response4 = await axios.get(this.$store.state.API + `/getAllFollowees/${this.$store.state.logged_user_id}`);
        const response5 = await axios.get(this.$store.state.API + `/readFollowees/${this.$store.state.logged_user_id}`);

        console.log("API response:", response2.data);
        this.followerList = response2.data;
        this.followerNumber = response3.data;
        this.followeeNumber = response5.data;
        this.followeeList = response4.data;
        this.email = response.data.email;
        this.profilePicId = response.data.photo_id;
        return response.data.email;
      } catch (error) {
        console.log(error);
      }
    },
    async getPhoto(photoId) {
      try {
        const response = await axios.get(this.$store.state.API + `/getPhoto`, { params: { id: photoId }, responseType: "arraybuffer" });
        const base64 = btoa(
          new Uint8Array(response.data).reduce((data, byte) => data + String.fromCharCode(byte), "")
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
.no-follower {
  margin-top: 15px;
  font-size: x-large;
}

.map-container {
  position: fixed;
  ;
  right: 1vh;
  width: 15%;
}

.account-info {
  background-color: #2200cd;
  color: white;
  padding: 20px;
  margin: 15px;
}

.title {
  font-size: 24px;
  margin-bottom: 15px;
}

.info-item {
  margin-bottom: 10px;
}

.follower-item {
  border: 1px solid #ccc;
  padding: 15px;
  margin: 15px;
  background-color: white;
  border-radius: 5px;
  box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.1);
}

.follower-name {
  font-size: 22px;
  padding-top: 8px;

}

.follower-name:hover {
  cursor: pointer;
}

.follower-count {
  font-size: 20px;
  color: #555;
  margin-right: 90%;
  margin-top: -30px;
  margin-bottom: 10px;
}

.info-item {
  margin-bottom: 10px;
}

.post-photo img {
  max-width: 60%;
  height: auto;
  display: block;
  margin: 0 auto;
}

.profile-picture {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  margin-bottom: 10px;
}</style>
  