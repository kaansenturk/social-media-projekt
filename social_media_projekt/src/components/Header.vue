<template>
  <div class="Header sticky-top">
    <div class="row align-items-center">
      <div>
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
    }},
    methods: {
},

}

</script>

<style>
#navbar {
  background-color: #3c4e74;
}

.Header {
  background-color: transparent;
}

.logo-container {
  position: absolute;
  top: 30px;
  right: 4%;
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
  z-index: 1020; /* Ensure it appears above other elements */
}

#headerBar {
  height: 100px;
  background-color: #DAF7A6;
}
</style>
