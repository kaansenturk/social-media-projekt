<template>
  <div class="Header sticky-top">
    <div class="row ">
      <div class="col-md-2">
        <img id="app_icon" alt="App Logo" src="../assets/hacker.png">
      </div>
      <div class="col-md-10 d-flex justify-content-end">
        <SearchModule />
      </div>
    </div>
  </div>
</template>

<script>
import SearchModule from './SearchModule.vue';
export default {
  name: 'HeaderPart',
  components: {
SearchModule,
  },
  props: {
    friends: {
      type: Array,
      required: false,
    },
    userId: Number,
  },
  data() {
    return {

    }},
    methods: {
}

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