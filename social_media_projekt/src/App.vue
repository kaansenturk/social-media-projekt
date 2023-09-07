<template>
  <div>
    <HeaderPart class="header"></HeaderPart>
  <router-view></router-view>
</div>
</template>

<script>
import HeaderPart from './components/Header.vue';
export default {
  name: 'App',
  components: {
HeaderPart
},

}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-color: #F8F9F9;
}

</style>
