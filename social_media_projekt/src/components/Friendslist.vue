<template>
  <div class="friends-title">Your Followees:</div>
  <div class="friends-container" v-if="friendsList.length > 0">
    <div class="friend-list">
      <div
        v-for="friend in friendsList"
        :key="friend.userId"
        class="friend-item">
        <div class="friend-details">
          <div class="friend-username">{{ friend.username }}</div>
        </div>
        <div class="friend-actions">
          <button
            v-if="fromMessenger"
            @click="$emit('userSelected', friend.userId, friend.username)">
            <i class="fa-solid fa-message"></i>
          </button>
          <button v-else @click="goToMessenger">
            <i class="fa-solid fa-message"></i>
          </button>
          <button
            @click="
              visitUserProfile(friend.userId, friend.username, friend.email)
            ">
            <i class="fa-solid fa-user"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";

export default {
  name: "FriendsList",
  props: {
    friends: {
      type: Array,
      required: false,
    },
    userId: Number,
    fromMessenger: Boolean,
  },
  data() {
    return {
      friendsList: [],
      API: this.$store.state.API,
    };
  },
  mounted() {
    this.getFriends();
  },
  methods: {
    goToMessenger() {
      this.$router.push("/messenger");
    },
    visitUserProfile(friendId, username, email) {
      this.$router
        .push({ name: "friend", query: { friendId, username, email } })
        .then(() => {
          window.location.reload();
        });
    },
    async getUserById(userId) {
      try {
        const response = await axios.get(this.API + `/users/${userId}`);
        return response.data;
      } catch (error) {
        console.error(
          `An error occurred while fetching user with ID ${userId}: `,
          error
        );
        return null;
      }
    },
    async getFriendsLocation(userId) {
      try {
        const response = await axios.get(
          this.API + `/get_user_location/${userId}`
        );
        return response.data;
      } catch (error) {
        console.log(error);
      }
    },
    async getFriends() {
      try {
        const user_id = this.$store.state.logged_user_id;
        const response = await axios.get(
          this.API + `/getAllFollowees/${user_id}`
        );

        if (response.status == 200) {
          this.$store.commit("setFriendsList", []);
        }
        let List = [];
        for (const followee of response.data) {
          let userLocation = null;
          try {
            const userId = followee.followee_id;
            const user = await this.getUserById(userId);

            if (user) {
              userLocation = await this.getFriendsLocation(userId);
              List.push({
                userId: userId,
                username: user.username,
                location: userLocation,
                email: user.email,
              });
            }
          } catch (error) {
            console.log(error);
          }
        }
        this.friendsList = List;
        this.$store.commit("setFriendsList", List);
        return List;
      } catch (error) {
        console.log(error);
        return null;
      }
    },
  },
};
</script>

<style scoped>
.friends-container {
  display: flex;
  flex-direction: column;
  width: 16%;
  position: fixed;
  top: 50%;
  top: 45%;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1;
  max-height: 51%;
}

.friends-title {
  display: flex;
  position: fixed;
  top: 40%;
  width: 16%;
  justify-content: center;
  align-items: center;
  height: 5%;
  background-color: #142957;
  color: #fff;
  font-weight: bold;
  z-index: 4;
}

.friend-list {
  overflow-y: auto;
}

.friend-item {
  display: flex;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #ccc;
}

.friend-details {
  flex-grow: 1;
}

.friend-username {
  font-weight: bold;
}

.friend-actions button {
  color: #fff;
  background-color: #007bff;
  border: none;
  cursor: pointer;
}

.friend-actions button:hover {
  background-color: #0056b3;
}
</style>
