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
        <div v-if="searchResults.length"><i class="fa fa-square-xmark" @click="clearSearchResults" style=" cursor: pointer" title="Liste leeren"></i></div>
      </div>
    </div>
    <div class="search-results" v-if="searchResults.length">
      <ul class="list-group">
        <li class="list-group-item" v-for="user in searchResults" :key="user.id">
          {{ user.username }}
          <button class="btn btn-sm btn-secondary float-right" @click="followUser(user.id, user.username)">Follow</button>
          <button class="btn btn-sm btn-secondary float-right" @click="openChat"><i class="fa-regular fa-message"></i></button>

        </li>
      </ul>
      
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
      API: this.$store.state.API,
      text: "",
      searchResults: [],
    };
  },
  methods: {
    clearSearchResults(){
      this.searchResults = []
    },
    openChat(){
      this.$router.push("/messenger")
      this.searchResults = []
    },
    // method to call the getUsers rooute and get all user with a name like the query we pass it
    async handleSearch() {
      try {
        const response = await axios.get(this.API + "/getUsers", {
          params: {
            query: this.text,
          },
        });
        console.log(response);
        this.searchResults = response.data;
      } catch (error) {
        console.error("Search error:", error);
      }
    },
    async followUser(followee_id, username) {
    try {

      const follower_id = this.$store.state.logged_user_id;
      const response = await axios.post(this.API + "/createFollower", {
        followee: followee_id,
        owner_id: follower_id
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
        this.clearSearchResults()
 } 
else{
  console.log("ciao")
}
window.location.reload();
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
  line-height: 1;
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
