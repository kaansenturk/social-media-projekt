<template>
  <div class="friends-container">
    <div v-for="friend in friendsList" :key="friend.userId" class="friend-item">
      {{ friend.username }}
      <button v-if="fromMessenger" @click="$emit('userSelected', friend.userId)">Chat</button>
      <button @click="visitUserProfile(friend.userId)">Visit Profile</button>
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
    fromMessenger: Boolean,
  },
  data() {
    return {
        friends12: [
        { id: 1, name: "Daniel" },
        { id: 2, name: "Johann" },
        { id: 3, name: "Kaan" },
      ],
      friendsList: [],
      API: "http://localhost:8000",
    }},
    mounted() {
    this.getFriends();
  },
    methods: {
  getFriendState(){
    // Checken ob Online oder nicht
  },
  async getUserById (userId)  {
  try {
    const response = await axios.get(this.API + `/users/${userId}`);
    return response.data;
  } catch (error) {
    console.error(`An error occurred while fetching user with ID ${userId}: `, error);
    return null;
  }
},
async  getFriendsLocation(userId) {
          try {
            const response = await axios.get(this.API + `/get_user_locations/${userId}`)
              console.log(response.data)
              return response.data
          } catch {
            console.log("hallo")
          }
        },
  async getFriends(){
    const query = this.$store.state.logged_user_id
      try {
    const response =  await axios.get(this.API + '/getAllFollowers', {
      params: {
        followee: query
      }
    });
    let List = [];
    for (const follower of response.data) {
      let userLocation = null;
      try {
        const userId = follower.user_id;
        const user =  await this.getUserById(userId);
        
         userLocation = await this.getFriendsLocation(userId);
        if (user) {
          List.push({
            userId: userId,
            username: user.username, // Assuming 'username' is a field in the User schema
            location: userLocation
          });
        }
      }  
         catch {
          console.log("Error")
        }
      }
      console.log(List)
      this.friendsList = List;
      this.$store.commit('setFriendsList', List);
      return List;
    }catch (error){

      console.log(error)
      return null
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