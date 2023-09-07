<template>
  <div class="Header sticky-top">
    <div class="row align-items-center">
      <div>
        <NavBar v-if="isUserLoggedIn"></NavBar>
        <img id="app_icon" alt="App Logo" src="../assets/hacker.png">
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
import NavBar from './NavBar.vue';
import { mapState } from 'vuex';
import DropDownMenu from "./DropDownMenu.vue";
export default {
  name: 'HeaderPart',
  components: {
SearchModule,
DropDownMenu,
NavBar,
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
  
</style>