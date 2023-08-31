<template>
  <div class="row">
    <div class="col-md-6 account-info">
      <h2 class="title">Account Information</h2>
      <form @submit.prevent="saveChanges" v-if="editMode">
        <div class="info-item">
          <label for="username">Username:</label>
          <input v-model="editedUsername" id="username" />
        </div>
        <div class="info-item">
          <label for="email">Email:</label>
          <input v-model="editedEmail" id="email" />
        </div>
        <button type="submit">Save</button>
        <button @click="editMode = false">Cancel</button>
      </form>
      <div v-else>
      <div class="info-item">
        <strong>Username:</strong> {{ username }}
      </div>
      <div class="info-item">
        <strong>Email:</strong> {{ email }}
      </div>
      <button @click="editMode = true" v-if="!editMode">Edit</button>
    </div></div>
    <FriendsList class="col-md-2" :friends="friendsList"/>
  </div>
  </template>
  <script>
  import FriendsList from "./Friendslist.vue"
  import axios from "axios";
  export default {
    name: 'AccountInfo',
    components: {
    FriendsList,
},
    data() {
      return {
        username: this.$store.state.logged_user,
        email: '',
      editMode: false,
      editedUsername: '',
      editedEmail: '',
      };
    },
    async mounted() {
    await this.fetchData(); 
  },
    methods: {
      async saveChanges() {
      try {
        const response = await axios.put(this.$store.state.API + `/update_user/${this.username}`, {
          username: this.editedUsername,
          email: this.editedEmail,
        });
        console.log('User updated:', response.data);
        this.username = this.editedUsername;
        this.email = this.editedEmail;

        this.editMode = false;
        this.$store.dispatch('login', { user: this.username, user_id: this.$store.state.logged_user_id});
        localStorage.setItem('logged_user', this.username)
      } catch (error) {
        console.error('Error updating user:', error);
      }
    },
      async fetchData(){
        try {
        const response = await axios.get(this.$store.state.API + `/users/${this.$store.state.logged_user_id}`);
        
        console.log(this.$store.state.API,this.$store.state.logged_user_id, response.data.email)
        this.email = response.data.email
        return response.data.email
      } catch(error) {
        console.log(error)
      }
    },
  }
  };
  </script>
  
  <style scoped>
  .map-container {
    position: fixed; ; right: 1vh;
    width: 15%;
  }
  .account-info {
    background-color: #2200cd;
    padding: 2%;
    color: white;
    margin: auto;
  }
  
  .title {
    font-size: 24px;
    margin-bottom: 10px;
  }
  
  .info-item {
    margin-bottom: 5px;
  }
  </style>
  