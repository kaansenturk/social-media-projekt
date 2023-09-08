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
        <button @click="likePost(post.id, userId)" class="btn">
          <i v-if="likedPosts[post.id]" class="fa-solid fa-heart"></i>
          <i v-else class="fa-regular fa-heart"></i>
        </button>
        <a href="" class="post-likes">{{ likedPostsCount[post.id] || 0 }}</a>
        <button @click="visitPostProfile(post.id)" class="btn"><i class="fa-solid fa-message"></i></button>
        <span class="comment-amount">{{ commentAmount[post.id] || 0 }}</span>
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
        username: this.$store.state.logged_user,
        postLikes: {},
        commentAmount: {},
        likedPosts: {},
        likedPostsCount: {},
    }},
    // initializes the page with friends, posts, likes etc.
    async mounted() {
      let newLikedPostsCount = { ...this.likedPostsCount };
      this.friendsList = this.$store.state.friendsList
            console.log(this.friendsList)
              for (let friend of this.friendsList) {
                console.log(friend)
                await this.fetchPosts(friend.userId, friend.username);    
              }
              await this.fetchPosts(this.userId, this.username); 
            this.feed = this.feed.flat();
            for (const post of this.feed) {
              console.log(post)
              this.postLikes = await this.getPostLikes(post.id)
              this.commentAmount[post.id] = await this.getCommentAmount(post.id)        

              this.likedPosts[post.id] = await this.isPostLiked(post.id, this.userId);

              const response = await this.getPostLikes(post.id);
              newLikedPostsCount[post.id] = response;
              this.likedPostsCount = newLikedPostsCount;

              if (post.photo_id !== null) {
                this.photoData[post.photo_id] = await this.getPhoto(post.photo_id);
              }
            }
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
  const response = await axios.get(this.$store.state.API + `/isPostLiked/${post_id}/${user_id}`);
  let newLikedPosts = { ...this.likedPosts }; // Create a shallow copy
  if(response.data == true){
    await axios.post(this.$store.state.API + `/unlikePost/${post_id}/${user_id}`);
    newLikedPosts[post_id] = false;
  } else if(response.data == false) {
    await axios.post(this.$store.state.API + `/createPostLike/${post_id}/${user_id}`);
    newLikedPosts[post_id] = true;
  }
  this.likedPosts = newLikedPosts; // Replace the entire object to force reactivity
},
  async getPostLikes(post_id) {
    const response = await axios.get(this.$store.state.API + `/getPostLikeAmount/${post_id}`);
    //console.log("POST LIKES für POST_ID: " + post_id + " Anzahl PostLikes: " + response.data)
    return response.data
  },
  
  async getCommentAmount(post_id) {
    const response = await axios.get(this.$store.state.API + `/getCommentsOfPostAmount/${post_id}`);
    //console.log("POST COMMENTS für POST_ID: " + post_id + " Anzahl Comments: " + response.data)
    console.log("POST KOMMENTARE FÜR " + post_id + ", " + response.data)
    return response.data
  },

  async changeLikeButton(post_id, user_id) {
    const response = await axios.get(this.$store.state.API + `/isPostLiked/${post_id}/${user_id}`);
    console.log(typeof(response.data))
    if(response.data === true) {

      console.log(response.data)
      return true;
    } else {
      console.log("No IF")
      return false;
    }
  },
  async isPostLiked(post_id, user_id) {
  const response = await axios.get(this.$store.state.API + `/isPostLiked/${post_id}/${user_id}`);
  return response.data;
},
visitPostProfile(postId){
        this.$router.push({ name: 'postComments', query: { postId } });
      },
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
      background-color: #ECF0F1;
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