<template>
    <div class="comment-container">  
        <form>
            <textarea  id="comment_text" placeholder="Tell them your opinion..." required v-model="caption" />
            <div class="file-list">
                <div class="file-item" v-for="(file, index) in droppedFiles" :key="index">
                </div>
            </div>
            <button type="button" @click.prevent="submitcomment">comment</button>
        </form>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'commentCreator',
  props: {
    postId: Number,
  },
  data() {
    return {
      API: this.$store.state.API,
      isDragging: false,
      caption: "",
      post_id: null,
    }},
   
    methods: {
      async submitcomment() {
      try {
        console.log(this.caption)
        const response = await axios.post(this.API + `/createComment/${this.$store.state.logged_user_id}/${this.postId}/${this.caption}`);
        console.log(response.data);
      } catch (error) {
        console.error("An error occurred while submitting the comment:", error);
      }} 
    },
    getUser(name){
        this.username = name
    }
  
}


</script>

<style>
.image-preview {
  max-width: 100%;
  max-height: 200px;
  object-fit: contain; 
}
.active {
  border: 2px dashed #0066ff;
}

.file-list {
  margin-top: 20px;
}

.file-item {
  margin: 5px 0;
}
.file-uploader {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100px;
}

.drop-area {
  border: 2px dashed #ccc;
  padding: 20px;
  text-align: center;
  cursor: pointer;
}
#comment_text {
  width: 100%;
  height: 100px;
}
  
  .comment-container {
    height: 20%;
    padding: 30px;
    background-color: #fff;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
  
  .login-container h1 {
    text-align: center;
  }
  
  .login-container input[type="text"],
  .login-container input[type="password"] {
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
  }
  
  .login-container button {
    width: 100%;
    padding: 10px;
    background-color: #2200cd;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .login-container button:hover {
    background-color: #2200cd;
  }
  
</style>