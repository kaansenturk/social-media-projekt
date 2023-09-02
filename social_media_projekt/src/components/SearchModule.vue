<template>
  <div class="search-container">
    <div class="row">
      <div class="col-md-9">
        <input
          id="post_text"
          class="form-control"
          placeholder="Search..."
          required
          v-model="text"
        />
      </div>
      <div class="col-md-2 button-group">
        <button class="btn btn-primary btn-block search-button" @click.prevent="handleSearch">
          <i class="fa-solid fa-magnifying-glass" style="color: #f1dbff;"></i>
        </button>
      </div>
    </div>
    <div class="search-results" v-if="searchResults.length">
      <ul class="list-group">
        <li class="list-group-item" v-for="user in searchResults" :key="user.id">
          {{ user.username }}
          <button class="btn btn-sm btn-secondary float-right" @click="followUser(user.id, user.username)">Follow</button>
          <button class="btn btn-sm btn-secondary float-right" @click="chatWithUser(user.id, user.username)"><i class="fa-regular fa-message"></i></button>

        </li>
      </ul>
      <i class="fa-solid fa-messages"></i>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Swal from 'sweetalert2/dist/sweetalert2.js'
import 'sweetalert2/dist/sweetalert2.min.css';

export default {
  name: 'SearchModule',
  data() {
    return {
      API: "http://localhost:8000",
      text: "",
      searchResults: [],
    };
  },
  methods: {
    async chatWithUser(user_id, username){
      try {
        console.log("Hi", user_id)
      }
      catch {
        console.log("Hi", username)
      }
    },
    async handleSearch() {
      try {
        const response = await axios.get(this.API + "/getUsers", {
          params: {
            query: this.text,
          },
        });
        print
        console.log(response);
        console.log(response.data);
        console.log("Search completed");
        this.searchResults = response.data;
      } catch (error) {
        console.error("Search error:", error);
      }
    },
    async followUser(followerId, username) {
    try {

      const followee_id = this.$store.state.logged_user_id;
      console.log(followee_id, followerId)
      const response = await axios.post(this.API + "/createFollower", {
        followee: followee_id,
        owner_id: followerId
      });
      if (response.data) {
        Swal.fire({
      title: 'Folgen erfolgreich',
      text: `Du folgst jetzt ${username}`,
       icon: 'info',
      iconColor: '#2200cd',
      showCloseButton: false,
      confirmButtonText: 'Schließen',
      confirmButtonColor: '#2200cd',
    }).then((result) => {
      if (result.value) {
        console.log("Hi")
        this.showRegister = !this.showRegister
 } 
else{
  console.log("ciao")
}
})
      }
    } catch (error) {
      console.error("Error following user:", error);
    }
  }
  },
};
</script>

<style scoped>
.search-results {
  margin-top: 15px;
}
.button-group {
  padding-left: 0;
  padding-right: 0;
}
.form-control {
  border-radius: 10px 0 0 10px;
  height: 15vh; 
  line-height: 1.5;
}
.search-container {
  position: absolute;
  display: inline-block;
  top: 0px; 
  right: 10px; 
}

.input-group {
  display: flex;
  align-items: center;
}

.form-control {
  border-radius: 10px 0 0 10px;
}

.input-group-append {
  display: flex;
}

.search-button {
  border-radius: 0 10px 10px 0;
  background-color: #2200cd;
  color: #fff;
}
</style>
