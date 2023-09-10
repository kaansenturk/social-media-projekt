<template>
  <div class="comment-container">
    <form>
      <textarea
        id="comment_text"
        placeholder="Tell them your opinion..."
        required
        v-model="caption" />
      <div class="file-list">
        <div
          class="file-item"
          v-for="(file, index) in droppedFiles"
          :key="index"></div>
      </div>
      <button type="button" @click.prevent="submitcomment">comment</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "commentCreator",
  props: {
    postId: Number,
  },
  data() {
    return {
      API: this.$store.state.API,
      isDragging: false,
      caption: "",
      post_id: null,
    };
  },

  methods: {
    async submitcomment() {
      try {
        console.log(this.caption);
        const response = await axios.post(
          this.API +
            `/createComment/${this.$store.state.logged_user_id}/${this.postId}/${this.caption}`
        );
        console.log(response.data);
      } catch (error) {
        console.error("An error occurred while submitting the comment:", error);
      }
      window.location.reload();
    },
  },
  getUser(name) {
    this.username = name;
  },
};
</script>

<style>
#comment_text {
  width: 100%;
}
.comment-container {
  height: 15%;
  padding: 30px;
  background-color: #aaa;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
</style>
