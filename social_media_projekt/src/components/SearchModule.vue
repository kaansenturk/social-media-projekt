<template>
  <div class="search-container">
    <div class="row">
      <div class="col-md-9 search">
        <input
          id="post_text"
          class="form-control"
          placeholder="Search..."
          required
          v-model="text" />
      </div>
      <div class="col-md-2 button-group">
        <button
          class="btn btn-primary btn-block search-button"
          @click.prevent="handleSearch">
          <i class="fa-solid fa-magnifying-glass" style="color: #f1dbff"></i>
        </button>
      </div>
      <div class="col-md-2 button-group">
        <div v-if="searchResults.length">
          <i
            class="fa fa-square-xmark"
            @click="clearSearchResults"
            style="cursor: pointer"
            title="Liste leeren"></i>
        </div>
      </div>
    </div>
    <div
      class="search-results"
      v-if="searchResults.length"
      style="max-height: 290px; overflow-y: auto">
      <ul class="list-group">
        <li
          class="list-group-item"
          v-for="user in searchResults"
          :key="user.id">
          {{ user.username }}
          <button
            class="btn btn-sm btn-secondary float-right"
            @click="followUser(user.id, user.username)">
            Follow
          </button>
          <button
            class="btn btn-sm btn-secondary float-right"
            @click="openChat">
            <i class="fa-regular fa-message"></i>
          </button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2/dist/sweetalert2.js";
import "sweetalert2/dist/sweetalert2.min.css";

export default {
  name: "SearchModule",
  data() {
    return {
      API: this.$store.state.API,
      text: "",
      searchResults: [],
    };
  },
  methods: {
    clearSearchResults() {
      this.searchResults = [];
    },
    openChat() {
      this.$router.push("/messenger");
      this.searchResults = [];
    },
    // method to call the getUsers rooute and get all user with a name like the query we pass it
    async handleSearch() {
      try {
        const response = await axios.get(this.API + "/getUsers", {
          params: {
            query: this.text,
          },
        });

        this.searchResults = response.data.filter(
          (user) => user.id != this.$store.state.logged_user_id
        );
      } catch (error) {
        console.error("Search error:", error);
      }
    },
    async followUser(followee_id, username) {
      try {
        console.log("TEST");
        const response = await axios.post(this.API + "/createFollower", {
          followee: followee_id,
          owner_id: this.$store.state.logged_user_id,
        });
        console.log(response.data);
        if (response.data) {
          Swal.fire({
            title: "Folgen erfolgreich",
            text: `Du folgst jetzt ${username}`,
            icon: "info",
            iconColor: "#2200cd",
            showCloseButton: false,
            confirmButtonText: "Schließen",
            confirmButtonColor: "#2200cd",
          }).then((result) => {
            if (result.value) {
              this.clearSearchResults();
            }
            window.location.reload();
          });
        }
      } catch (error) {
        console.error("Error following user:", error);
        if (error.code == "ERR_BAD_REQUEST") {
          Swal.fire({
            title: "Error",
            text: "You already follow this user",
            icon: "info",
            iconColor: "#d0342c",
            showCloseButton: false,
            confirmButtonText: "Schließen",
            confirmButtonColor: "#d0342c",
          });
        }
      }
    },
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
  padding: 6px 12px;
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
  margin: 20px;
  height: 50px;
}

#post_text {
  height: 50px;
  margin: 20px;
  padding: 20px;
}

.fa-square-xmark {
  color: red;
}
</style>
