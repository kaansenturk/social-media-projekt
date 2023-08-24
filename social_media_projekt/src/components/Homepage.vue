<template>
    <div class="row">
         
  
      <div class="col-md-2 account-info">
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
      <PostCreator class="col-md-7"/>
      <FriendsList class="col-md-2" :friends="friendsList"/>
    </div>
      <FriendsMap class="map-container"></FriendsMap>
    </template>
    
    <script>
    import FriendsList from "./Friendslist.vue"
  import PostCreator from "./postCreator.vue"
  import FriendsMap from "./map.vue"
    export default {
      name: 'HomePage',
      components: {
      FriendsList,
      PostCreator,
      FriendsMap,
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
    