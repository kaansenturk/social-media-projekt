<template>
    <nav class="navbar">
      <ul class="nav-links">
        <!--<li><router-link to="/">Home</router-link></li>
        <li><router-link to="/account">Account Info</router-link></li>
        <li><router-link to="/messenger">Messenger</router-link></li>
        <button type="submit" @click="logout"></button>-->
      </ul>
    </nav>
  </template>
  <script>
  export default {
    name: 'NavBar',
    components: {
    },
    methods: {
        logout() {
  localStorage.removeItem('logegd_user_id');
  localStorage.removeItem('logged_user');
  this.$store.commit('setUser', null)
  this.$store.commit('setUserId', null)
  this.$router.push('/login')
},
    },
    data() {
      return {
      };
    },}
</script>
  <style scoped>
  .navbar {
    background-color: transparent;
    color: purple;
    display: flex;
    justify-content: center;
    max-height: 200px;
    height: 85px;
    width: 100%;
  }
  
  .nav-links {
    list-style: none;
    display: flex;
    gap: 550px;
  }
  
  .nav-links li {
    padding: 520px;
  }
  
  .nav-links li a {
    text-decoration: none;
    color: purple;
  }
  button {
    padding: 10px;
    background-color: transparent;
    color: purple;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  </style>
  