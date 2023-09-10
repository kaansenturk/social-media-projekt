<template>
  <div class="row">
    <div class="col-md-3 account-info">
      <div v-if="profilePicId !== null">
        <img class="profile-picture" :src="profilePicData" />
      </div>
      <div v-else>
        <img src="../assets/blank_profile_pic.webp" class="profile-picture" />
      </div>
      <h2 class="title">Account Information</h2>
      <div class="info">
        <div class="info-item"><strong>Username:</strong> {{ username }}</div>
        <div class="info-item"><strong>Email:</strong> {{ email }}</div>
        <div class="info-item">
          <strong>{{ currentList }}:</strong>
          {{ currentList === "Followers" ? followerNumber : followeeNumber }}
        </div>
      </div>
    </div>
    <div class="col-md-9 follower-list">
      <div class="list-header">
        <h2 :style="{ fontFamily: 'Trebuchet MS, sans-serif', color: 'white' }">
          Your {{ currentList === "Followers" ? "Follower" : "Followees" }}
        </h2>
        <button class="toggle-button" @click="toggleList">
          Switch to
          {{ currentList === "Followers" ? "Followees" : "Followers" }}
        </button>
      </div>
      <div v-if="currentList === 'Followers'">
        <div v-if="followerList.length === 0" class="no-follower">
          <p>Nobody's following you yet</p>
        </div>
        <div
          v-for="follower in followerList"
          :key="follower.id"
          class="follower-item">
          <div class="profile-picture-container">
            <img
              v-if="follower.profilePicData"
              :src="follower.profilePicData"
              class="profile-picture" />
            <img
              v-else
              src="../assets/blank_profile_pic.webp"
              alt="Default Profile Picture"
              class="profile-picture" />
          </div>
          <div
            @click="
              visitUserProfile(follower.id, follower.username, follower.email)
            "
            class="follower-name"
            :style="{ fontFamily: 'Trebuchet MS, sans-serif' }">
            {{ follower.username }}
          </div>
          <div
            class="follower-email"
            :style="{ fontFamily: 'Trebuchet MS, sans-serif' }">
            {{ follower.email }}
          </div>
          <button
            class="btn btn-sm btn-secondary float-right"
            @click="followUser(follower.id, follower.username)"
            :disabled="followerNotFollowed(follower.id)">
            Follow
          </button>
        </div>
      </div>
      <div v-if="currentList === 'Followees'">
        <div v-if="followeeList.length === 0" class="no-follower">
          <p>You're not following anybody yet.</p>
        </div>
        <div
          v-for="followee in followeeList"
          :key="followee.id"
          class="follower-item">
          <div class="profile-picture-container">
            <img
              v-if="followee.profilePicData"
              :src="followee.profilePicData"
              alt="Followee Profile Picture"
              class="profile-picture" />
            <img
              v-else
              src="../assets/blank_profile_pic.webp"
              alt="Default Profile Picture"
              class="profile-picture" />
          </div>
          <div
            @click="
              visitUserProfile(followee.id, followee.username, followee.email)
            "
            class="follower-name"
            :style="{ fontFamily: 'Trebuchet MS, sans-serif' }">
            {{ followee.username }}
          </div>
          <div
            class="follower-email"
            :style="{ fontFamily: 'Trebuchet MS, sans-serif' }">
            {{ followee.email }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { toRaw } from "vue";
import Swal from "sweetalert2/dist/sweetalert2.js";
import "sweetalert2/dist/sweetalert2.min.css";
export default {
  name: "FollowerPage",
  components: {},
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
      currentList: "Followers",
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
    async followUser(followee_id, username) {
      try {
        const response = await axios.post(
          this.$store.state.API + "/createFollower",
          {
            followee: followee_id,
            owner_id: this.$store.state.logged_user_id,
          }
        );
        console.log(response.data);
        if (response.data) {
          Swal.fire({
            title: "Folgen erfolgreich",
            text: `Du folgst jetzt ${username}`,
            icon: "info",
            iconColor: "#2200cd",
            showCloseButton: false,
            confirmButtonText: "Schließen",
            confirmButtonColor: "#2200cd",
          }).then((result) => {
            if (result.value) {
              window.location.reload();
            }
          });
        }
      } catch (error) {
        console.error("Error following user:", error);
        if (error.code == "ERR_BAD_REQUEST") {
          Swal.fire({
            title: "Error",
            text: "You already follow this user",
            icon: "info",
            iconColor: "#d0342c",
            showCloseButton: false,
            confirmButtonText: "Schließen",
            confirmButtonColor: "#d0342c",
          });
        }
      }
    },
    followerNotFollowed(followerId) {
      return this.followeeList.some((followee) => followee.id === followerId);
    },
    toggleList() {
      this.currentList =
        this.currentList === "Followers" ? "Followees" : "Followers";
    },
    visitUserProfile(friendId, username, email) {
      this.$router.push({
        name: "friend",
        query: { friendId, username, email },
      });
    },
    async loadFolloweeDetails() {
      try {
        console.log(this.followeeList);
        const rawFolloweeList = toRaw(this.followeeList);
        const followeeDetailsPromises = rawFolloweeList.map(async (user_id) => {
          const response = await axios.get(
            `${this.$store.state.API}/users/${user_id.followee_id}`
          );
          const followeeData = response.data;
          if (followeeData.photo_id) {
            followeeData.profilePicData = await this.getPhoto(
              followeeData.photo_id
            );
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
          const response = await axios.get(
            `${this.$store.state.API}/users/${user_id.user_id}`
          );
          const followerData = response.data;
          followerData.profilePicData = null;

          if (followerData.photo_id) {
            followerData.profilePicData = await this.getPhoto(
              followerData.photo_id
            );
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
        const response = await axios.get(
          this.$store.state.API + `/users/${this.$store.state.logged_user_id}`
        );
        const response2 = await axios.get(
          this.$store.state.API +
            `/getAllFollowers/${this.$store.state.logged_user_id}`
        );
        const response3 = await axios.get(
          this.$store.state.API +
            `/readFollowers/${this.$store.state.logged_user_id}`
        );
        const response4 = await axios.get(
          this.$store.state.API +
            `/getAllFollowees/${this.$store.state.logged_user_id}`
        );
        const response5 = await axios.get(
          this.$store.state.API +
            `/readFollowees/${this.$store.state.logged_user_id}`
        );

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

.account-info {
  color: white;
  padding: 20px;
  height: 100vh;
  background-color: #142957;
  height: 300px;
  font-size: 20px;
}

.title {
  font-size: 30px;
  margin-bottom: 15px;
}

.info {
  margin-bottom: 20px;
}

.info-item {
  margin-bottom: 10px;
}

.follower-list {
  background-color: #3c4e74;
  padding: 20px;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.toggle-button {
  background-color: #3c4e74;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.toggle-button:hover {
  background-color: #142957;
}

.no-follower {
  margin-top: 15px;
  font-size: 18px;
  text-align: center;
}

.follower-item {
  border: 1px solid #17008a;
  padding: 15px;
  margin: 15px 0;
  background-color: #284585;
  color: white;
  border-radius: 5px;
  box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
}

.profile-picture-container {
  margin-right: 20px;
}

.profile-picture {
  width: 70px;
  height: 70px;
  border-radius: 50%;
}

.follower-name {
  font-size: 20px;
  cursor: pointer;
}

.follower-name:hover {
  text-decoration: underline;
}

.follower-email {
  padding: 30px;
  font-size: 20px;
  color: grey;
}
</style>
