<template>
    <div class="feedContainer">
    <div class="col-md-7 post-list mx-auto">
      <h2 class="title">Your Feed: </h2>
      <div v-for="post in this.feed" :key="post.id" class="post-item">
        <div class="post-header">
          <p>{{ post.username }}:</p>
        </div>
        <div v-if="post.photo_id !== null" class="post-photo">
          <img :src="photoData[post.photo_id]" alt="Photo" />
        </div>
        <div class="post-text">{{ post.caption }}</div>
        <p class="post-date">{{ post.created_at }}</p>
        <button class="btn" id="green"><i class="fa fa-thumbs-up fa-lg" aria-hidden="true" @click="likePost(post.id, userId)"></i></button>
        <a class="post-likes">{{ postLikes }}</a>
        <button class="btn"><img src="../assets/comment.png"></button>
        <a class="comment-amount">{{ commentAmount }}</a>
        <!--
        <div v-for="comment in this.posts" :key="comment.id" class="comment-item">
          <div class="comment-header">
            <p>{{ comment.username }}:</p>
          </div>
        </div>
      -->
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {

  name: 'UserFeed',
  props: {
  },
  data() {
    return {
        feed: [],
        posts: [],
        friendsList: [],
        photoData: {},
        userId: this.$store.state.logged_user_id,
        postLikes: null,
    }},
    async mounted() {
    this.friendsList = this.$store.state.friendsList
            console.log(this.friendsList)
              for (let friend of this.friendsList) {
                console.log(friend)
                await this.fetchPosts(friend.userId, friend.username);
              }
            this.feed = this.feed.flat();
            for (const post of this.feed) {
              console.log(post)
              this.postLikes = this.getPostLikes(post.id)
              console.log(post.photo_id)           
                if (post.photo_id !== null) {
                    this.photoData[post.photo_id] = await this.getPhoto(post.photo_id);
                }
            
          }
    },
    methods: {
    // method to get the posts of each friend of a user 
      async fetchPosts(userId, username) {
  try {
    const response = await axios.get(this.$store.state.API + `/getPosts?user_id=${userId}`);

    // Add the username to each post in the response
    const responseDataWithUsername = response.data.map(post => {
      return {
        ...post,
        username: username
      };
    });

    this.feed.push(responseDataWithUsername);
    this.feed = this.feed.flat();

    this.feed.sort((a, b) => {
      const dateA = new Date(a.created_at);
      const dateB = new Date(b.created_at);
      return dateB - dateA;
    });

  } catch (error) {
    console.error("Error fetching posts:", error);
  }
},

     // method to get the image appended to a post
     async getPhoto(photoId) {
      try {
        const response = await axios.get(this.$store.state.API + `/getPhoto`, {params: {id: photoId}, responseType: 'arraybuffer'});
        const base64 = btoa(
        new Uint8Array(response.data).reduce(
          (data, byte) => data + String.fromCharCode(byte),
          '',
        ),
      );
      const imageSrc = `data:image/png;base64,${base64}`;
        return imageSrc
      } catch (error) {
        console.error("Error fetching photos:", error);
      }
    },

  getAdPosts(){
    // Vielleicht irgendwie alle 5 Posts oder so eine fake Werbung einbauen
  },
  async likePost(post_id, user_id) {

    var btn1 = document.querySelector('#green');
    btn1.addEventListener('click', function() {

        if (btn1.classList.contains('green')) {
        btn1.classList.remove('green');
      } 
    //this.classList.toggle('green');
  
});

    const response = await axios.get(this.$store.state.API + `/isPostLiked/${post_id}/${user_id}`);
    if(response.data == true){
      await axios.post(this.$store.state.API + `/unlikePost/${post_id}/${user_id}`);
    } else if(response.data == false) {
      await axios.post(this.$store.state.API + `/createPostLike/${post_id}/${user_id}`);
    }
    window.location.reload()
  },

  async getPostLikes(post_id) {
    const response = await axios.get(this.$store.state.API + `/getPostLikeAmount/${post_id}`);
    console.log("POST LIKES für POST_ID: " + post_id + " ANzahl PostLikes: " + response.data)
    return response.data
  }
},

}

</script>

<style>
.post-text {
  font-family: 'Times New Roman', Times, serif;
}
  .post-item {
      border: 1px solid blue;
      padding: 20px;
      margin-bottom: 20px;
      background-color: #f5f5f5;
      border-radius: 5px;
      max-width: 90%;
      overflow: hidden;
      text-align: left;
      font-size: 20px;
    }

    .post-date {
      font-size: 14px;
      color: #555;
      margin-top: 5px;
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

button{
  cursor: pointer;
  outline: 0;
  color: #AAA;

}

.btn:focus {
  outline: none;
}

.green{
  color: green;
}
</style>