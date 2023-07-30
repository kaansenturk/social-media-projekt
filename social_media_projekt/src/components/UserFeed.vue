<template>
    <div class="feedContainer">
    <div v-for="posts in feed" :key="post.id" class="feed">
      {{ Hallo }}
    </div>
  </div>
</template>

<script>
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
        feed: []
    }},
    methods: {
  getFriendsPosts(){
    // Posts von Freunden mit userId kriegen
  },
  getAdPosts(){
    // Vielleicht irgendwie alle 5 Posts oder so eine fake Werbung einbauen
  },
}

}

</script>

<style>
  
</style>