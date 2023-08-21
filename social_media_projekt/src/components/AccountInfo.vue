<template>
       <PostCreator />

    <div class="account-info">
      <h2 class="title">Account Information</h2>
      <div class="info-item">
        <strong>Username:</strong> {{ username }}
      </div>
      <div class="info-item">
        <strong>Email:</strong> {{ email }}
      </div>
      <div class="info-item">
        <strong>Role:</strong> {{ role }}
      </div>
    </div>
    <FriendsList :friends="friendsList"/>
  </template>
  
  <script>
  import FriendsList from "./Friendslist.vue"
import PostCreator from "./postCreator.vue";
  export default {
    name: 'AccountInfo',
    components: {
    FriendsList,
    PostCreator,
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
      };
    },
    methods: {
      fetchData(){
        // Datenzugriff regeln
      },
    },
  };
  </script>
  
  <style scoped>
  .account-info {
    background-color: #2200cd;
    color: white;
    width: 60%;
    padding: 20px;
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
  