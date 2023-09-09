<template>
  <div class="friends-container">
    <div v-for="friend in friendsList" :key="friend.userId" class="friend-item">
      {{ friend.username }}
      <button v-if="fromMessenger" @click="$emit('userSelected', friend.userId, friend.username)"><i class="fa-solid fa-message"></i></button>
      <button @click="visitUserProfile(friend.userId, friend.username, friend.email)"><i class="fa-solid fa-user"></i></button>
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
      friendsList: [],
      API: this.$store.state.API,
    }},
    mounted() {
    this.getFriends();
  },
    methods: {
      visitUserProfile(friendId, username,  email){
        this.$router.push({ name: 'friend', query: { friendId, username, email } }).then(() => {
          window.location.reload();
        });
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
            const response = await axios.get(this.API + `/get_user_location/${userId}`)
              console.log(response.data)
              return response.data
          } catch {
            console.log("hallo")
          }
        },
  async getFriends(){
      try {
        const user_id = this.$store.state.logged_user_id
        const response =  await axios.get(this.API + `/getAllFollowees/${user_id}`);
    
    if (response.status == 200) {
      this.$store.commit('setFriendsList', []);
    }
    let List = [];
    for (const followee of response.data) {
      let userLocation = null;
      try {
        const userId = followee.followee_id;
        const user =  await this.getUserById(userId);
        
        if (user) {
          userLocation = await this.getFriendsLocation(userId);
          List.push({
            userId: userId,
            username: user.username,
            location: userLocation,
            email: user.email
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
      console.log(this.$store.state.friendsList)
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
  button {
    color: white;
    background-color: blue;
    border-radius: 10px;
  }
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
  background-color: #ECF0F1;
}
  
</style>