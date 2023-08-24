<template>
  <div class="search-container">
    <div class="row">
      <div class="col-md-6">
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
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SearchModule',
  data() {
    return {
      API: "http://localhost:8000",
      text: "",
    };
  },
  methods: {
    async handleSearch() {
      try {
        const response = await axios.get(this.API + "/get_users", {
          params: {
            text: this.text,
          },
        });
        console.log(response);
        console.log("Search completed");
      } catch (error) {
        console.error("Search error:", error);
      }
    },
  },
};
</script>

<style scoped>
.button-group {
  padding-left: 0;
  padding-right: 0;
}
.form-control {
  border-radius: 10px 0 0 10px;
  height: 15vh; /* Set height to 'auto' */
  line-height: 1.5; /* Adjust line height for better vertical alignment */
}
.search-container {
  display: flex;
  align-items: center;
  height: 20vh;
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
