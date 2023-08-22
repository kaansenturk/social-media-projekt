<template>
  <div>
    <HeaderPart></HeaderPart>
  <img class="app_icon" alt="App Logo" src="./assets/hacker.png">
  <router-view></router-view>
</div>
</template>

<script>
import HeaderPart from './components/Header.vue';
export default {
  name: 'App',
  components: {
HeaderPart
}
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.app_icon{
  width: 20%;
  margin-left: auto;
  margin-right: auto;
}
</style>
