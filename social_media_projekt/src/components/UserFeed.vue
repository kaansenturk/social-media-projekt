<template>
    <div class="feedContainer">
    <div v-for="posts in feed" :key="post.id" class="feed">
      {{ Hallo }}
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {

  name: 'UserFeed',
  props: {
    friendsPosts: {
      type: Array,
      required: true,
    },
    userId: Number,
    required: true,
  },
  data() {
    return {
        feed: [],
        loggedInUserId: null,
    }},
    methods: {
      async  fetchAllFollowerPosts() {
    try {
        // Assuming `loggedInUserId` is the ID of the currently logged-in user
        const followersResponse = await axios.get(`/getAllFollowers?followee=${loggedInUserId}`);

        const followerIds = followersResponse.data; // Assuming the API returns an array of follower IDs

        // Fetch posts of all followers
        const allPostsPromises = followerIds.map(followerId => {
            return axios.get(`/getPosts?user_id=${followerId}`);
        });

        // Wait for all requests to complete
        const allPostsResponses = await Promise.all(allPostsPromises);

        // Extract posts from responses
        const allPosts = allPostsResponses.flatMap(response => response.data);

        return allPosts;

    } catch (error) {
        console.error("Error fetching follower posts:", error);
        return [];
    }
},

  getAdPosts(){
    // Vielleicht irgendwie alle 5 Posts oder so eine fake Werbung einbauen
  },
},
mounted: {
  setLoggedUser(){
  this.loggedInUserId = this.$store.state.logged_user_id
  }
},

}

</script>

<style>
  
</style>