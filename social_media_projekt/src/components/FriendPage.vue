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
        <div><i class="fa fa-user-minus" @click="unfollowUser" style=" cursor: pointer" title="Follow Beenden"></i></div>
        </div>
    </div>
    <div class="col-md-7 post-list">
      <h2 class="title">Friend's Posts</h2>
      <div v-for="post in this.posts" :key="post.id" class="post-item">
        <div class="post-header">
          <div>{{ post.caption }}</div>
          <p class="post-date">{{ post.created_at }}</p>
        </div>
        <div v-if="post.photo_id !== null" class="post-photo">
          <img :src="photoData[post.photo_id]" alt="Photo" />
        </div>
      </div></div>
      <FriendsList class="col-md-2" :friends="friendsList"/>
    </div>
    </template>
    <script>
    import FriendsList from "./Friendslist.vue"
    import axios from "axios";
    import Swal from 'sweetalert2/dist/sweetalert2.js'
    import 'sweetalert2/dist/sweetalert2.min.css';
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
      watch: {
    '$route': 'fetchData'
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
        // duplicate method to allow switching the user from within this page and circumvent the mounted lifecycle
        async fetchData() {
      const userId = this.$route.query.friendId;
      this.userId = userId;
      if (userId) {
        await this.fetchPosts(userId);
      }
      for (const post of this.posts) {
        if (post.photo_id !== null) {
          this.photoData[post.photo_id] = await this.getPhoto(post.photo_id);
        }
      }
      this.username = this.$route.query.username;
      this.email = this.$route.query.email;
    },
    // method to call the app route to unfollow the selected user
        async unfollowUser(){
            try {
                const response = await axios.post(this.$store.state.API + "/unfollowUser", null, {
                    params: {
                        followee_id: this.$store.state.logged_user_id,
                        user_id: this.userId
                    }
                })
                if (response.status == 200) {
                    Swal.fire({
      title: 'Erfolgreich Follow beendet',
       icon: 'info',
      iconColor: '#2200cd',
      showCloseButton: false,
      confirmButtonText: 'Zurück',
      confirmButtonColor: '#2200cd',
    }).then((result) => {
      if (result.value) {
        this.$router.push("/")
        } 
    else{
  console.log("ciao")
    }})
        }
            } catch(error) {
                console.log(error)
            }
        },
        // method to get all posts of the user we visit on this page
        async fetchPosts(userId) {
      try {
        const response = await axios.get(this.$store.state.API + `/getPosts?user_id=${userId}`);
        this.posts = response.data;
        this.posts.sort((a, b) => {
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
      max-height: 270px;
      overflow-y: auto; 
    }
    
    .title {
      font-size: 35px;
      margin-bottom: 10px;
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
    </style>
    