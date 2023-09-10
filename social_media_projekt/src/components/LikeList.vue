<template>
  <div class="col-md-0 likes-list">
    <div v-if="likeList.length == 0" class="no-likes">
      <p v-if="postId != null" style="color: white;">Nobody likes this post:</p>
      <p v-else-if="commentId != null" style="color: white;">Nobody likes this comment:</p>
    </div>
    <div v-else class="user-item-container">
      <p v-if="postId != null" style="color: white;">Users who liked this post:</p>
      <p v-else-if="commentId != null" style="color: white;">Users who liked this comment:</p>
      <div v-for="user in userList" :key="user.user_id" class="user-item">
        <div v-if="user.photo_id">
          <img
            :src="user.profilePicData"
            alt="User Profile Picture"
            class="profile-picture" />
        </div>
        <div v-else>
          <img
            src="../assets/blank_profile_pic.webp"
            alt="Default Profile Picture"
            class="profile-picture" />
        </div>
        <a
          @click="visitUserProfile(user.id, user.username, user.email)"
          class="user-name"
          >{{ user.username }}
        </a>
        <div class="user-email">{{ user.email }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "LikeList",
  props: {
    postId: Number,
    commentId: Number,
  },
  data() {
    return {
      likeList: [],
      userList: [],
      profilePicId: null,
      profilePicData: {},
    };
  },
  async mounted() {
    if (this.postId != null) {
      await this.fetchPostLikes(this.postId);
      this.likeList = this.likeList.flat();
    } else {
      await this.fetchCommentLikes(this.commentId);
      this.likeList = this.likeList.flat();
    }

    await this.fetchUsers(this.likeList);

    if (this.profilePicId != null) {
      this.profilePicData = await this.getPhoto(this.profilePicId);
    }
  },
  methods: {
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
    // method to get the likes of a post
    async fetchPostLikes(postId) {
      try {
        const response = await axios.get(
          this.$store.state.API + `/getPostLikes/${postId}`
        );
        // Add the username to each user in the response
        this.likeList.push(response.data);
        this.likeList = this.likeList.flat();

        this.likeList.sort((a, b) => {
          const dateA = new Date(a.created_at);
          const dateB = new Date(b.created_at);
          return dateB - dateA;
        });
      } catch (error) {
        console.error("Error fetching post:", error);
      }
    },
    // method to get the likes of a comment
    async fetchCommentLikes(commentId) {
      try {
        const response = await axios.get(
          this.$store.state.API + `/getCommentLikes/${commentId}`
        );
        // Add the username to each user in the response
        this.likeList.push(response.data);
        this.likeList = this.likeList.flat();

        this.likeList.sort((a, b) => {
          const dateA = new Date(a.created_at);
          const dateB = new Date(b.created_at);
          return dateB - dateA;
        });
      } catch (error) {
        console.error("Error fetching comment:", error);
      }
    },
    // method to get the Users
    async fetchUsers(likeList) {
      try {
        for (var entry in likeList) {
          const response = await axios.get(
            this.$store.state.API + `/users/${likeList[entry].user_id}`
          );
          var user = response.data;
          user.profilePicData = null;
          if (user.photo_id !== null){
          user.profilePicData = await this.getPhoto(user.photo_id);
          }
          this.userList.push(user);
          this.userList = this.userList.flat();
        }
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    },
    visitUserProfile(friendId, username, email) {
      this.$router.push({
        name: "friend",
        query: { friendId, username, email },
      });
    },
  },
};
</script>

<style>
.user-text {
  font-family: "Times New Roman", Times, serif;
}

.user-item {
  display: flex;
  border: 1px solid blue;
  padding: 20px;
  margin-bottom: 20px;
  background-color: #daf7a6;
  border-radius: 5px;
  max-width: 90%;
  overflow: hidden;
  text-align: left;
  font-size: 20px;
  max-height: 200px;
  width: 200px;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.user-name {
  color: #555;
}

.user-date {
  font-size: 14px;
  color: #555;
  margin-top: 5px;
}

.info-item {
  margin-bottom: 10px;
}

.user-photo img {
  max-width: 60%;
  height: auto;
  display: block;
  margin: 0 auto;
}

button {
  cursor: pointer;
  outline: 0;
  color: #aaa;
}

.btn:focus {
  outline: none;
}

.green {
  color: green;
}

.profile-picture {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  margin-bottom: 10px;
}

.user-item-container {
  display: grid;
  place-items: center;
}
</style>
