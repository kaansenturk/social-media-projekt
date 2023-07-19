<template>
  <div>
  <img class="app_icon" alt="App Logo" src="./assets/hacker.png">
  <router-view></router-view>
</div>
</template>

<script>

export default {
  name: 'App',
  components: {
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
