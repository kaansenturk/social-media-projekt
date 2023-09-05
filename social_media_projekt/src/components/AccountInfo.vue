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
      <div v-if="changePasswordMode">
        <form @submit.prevent="changePassword">
        <div class="info-item">
          <label for="username">Altes Passwort:  </label>
          <input type="password" v-model="oldPassword" id="password" />
        </div>
        <div class="info-item">
          <label for="email">Neues Passwort: </label>
          <input type="password" v-model="newPassword" id="password" />
        </div>
        <div class="info-item">
          <label for="email">Wiederholen: </label>
          <input type="password" v-model="passwordRepeat" id="password" />
        </div>
        <button type="submit">Save</button>
        <button @click="changePasswordMode = !changePasswordMode">Cancel</button>
      </form>
      </div>
      <span>
      <button @click="editMode = true" v-if="!editMode" title="Userinfo ändern">Edit</button> 
      <button><i class="fa fa-wrench" title="Passwort ändern" @click="changePasswordMode = !changePasswordMode"></i></button>
    </span>
    </div></div>
    <div class="col-md-7 post-list mx-auto">
      <h2 class="title">Your Posts</h2>
      <div v-for="post in this.posts" :key="post.id" class="post-item">
        <div class="post-header">
          <div>{{ post.caption }}</div>
          <p class="post-date">{{ post.created_at }}</p>
        </div>
        <div v-if="post.photo_id !== null" class="post-photo">
          <img :src="photoData[post.photo_id]" alt="Photo" />
        </div>
      </div></div>
    <FriendsList class="col-md-2" :friends="friendsList"/>
  </div>
  </template>
  <script>
  import FriendsList from "./Friendslist.vue"
  import axios from "axios";
  import Swal from 'sweetalert2/dist/sweetalert2.js'
import 'sweetalert2/dist/sweetalert2.min.css';
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
      changePasswordMode: false,
      oldPassword: "",
      newPassword: "",
      passwordRepeat: "",
      editedUsername: '',
      editedEmail: '',
      posts: [],
      photoData: {},
      };
    },
    async mounted() {
                await this.fetchPosts();
            for (const post of this.posts) {
                if (post.photo_id !== null) {
                    this.photoData[post.photo_id] = await this.getPhoto(post.photo_id);
                }
            }
    },
    methods: {
      async changePassword() {
        if (this.newPassword == this.passwordRepeat){
        const username = this.username
        const currentPassword = this.oldPassword
        const newPassword = this.newPassword
      try {
        const response = await axios.put(this.$store.state.API + `/users/${username}/update_password/`, {
          current_password: currentPassword,
          new_password: newPassword
        });
        console.log("Passwort geändert:", response.data);
        if (response.status == 200) {
          Swal.fire({
      title: 'Passwort erfolgreich geändert!',
       icon: 'info',
      iconColor: '#2200cd',
      showCloseButton: false,
      confirmButtonText: 'Schließen',
      confirmButtonColor: '#2200cd',
    }).then((result) => {
      if (result.value) {
        this.$router.push("/login")
 } 
else{
  console.log("ciao")
}})
        }
      } catch (error) {
        console.error("An error occurred while updating the password:", error);
      }} else {
        Swal.fire({
      title: 'Bitte gib zweimal das gleiche Passwort ein!',
       icon: 'info',
      iconColor: '#FF0000',
      showCloseButton: false,
      confirmButtonText: 'Schließen',
      confirmButtonColor: '#FF0000',
    })
      }
    },
      async fetchPosts() {
      try {
        const response = await axios.get(this.$store.state.API + `/getPosts?user_id=${this.$store.state.logged_user_id}`);
        this.posts = response.data;
        this.posts.sort((a, b) => {
        const dateA = new Date(a.created_at);
        const dateB = new Date(b.created_at);

      return dateB - dateA;
    });
        console.log(this.$store.state.logged_user_id)
        console.log(response.data)
      } catch (error) {
        console.error("Error fetching posts:", error);
      }
    },
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
    async getPhoto(photoId) {
      try {
        const response = await axios.get(this.$store.state.API + `/getPhoto`, {params: {id: photoId}, responseType: 'arraybuffer'});
        const base64 = btoa(
        new Uint8Array(response.data).reduce(
          (data, byte) => data + String.fromCharCode(byte),
          '',
        ),
      );
      const imageSrc = `data:image/png;base64,${base64}`;
        return imageSrc
      } catch (error) {
        console.error("Error fetching posts:", error);
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

    .post-item {
      border: 1px solid blue;
      padding: 20px;
      margin-bottom: 20px;
      background-color: #f5f5f5;
      border-radius: 5px;
      max-width: 90%;
      overflow: hidden;
      text-align: left;
      font-size: 20px;
    }

    .post-date {
      font-size: 14px;
      color: #555;
      margin-top: 5px;
}
        
    .info-item {
      margin-bottom: 10px;
    }

    .post-photo img {
      max-width: 60%;
      height: auto;
      display: block;
      margin: 0 auto;
    }
  </style>
  