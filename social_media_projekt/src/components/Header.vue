<template>
  <div class="Header sticky-top">
    <div class="row ">
      <div class="col-md-2">
        <img id="app_icon" alt="App Logo" src="../assets/hacker.png">
      </div>
      <NavBar v-if="isUserLoggedIn" class="col-md-6" ></NavBar>
      <div v-if="isUserLoggedIn" class="col-md-4 d-flex justify-content-end">
        <SearchModule />
      </div>
    </div>
  </div>
</template>

<script>
import SearchModule from './SearchModule.vue';
import NavBar from './NavBar.vue';
import { mapState } from 'vuex';
export default {
  name: 'HeaderPart',
  components: {
SearchModule,
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
  width: 100px;
}

/* Overriding Bootstrap's sticky-top styles to make sure it sticks to the top */
.sticky-top {

  position: sticky;
  top: 2vh;
  z-index: 1020; /* Ensure it appears above other elements */
}
  
</style>