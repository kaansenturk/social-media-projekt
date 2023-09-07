<template>
  <div class="row">
  <div class="col-md-3 account-info">
    <div v-if="profilePicId !== null"><img  class="profile-picture" :src="profilePicData"></div>
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
        <strong>Follower:</strong> {{ followerNumber }}
      </div>
      </div>
    </div>
      <div class="col-md-7 follower-list">
     <h2 class="title">Deine Follower:</h2>
    <div v-for="(follower, index) in followerList" :key="index" class="follower-item">
      <div class="follower-header">
        <div class="follower-name">{{ index + 1 }}. ({{ follower }})</div>
      </div>
    </div>
   </div> 
  </div>
</template>

<script>
import axios from "axios";

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
      profilePicData: {},
    };
  },
  async mounted() {
    await this.fetchData();
                
    if (this.profilePicId != null) {
      this. profilePicData = await this.getPhoto(this.profilePicId)
    }
  },
  watch: {
    async profilePicId(newProfilePicId, oldProfilePicId) {
      if (newProfilePicId !== oldProfilePicId) {
        this.profilePicData = await this.getPhoto(newProfilePicId);
      }
    },
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get(this.$store.state.API + `/users/${this.$store.state.logged_user_id}`);
        const response2 = await axios.get(this.$store.state.API + `/getAllFollowers/${this.$store.state.logged_user_id}`);
        const response3 = await axios.get(this.$store.state.API + `/readFollowers/${this.$store.state.logged_user_id}`);

        console.log("API response:", response2.data);
        this.followerList = response2.data;
        this.followerNumber = response3.data;
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
  .map-container {
    position: fixed; ; right: 1vh;
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
    }
  </style>
  