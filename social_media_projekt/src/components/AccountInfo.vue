<template>
  <div class="container-fluid">
    <div v-if="profilePicId !== null"><img class="profile-picture" :src="profilePicData"><i class="fa-solid fa-pencil"
        @click="showDialog = true"></i></div>
    <div v-else><img src="../assets/blank_profile_pic.webp" alt="Profilbild" class="profile-picture" /><i
        class="fa-solid fa-pencil" @click="showDialog = true"></i></div>
    <div class="col-md-5 account-info mx-auto text-center">
      <h2 class="title">Account Information</h2>
      <dialog :open="showDialog">
        <h2>Choose a new profile picture</h2>
        <input type="file" ref="fileInput" @change="previewImage" />
        <img v-if="preview" :src="preview" alt="Profile preview" width="200" />
        <menu>
          <button @click="uploadImage">Upload</button>
          <button @click="closeDialog">Cancel</button>
        </menu>
      </dialog>
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
          <strong>Following:</strong> {{ followingNumber }}
        </div>
        <div class="info-item">
          <strong>Follower:</strong> {{ followerNumber }}
        </div>
        <div v-if="changePasswordMode">
          <form @submit.prevent="changePassword">
            <div class="info-item">
              <label for="username">Altes Passwort: </label>
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
          <button><i class="fa fa-wrench" title="Passwort ändern"
              @click="changePasswordMode = !changePasswordMode"></i></button>
              <button @click="deleteProfile" title="Profil löschen!" class="fa fa-trash "></button>
        </span>
      </div>
    </div>
    <FriendsList class="col-md-2" :friends="friendsList" />
    <UserOnlyFeed :userId=this.$store.state.logged_user_id :username="username" />
  </div>
</template>
<script>
import FriendsList from "./Friendslist.vue"
import axios from "axios";
import Swal from 'sweetalert2/dist/sweetalert2.js'
import 'sweetalert2/dist/sweetalert2.min.css';
import UserOnlyFeed from "./UserOnlyFeed.vue"
export default {
  name: 'AccountInfo',
  components: {
    FriendsList,
    UserOnlyFeed,
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
      followingNumber: null,
      followerNumber: null,
      profilePicId: null,
      profilePicData: {},
      showDialog: false,
      preview: null,
      selectedFile: null,
    };
  },
  async mounted() {
    await this.fetchData();
    await this.fetchPosts();

    for (const post of this.posts) {
      if (post.photo_id !== null) {
        this.photoData[post.photo_id] = await this.getPhoto(post.photo_id);
      }
    }
    if (this.profilePicId != null) {
      this.profilePicData = await this.getPhoto(this.profilePicId)
    }
  },
  watch: {
    async profilePicId(newProfilePicId, oldProfilePicId) {
      if (newProfilePicId !== oldProfilePicId) {
        this.profilePicData = await this.getPhoto(newProfilePicId);
      }
    },
  },
  methods: {
    async deleteProfile(){
      Swal.fire({
              title: 'Möchtest du dein Profil wirklich löschen??!',
              icon: 'warning',
              iconColor: '#2200cd',
              showCancelButton: true,
              cancelButtonText: "close",
              confirmButtonText: "Delete Profile",
              confirmButtonColor: '#2200cd',
            }).then(async (result) => {
              if (result.value) {
                try {
                const response = await axios.post(this.$store.state.API + `/deleteUser/${this.username}`)
                if (response.status == 200){
                  this.$store.dispatch('logout');
                  this.$router.push("/login")
                }
                } catch (error){
                  alert("Deleting did not work!")
                }
              }
              else {
                console.log("ciao")
              }
            })
      
    },
    
    closeDialog() {
      this.showDialog = false;
    },
    previewImage(event) {
      const file = event.target.files[0];
      this.selectedFile = file;
      const reader = new FileReader();
      reader.onload = (e) => {
        this.preview = e.target.result;
      };
      reader.readAsDataURL(file);
    },
    async uploadImage() {
      if (!this.selectedFile) return;

      const formData = new FormData();
      formData.append('image_data', this.selectedFile);

      const userId = this.$store.state.logged_user_id;
      const title = 'Profile Picture';

      try {

        const uploadResponse = await axios.post(
          `${this.$store.state.API}/upload_photo/?title=${title}&user_id=${userId}`,
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          }
        );
        const photo_id = uploadResponse.data;
        this.profilePicId = uploadResponse.data;

        const username = this.$store.state.logged_user;
        const setUserPicResponse = await axios.post(`${this.$store.state.API}/set_profile_picture/?username=${username}&photo_id=${photo_id}`, {
          params: {
            username: username,
            photo_id: photo_id,
          }
        });
        if (setUserPicResponse.status === 200) {
          Swal.fire({
            title: 'Erfolgreich geändert',
            text: 'Schickes Bild! ;)',
            icon: 'info',
            iconColor: '#2200cd',
            showCloseButton: false,
            confirmButtonText: 'Schließen',
            confirmButtonColor: '#2200cd',
          })
        }
        this.closeDialog();
      } catch (error) {
        console.error('An error occurred while uploading the image:', error);
      }
    },
    async changePassword() {
      if (this.newPassword == this.passwordRepeat) {
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
            })
          }
        } catch (error) {
          console.error("An error occurred while updating the password:", error);
        }
      } else {
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
        console.log("User_ID: " + this.$store.state.logged_user_id)
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
        if (response.status == 200){
        this.username = this.editedUsername;
        this.email = this.editedEmail;
        }
        this.editMode = false;
        this.$store.dispatch('login', { user: this.username, user_id: this.$store.state.logged_user_id });
        localStorage.setItem('logged_user', this.username)
      } catch (error) {
        console.error('Error updating user:', error);
      }
    },
    async fetchData() {
      try {
        const response = await axios.get(this.$store.state.API + `/users/${this.$store.state.logged_user_id}`);
        const response2 = await axios.get(this.$store.state.API + `/readFollowers/${this.$store.state.logged_user_id}`);
        const response3 = await axios.get(this.$store.state.API + `/readFollowees/${this.$store.state.logged_user_id}`);

        this.followerNumber = response2.data
        this.followingNumber = response3.data
        this.email = response.data.email
        this.profilePicId = response.data.photo_id;
        return response.data.email
      } catch (error) {
        console.log(error)
      }
    },
    async getPhoto(photoId) {
      try {
        const response = await axios.get(this.$store.state.API + `/getPhoto`, { params: { id: photoId }, responseType: 'arraybuffer' });
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
.container-fluid {
  background-color: #3c4e74;
  z-index:-2
}

.account-info {
  background-color:  #142957;
  color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
}

.title {
  font-size: 24px;
  margin-bottom: 20px;
}

.info-item {
  margin-bottom: 10px;
}

.info-item label {
  font-weight: bold;
  display: block;
  margin-bottom: 5px;
}

.info-item input[type="text"],
.info-item input[type="password"] {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.info-item input[type="text"]:focus,
.info-item input[type="password"]:focus {
  outline: none;
  border-color: #142957;
  box-shadow: 0px 0px 5px rgba(34, 0, 205, 0.5);
}

button {
  background-color: #142957;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-right: 10px;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #1a0099;
}

.profile-picture {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  margin-bottom: 20px;
}

.profile-picture i.fa-pencil {
  position: absolute;
  bottom: 0;
  right: 0;
  background-color: #2200cd;
  color: white;
  border-radius: 50%;
  padding: 5px;
  cursor: pointer;
}

.dialog-content {
  text-align: center;
}

.dialog-content h2 {
  font-size: 20px;
  margin-bottom: 10px;
}

.dialog-content input[type="file"] {
  margin-bottom: 20px;
}

.dialog-content img {
  max-width: 100%;
  height: auto;
  margin: 0 auto;
  display: block;
  margin-top: 10px;
}

.menu-button-container {
  text-align: center;
  margin-top: 20px;
}

.menu-button-container button {
  margin: 0 10px;
}

.change-password-container {
  margin-top: 20px;
}

.change-password-container input[type="password"] {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.change-password-container button {
  margin-top: 10px;
}

.delete-profile-button {
  background-color: #d0342c;
  margin-top: 20px;
}

.delete-profile-button:hover {
  background-color: #b32b27;
}

</style>
