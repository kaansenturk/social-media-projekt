<template>
    <div class="row">
      <div class="col-md-3 account-info">
        <h2 class="title">Account Information</h2>
        
        <div>
        <div class="info-item">
          <strong>Username:</strong> {{ username }}
        </div>
        <div class="info-item">
          <strong>Email:</strong> {{ email }}
        </div>
        </div>
    </div>
    <div class="col-md-7 post-list">
      <h2 class="title">Friend's Posts</h2>
      <div v-for="post in this.posts" :key="post.id" class="post-item">
        <h3>{{ post.caption }}</h3>
        <p>{{ post.created_at }}</p>
        <div v-if="post.photo_id !== null">
          <img :src="photoData[post.photo_id]" alt="Photo" style="max-width: 30%;"/>
        </div>
      </div></div>
      <FriendsList class="col-md-2" :friends="friendsList"/>
    </div>
    </template>
    <script>
    import FriendsList from "./Friendslist.vue"
    import axios from "axios";
    export default {
      name: 'FriendPage',
      components: {
      FriendsList,
  },
      data() {
        return {
          username: '',
          email: '',
          posts: [],
          userId: null,
          photoData: {},
        };
      },
      created() {
    const friendIdFromQuery = this.$route.query.friendId;
    this.userId = friendIdFromQuery;
    
  },
        async mounted() {
            const userId = this.$route.query.friendId;
            console.log(this.$route.query.friend)
            if (userId) {
                await this.fetchPosts(userId);
                }
            for (const post of this.posts) {
                if (post.photo_id !== null) {
                    this.photoData[post.photo_id] = await this.getPhoto(post.photo_id);
                }
            }
            this.username = this.$route.query.username
            this.email = this.$route.query.email
    },
      methods: {
        async fetchPosts(userId) {
      try {
        const response = await axios.get(this.$store.state.API + `/getPosts?user_id=${userId}`);
        this.posts = response.data;
      } catch (error) {
        console.error("Error fetching posts:", error);
      }
    },
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
        console.error("Error fetching posts:", error);
      }
    },
      },
    };
    </script>
    
    <style scoped>
    .map-container {
      position: fixed; ; right: 1vh;
      width: 15%;
    }
    .account-info {
      background-color: #2200cd;
      color: white;
      padding: 35px;
      margin-left: 15px;
    }
    
    .title {
      font-size: 24px;
      margin-bottom: 10px;
    }
    
    .info-item {
      margin-bottom: 5px;
    }
    .post-item {
        border: 1px solid blue;
        max-width: 90%;
    }
    </style>
    