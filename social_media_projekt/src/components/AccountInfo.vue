<template>
  <div class="row">
    <div class="col-md-2 account-info">
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
      <div class="info-item">
        <strong>Role:</strong> {{ role }}
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
        username: 'Fr@dt',
        email: 'fredmetzler@battlenet.com',
        role: 'CEO',
        // Hier Freunde aus DB beziehen ... 
        friendsList: [
        { id: 1, name: "Daniel" },
        { id: 2, name: "Johann" },
        { id: 3, name: "Kaan" },
      ],
      editMode: false,
      editedUsername: '',
      editedEmail: '',
      };
    },
    mounted() {
    document.addEventListener('drop', this.preventGlobalDrop, false);
  },
  beforeUnmount() {
    document.removeEventListener('drop', this.preventGlobalDrop, false);
  },
  computed: {
    preventGlobalDrop() {
      return function(event) {
        event.preventDefault();
        event.stopPropagation();
      };
    },
    },
    methods: {
      async saveChanges() {
      try {
        const response = await axios.put('/update_user', {
          username: this.editedUsername,
          email: this.editedEmail,
        });

        console.log('User updated:', response.data);

        // Update current user info
        this.username = this.editedUsername;
        this.email = this.editedEmail;

        this.editMode = false;
      } catch (error) {
        console.error('Error updating user:', error);
      }
    },
      fetchData(){
        // Datenzugriff regeln
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
  </style>
  