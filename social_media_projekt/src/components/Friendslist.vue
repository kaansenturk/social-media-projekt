<template>
    <div class="friends-container">
    <div v-for="friend in friends" :key="friend.id" class="friend-item">
      {{ friend.name }}
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'FriendsList',
  props: {
    friends: {
      type: Array,
      required: false,
    },
    userId: Number,
  },
  data() {
    return {
        friends12: [
        { id: 1, name: "Daniel" },
        { id: 2, name: "Johann" },
        { id: 3, name: "Kaan" },
      ],
      friendsList: [],
    }},
    methods: {
  getFriendState(){
    // Checken ob Online oder nicht
  },
  getFriends(){
    try {
      const response = axios.get(this.$store.state.API + "/getAllFollowers", null, {
      params: {
        followee: this.$store.state.logged_user
      }}
      ) 
      this.friendsList = response.data
    }catch (error){
      console.log(error)
    }
  }
}

}

</script>

<style>
  
  .friends-container {
  display: flex;
  flex-direction: column;
}

.friend-item {
  margin: 0px 5px 0px 5px;
}

.friends-container {
    width: 12%;
  position: fixed;
  right: 20px; 
  top: 40%; 
  height: 40%;
  transform: translateY(-50%);
  border: solid 2px blue;
  border-radius: 2px;
}
  
</style>