<template>
  <div class="feedContainer">
    <div class="col-md-7 post-list mx-auto">
      <h2 class="titleFeed" style="margin-left: 20px;">Your Feed: </h2>
      <div v-for="post in this.feed" :key="post.id" class="post-item">
        <div class="post-header">
          <p>{{ post.username }}:</p>
        </div>
        <div v-if="post.isAd" class="post-photo">
          <a href="http://www.hs-flensburg.de" target="_blank">
           <img src="../assets/HS_logo.png" alt="Advertisement" />
            </a>
        </div>
        <div v-else-if="post.photo_id !== null" class="post-photo">
          <img :src="photoData[post.photo_id]" alt="Photo" />
        </div>
        <div class="post-text">{{ post.caption }}</div>
        <p class="post-date">{{ post.created_at }}</p>
        <button @click="likePost(post.id, userId)" class="btn">
          <i v-if="likedPosts[post.id]" class="fa-solid fa-heart"></i>
          <i v-else class="fa-regular fa-heart"></i>
        </button>
        <a @click="visitLikeProfile(post.id)" class="post-likes">{{ likedPostsCount[post.id] || 0 }}</a>
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
      friendsList: this.$store.state.friendsList,
      photoData: {},
      userId: this.$store.state.logged_user_id,
      username: this.$store.state.logged_user,
      postLikes: {},
      commentAmount: {},
      likedPosts: {},
      likedPostsCount: {},
    }
  },
  // initializes the page with friends, posts, likes etc.
  async mounted() {
    let newLikedPostsCount = { ...this.likedPostsCount };
    console.log(this.friendsList)
    await this.fetchPostsLoop(this.friendsList)

    this.feed = this.feed.flat();
    for (const post of this.feed) {
      console.log(post)
      this.postLikes = await this.getPostLikes(post.id)
      this.commentAmount[post.id] = await this.getCommentAmount(post.id)

      this.likedPosts[post.id] = await this.isPostLiked(post.id, this.userId);

      console.log(this.likedPosts[post.id]);

      const response = await this.getPostLikes(post.id);
      newLikedPostsCount[post.id] = response;
      this.likedPostsCount = newLikedPostsCount;

      if (post.photo_id !== null) {
        this.photoData[post.photo_id] = await this.getPhoto(post.photo_id);
      }
    }
    this.getAdPosts()
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
    async fetchPostsLoop(friendsList) {
      for (let friend of friendsList) {
        await this.fetchPosts(friend.userId, friend.username);
      }
      //await this.fetchPosts(this.userId, this.username);
    },
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
        const response = await axios.get(this.$store.state.API + `/getPhoto`, { params: { id: photoId }, responseType: 'arraybuffer' });
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

    getAdPosts() {
  const adPost = {
    id: 'ad', 
    username: 'Ad', 
    photo_id: null,
    caption: '#NoFreeAds',
    created_at: new Date().toDateString(), 
    isAd: true, 
  };

  const newFeed = [];
  for (let i = 0; i < this.feed.length; i++) {
    newFeed.push(this.feed[i]);
    if ((i + 1) % 5 === 0) {
      newFeed.push(adPost);
    }
  }
  // If there are less than 5 posts add the ad at the end
  if (this.feed.length < 5) {
    newFeed.push(adPost);
  }

  this.feed = newFeed;
},

    async likePost(post_id, user_id) {
      const response = await axios.get(this.$store.state.API + `/isPostLiked/${post_id}/${user_id}`);
      let newLikedPosts = { ...this.likedPosts }; // Create a shallow copy
      if (response.data == true) {
        await axios.post(this.$store.state.API + `/unlikePost/${post_id}/${user_id}`);
        newLikedPosts[post_id] = false;
      } else if (response.data == false) {
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
      //console.log("POST KOMMENTARE FÜR " + post_id + ", " + response.data)
      return response.data
    },

    async changeLikeButton(post_id, user_id) {
      const response = await axios.get(this.$store.state.API + `/isPostLiked/${post_id}/${user_id}`);
      console.log(typeof (response.data))
      if (response.data === true) {

        console.log(response.data)
        return true;
      } else {
        return false;
      }
    },
    async isPostLiked(post_id, user_id) {
      const response = await axios.get(this.$store.state.API + `/isPostLiked/${post_id}/${user_id}`);
      console.log(response.data)
      return response.data;
    },
    visitPostProfile(postId) {
      this.$router.push({ name: 'postComments', query: { postId } });
    },
    visitLikeProfile(postId) {
      this.$router.push({ name: 'postLikeList', query: { postId } });
    },
  },

}
</script>
<style>

.titleFeed {
  margin-right: 18%; /* Hier den Abstand nach Bedarf anpassen */
  font-size: 34px; /* Sie können auch die Schriftgröße anpassen */
}

.feedContainer {
  color: white;
  font-family: 'Trebuchet MS', sans-serif;
}

.post-list {
  z-index: 1;
}

.post-text {
  font-family: 'Trebuchet MS', sans-serif
}

.post-item {
  border: 1px solid #17008a;
  padding: 20px;
  margin-bottom: 20px;
  background-color: #DAF7A6;
  border-radius: 5px;
  max-width: 90%;
  overflow: hidden;
  text-align: left;
  font-size: 20px;
  margin-left: -40px;
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

button {
  cursor: pointer;
  outline: 0;
  color: #AAA;

}

.btn:focus {
  outline: none;
}

</style>