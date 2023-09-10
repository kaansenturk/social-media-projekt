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
    <div class="col-md-8 mx-auto" id="comment-item">
      <div class="comment-header">
        <p>{{ username }}:</p>
      </div>
      <div class="comment-text">{{ comment.comment_text }}</div>
      <p class="comment-date">{{ comment.created_at }}</p>
      <button
        @click="likeComment(comment.id, this.$store.state.logged_user_id)"
        class="btn">
        <i v-if="likedComments[comment.id]" class="fa-solid fa-heart"></i>
        <i v-else class="fa-regular fa-heart"></i>
      </button>
      <span class="comment-likes">{{
        likedCommentsCount[comment.id] || 0
      }}</span>
    </div>
    <LikeList :commentId="this.commentId" :postId="null" />
    <FriendsList class="col-md-2" :friends="friendsList" />
  </div>
</div>
</template>
<script>
import FriendsList from "./Friendslist.vue";
import LikeList from "./LikeList.vue";
import axios from "axios";
//import { watch } from 'vue';
export default {
  name: "CommentLikeList",
  components: {
    FriendsList,
    LikeList,
  },
  data() {
    return {
      API: this.$store.state.API,
      comment: {},
      photoData: {},
      commentId: null,
      username: null,
      ownUsername: this.$store.state.logged_user,
      commentLikes: {},
      likedComments: {},
      likedCommentsCount: {},
      profilePicData: null,
      profilePicId: null,
    };
  },
  created() {
    this.commentId = this.$route.query.commentId;
  },
  async mounted() {
    let newLikedCommentsCount = { ...this.likedCommentsCount };
    await this.fetchComment();
    await this.fetchData();

    if (this.profilePicId != null) {
      this.profilePicData = await this.getPhoto(this.profilePicId);
    }

    this.commentLikes = await this.getCommentLikes(this.comment.id);

    this.likedComments[this.comment.id] = await this.isCommentLiked(
      this.comment.id,
      this.$store.state.logged_user_id
    );

    const response = await this.getCommentLikes(this.comment.id);
    newLikedCommentsCount[this.comment.id] = response;
    this.likedCommentsCount = newLikedCommentsCount;
  },
  // watcher to always get the accurate ammount of likes on a comment
  watch: {
    async likedComments(newVal) {
      let newLikedCommentsCount = { ...this.likedCommentsCount };
      for (const commentId in newVal) {
        const response = await this.getCommentLikes(commentId);
        newLikedCommentsCount[commentId] = response;
      }
      this.likedCommentsCount = newLikedCommentsCount;
    },
  },
  methods: {
    // method to get the image appended to a comment
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
    async fetchComment() {
      try {
        const response = await axios.get(
          this.API + `/getComment/${this.commentId}`
        );
        this.comment = response.data;
      } catch (error) {
        console.error("Error fetching comment:", error);
      }
    },
    async fetchData() {
      try {
        const response = await axios.get(
          this.API + `/users/${this.comment.user_id}`
        );
        this.username = response.data.username;

        const response1 = await axios.get(
          this.API + `/users/${this.$store.state.logged_user_id}`
        );
        console.log(response1.data)
        if (response1.data.photo_id != null) {
          this.profilePicId = response1.data.photo_id;
        }
      } catch (error) {
        console.error("Error fetching user:", error);
      }
    },
    async likeComment(comment_id, user_id) {
      const response = await axios.get(
        this.$store.state.API + `/isCommentLiked/${comment_id}/${user_id}`
      );
      let newLikedComments = { ...this.likedComments }; // Create a shallow copy
      if (response.data == true) {
        await axios.post(
          this.$store.state.API + `/unlikeComment/${comment_id}/${user_id}`
        );
        newLikedComments[comment_id] = false;
      } else if (response.data == false) {
        await axios.post(
          this.$store.state.API + `/createCommentLike/${comment_id}/${user_id}`
        );
        newLikedComments[comment_id] = true;
      }
      this.likedComments = newLikedComments; // Replace the entire object to force reactivity
      window.location.reload();
    },
    async getCommentLikes(comment_id) {
      const response = await axios.get(
        this.$store.state.API + `/getCommentLikeAmount/${comment_id}`
      );
      //console.log("POST LIKES für POST_ID: " + comment_id + " Anzahl CommentLikes: " + response.data)
      return response.data;
    },
    async isCommentLiked(comment_id, user_id) {
      const response = await axios.get(
        this.$store.state.API + `/isCommentLiked/${comment_id}/${user_id}`
      );
      return response.data;
    },
  },
};
</script>

<style scoped>
.page {
    background-color: #284585;
}
#comment-item{
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

#comment-item {
  font-size: 24px;
  margin-bottom: 10px;
}
</style>
