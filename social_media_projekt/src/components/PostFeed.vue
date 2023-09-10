<template>
  <div class="feedContainer">
    <div class="col-md-7 comment-list mx-auto">
      <h2 class="title">Comments:</h2>
      <div v-for="comment in this.feed" :key="comment.id" class="comment-item">
        <div class="comment-header">
          <p> !!TODO!! ADD USERNAME:</p>
          <div class="comment-text">{{ comment.comment_text }}</div>
          <p class="comment-date">{{ comment.created_at }}</p>
          <button @click="likeComment(comment.id, userId)" class="btn">
            <i v-if="likedComments[comment.id]" class="fa-solid fa-heart"></i>
            <i v-else class="fa-regular fa-heart"></i>
          </button>
          <a @click="visitLikeProfile(comment.id)" class="comment-likes">{{ likedCommentsCount[comment.id] || 0 }}</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {

  name: 'PostFeed',
  props: {
    postId: Number,
  },
  data() {
    return {
      username: null,
      feed: [],
      comments: [],
      userId: this.$store.state.logged_user_id,
      commentLikes: {},
      likedComments: {},
      likedCommentsCount: {},
    }
  },
  // initializes the page with friends, comments, likes etc.
  async mounted() {
    let newLikedCommentsCount = { ...this.likedCommentsCount };
    await this.fetchComments(this.postId,);
    this.feed = this.feed.flat();
    for (const comment of this.feed) {
      console.log(comment)
      //this.commentLikes = await this.getCommentLikes(comment.id)

      this.likedComments[comment.id] = await this.isCommentLiked(comment.id, this.userId);

      const response = await this.getCommentLikes(comment.id);
      newLikedCommentsCount[comment.id] = response;
      this.likedCommentsCount = newLikedCommentsCount;

    }
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
    // method to get the comments of the post
    async fetchComments(post_id, username) {
      try {
        const response = await axios.get(this.$store.state.API + `/getCommentsOfPost/${post_id}`);
        // Add the username to each comment in the response
        const responseDataWithUsername = response.data.map(comment => {
          return {
            ...comment,
            username: username
          };
        });
        console.log(responseDataWithUsername)
        this.feed.push(responseDataWithUsername);
        this.feed = this.feed.flat();
        this.feed.sort((a, b) => {
          const dateA = new Date(a.created_at);
          const dateB = new Date(b.created_at);
          return dateB - dateA;
        });

      } catch (error) {
        console.error("Error fetching comments:", error);
      }
    },

    async likeComment(comment_id, user_id) {
      const response = await axios.get(this.$store.state.API + `/isCommentLiked/${comment_id}/${user_id}`);
      let newLikedComments = { ...this.likedComments }; // Create a shallow copy
      if (response.data == true) {
        await axios.post(this.$store.state.API + `/unlikeComment/${comment_id}/${user_id}`);
        newLikedComments[comment_id] = false;
      } else if (response.data == false) {
        await axios.post(this.$store.state.API + `/createCommentLike/${comment_id}/${user_id}`);
        newLikedComments[comment_id] = true;
      }
      this.likedComments = newLikedComments; // Replace the entire object to force reactivity
    },
    async getCommentLikes(comment_id) {
      const response = await axios.get(this.$store.state.API + `/getCommentLikeAmount/${comment_id}`);
      console.log("COMMENT LIKES für COMMENT_ID: " + comment_id + " Anzahl CommentLikes: " + response.data)
      return response.data
    },
    async changeLikeButton(comment_id, user_id) {
      const response = await axios.get(this.$store.state.API + `/isCommentLiked/${comment_id}/${user_id}`);
      console.log(typeof (response.data))
      if (response.data === true) {

        console.log(response.data)
        return true;
      } else {
        console.log("No IF")
        return false;
      }
    },
    async isCommentLiked(comment_id, user_id) {
      const response = await axios.get(this.$store.state.API + `/isCommentLiked/${comment_id}/${user_id}`);
      return response.data;
    },
    visitLikeProfile(commentId) {
      this.$router.push({ name: 'commentLikeList', query: { commentId } });
    },
    async getUserName(userId) {
      const response = await axios.get(this.$store.state.API + `users/${userId}`);
      console.log(response.data);
      return response.data.username
    }
  },

}
</script>
<style>
.comment-text {
  font-family: 'Trebuchet MS', sans-serif;
  color: #555;
  ;
}

.comment-item {
  border: 1px solid black;
  padding: 20px;
  margin-bottom: 20px;
  background-color: #ECF0F1;
  border-radius: 5px;
  max-width: 90%;
  overflow: hidden;
  text-align: left;
  font-size: 20px;
}

.comment-date {
  font-size: 14px;
  color: #555;
  margin-top: 5px;
}

.info-item {
  margin-bottom: 10px;
}

.comment-photo img {
  max-width: 60%;
  height: auto;
  display: block;
  margin: 0 auto;
}

button {
  cursor: pointer;
  outline: 0;
  color: #AAA;

}

.btn:focus {
  outline: none;
}

.green {
  color: green;
}

.comment-header {
  color: #555;
}

.comment-likes {
  color: #555;
}
</style>