<template>
    <div class="Header">
    <SearchModule class=""></SearchModule>
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
  getData(){
    // Get requests for users friends with userId
  },
}

}

</script>

<style>
  
  .Header {
  display: flex;
  flex-direction: column;
}

.friend-item {
  margin: 0px 5px 0px 5px;
}

.friends-container {
    width: 12%;
  position: fixed;
  right: 20px; 
  top: 40%; 
  height: 40%;
  transform: translateY(-50%);
  border: solid 2px blue;
  border-radius: 2px;
}
  
</style>