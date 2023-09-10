<template>
  <div class="page">
    <div class="row">
      <div class="col-md-2 account-info">
        <div class="title">
          <img
            v-if="this.profilePicData == null"
            src="../assets/blank_profile_pic.webp"
            alt="Kein Profilbild"
            class="profile-picture" />
          <img
            v-else
            :src="this.profilePicData"
            alt="Profilbild"
            class="profile-picture" />
          <div>{{ ownUsername }}</div>
        </div>
      </div>
      <div class="col-md-10">
        <div class="mx-auto" id="post-item">
          <div class="post-header">
            <p>{{ username }}:</p>
          </div>
          <div v-if="post.photo_id !== null" class="post-photo">
            <img :src="photoData[post.photo_id]" alt="Photo" />
          </div>
          <div class="post-text">{{ post.caption }}</div>
          <p class="post-date">{{ post.created_at }}</p>
          <button
            @click="likePost(post.id, this.$store.state.logged_user_id)"
            class="btn">
            <i v-if="likedPosts[post.id]" class="fa-solid fa-heart"></i>
            <i v-else class="fa-regular fa-heart"></i>
          </button>
          <a class="post-likes">{{ likedPostsCount[post.id] || 0 }}</a>
          <button @click="visitPostProfile(post.id)" class="btn">
            <i class="fa-solid fa-message"></i>
          </button>
          <span class="comment-amount">{{ commentAmount[post.id] || 0 }}</span>
        </div>
        <LikeList :postId="this.postId" :commentId="null" />
      </div>
    </div>
    <FriendsList />
  </div>
</template>
<script>
import FriendsList from "./Friendslist.vue";
import LikeList from "./LikeList.vue";
import axios from "axios";
//import { watch } from 'vue';
export default {
  name: "PostLikeList",
  components: {
    FriendsList,
    LikeList,
  },
  data() {
    return {
      API: this.$store.state.API,
      post: {},
      photoData: {},
      postId: null,
      username: null,
      ownUsername: this.$store.state.logged_user,
      postLikes: {},
      commentAmount: {},
      likedPosts: {},
      likedPostsCount: {},
      profilePicId: null,
      profilePicData: null,
    };
  },
  created() {
    this.postId = this.$route.query.postId;
  },
  async mounted() {
    let newLikedPostsCount = { ...this.likedPostsCount };
    await this.fetchPost();
    await this.fetchData();

    if (this.profilePicId != null) {
      this.profilePicData = await this.getPhoto(this.profilePicId);
    }
    this.postLikes = await this.getPostLikes(this.post.id);
    this.commentAmount[this.post.id] = await this.getCommentAmount(
      this.post.id
    );

    this.likedPosts[this.post.id] = await this.isPostLiked(
      this.post.id,
      this.$store.state.logged_user_id
    );
    if (this.post.photo_id !== null) {
      this.photoData[this.post.photo_id] = await this.getPhoto(
        this.post.photo_id
      );
    }

    const response = await this.getPostLikes(this.post.id);
    newLikedPostsCount[this.post.id] = response;
    this.likedPostsCount = newLikedPostsCount;
  },
  // watcher to always get the accurate ammount of likes on a post
  watch: {
    async likedPosts(newVal) {
      let newLikedPostsCount = { ...this.likedPostsCount };
      for (const postId in newVal) {
        const response = await this.getPostLikes(postId);
        newLikedPostsCount[postId] = response;
      }
      this.likedPostsCount = newLikedPostsCount;
    },
  },
  methods: {
    // method to get the image appended to a post
    async getPhoto(photoId) {
      try {
        const response = await axios.get(this.API + `/getPhoto`, {
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
        console.error("Error fetching photo:", error);
      }
    },
    async fetchPost() {
      try {
        const response = await axios.get(this.API + `/getPost/${this.postId}`);
        this.post = response.data;
      } catch (error) {
        console.error("Error fetching post:", error);
      }
    },
    async fetchData() {
      try {
        const response = await axios.get(
          this.API + `/users/${this.post.user_id}`
        );
        this.username = response.data.username;

        const response1 = await axios.get(
          this.API + `/users/${this.$store.state.logged_user_id}`
        );
        if (response1.data.photo_id) {
          this.profilePicId = response1.data.photo_id;
        }
      } catch (error) {
        console.error("Error fetching user:", error);
      }
    },
    async likePost(post_id, user_id) {
      const response = await axios.get(
        this.$store.state.API + `/isPostLiked/${post_id}/${user_id}`
      );
      let newLikedPosts = { ...this.likedPosts }; // Create a shallow copy
      console.log(response.data);
      if (response.data == true) {
        await axios.post(
          this.$store.state.API + `/unlikePost/${post_id}/${user_id}`
        );
        newLikedPosts[post_id] = false;
      } else if (response.data == false) {
        await axios.post(
          this.$store.state.API + `/createPostLike/${post_id}/${user_id}`
        );
        newLikedPosts[post_id] = true;
      }
      this.likedPosts = newLikedPosts; // Replace the entire object to force reactivity
      window.location.reload();
    },
    async getPostLikes(post_id) {
      const response = await axios.get(
        this.$store.state.API + `/getPostLikeAmount/${post_id}`
      );
      //console.log("POST LIKES für POST_ID: " + post_id + " Anzahl PostLikes: " + response.data)
      return response.data;
    },
    async getCommentAmount(post_id) {
      const response = await axios.get(
        this.$store.state.API + `/getCommentsOfPostAmount/${post_id}`
      );
      //console.log("POST COMMENTS für POST_ID: " + post_id + " Anzahl Comments: " + response.data)
      console.log("POST KOMMENTARE FÜR " + post_id + ", " + response.data);
      return response.data;
    },
    async isPostLiked(post_id, user_id) {
      const response = await axios.get(
        this.$store.state.API + `/isPostLiked/${post_id}/${user_id}`
      );
      return response.data;
    },
    visitPostProfile(postId) {
      this.$router.push({ name: "postComments", query: { postId } });
    },
  },
};
</script>

<style scoped>
#post-item {
  border: 1px solid blue;
  padding: 20px;
  margin-bottom: 20px;
  margin-top: 20px;
  background-color: #aaa;
  border-radius: 5px;
  max-width: 40%;
  overflow: hidden;
  text-align: center;
  font-size: 20px;
  color: white;
}
.page {
  background-color: #3c4e74;
}
.post-likes:hover {
  cursor: pointer;
}
.account-info {
  background-color: #284585;
  color: white;
  padding: 35px;
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

#post-item {
  font-size: 24px;
  margin-bottom: 10px;
}
</style>
