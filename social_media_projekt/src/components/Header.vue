<template>
  <div class="Header sticky-top">
    <div class="row">
      <div class="col-md-0">
        <div v-if="isUserLoggedIn" id="headerBar"></div>
        <img id="app_icon" alt="App Logo" src="../assets/hacker.png">
        <div class="logo-container">
          Social Media Projekt
        </div>
      </div>
      <div class="d-flex justify-content-end">
        <div v-if="isUserLoggedIn">
          <DropDownMenu />
          <SearchModule />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SearchModule from './SearchModule.vue';
import { mapState } from 'vuex';
import DropDownMenu from "./DropDownMenu.vue";
export default {
  name: 'HeaderPart',
  components: {
    SearchModule,
    DropDownMenu,
  },
  props: {
  },
  computed: {
    ...mapState(['logged_user']),
    isUserLoggedIn() {
      return this.logged_user !== null;
    },
  },
  data() {
    return {
    }
  },
  methods: {
  },

}

</script>

<style>
.row {
  max-width: 100%;
}

#navbar {
  background-color: #3c4e74;
}

.Header {
  background-color: #3c4e74;
  height: 100px;
  border-bottom: 1px solid grey;
}

.logo-container {
  position: absolute;
  top: 30px;
  text-align: center;
  width: 100%;
  height: 110px;
  font-size: 24px;
  font-family: 'Courier New', monospace;
  color: #fff;
}

#app_icon {
  width: 70px;
  position: absolute;
  display: inline-block;
  top: 10px;
  left: 80px;
}

/* Overriding Bootstrap's sticky-top styles to make sure it sticks to the top */
.sticky-top {
  position: sticky;
  z-index: 1020;
  /* Ensure it appears above other elements */
}

</style>
