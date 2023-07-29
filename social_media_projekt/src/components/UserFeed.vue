<template>
    <div class="">
    <div v-for="posts in feed" :key="post.id" class="feed">
      {{ Hallo }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserFeed',
  props: {
    friends: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
        feed: []
    }},
    methods: {
  getFriendState(){
    // Checken ob Online oder nicht
  },
}

}

</script>

<style>
  
</style>