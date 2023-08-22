<template>
    <div class="login-container">
      <h1>{{ showRegister ? 'Registrieren' : 'Login' }}</h1>
    <form v-if="!showRegister" id="login-form">
      <input type="text" id="username" placeholder="Username" required v-model="username">
      <input type="password" id="password" placeholder="Password" required v-model="password">
      <button type="submit" @click.prevent="login_try">Log in</button>
      <button type="button" @click.prevent="showRegister = !showRegister">Registrieren</button>
    </form>
    <form v-else>
      <input type="text" id="username" placeholder="Username" required v-model="username">
      <input type="mail" id="email" placeholder="Email" required v-model="email">
      <input type="password" id="password" placeholder="Password" required v-model="password">
      <input type="password" id="password" placeholder="Password wiederholen" required>

      <button type="button" @click.prevent="register_new_user">Registrieren</button>
  
    </form>
  </div>
</template>

<script>
import axios from 'axios';
import { mapState, mapActions } from 'vuex';
export default {
  name: 'LoginPage',
  props: {
    
  },
  data() {
    return {
      username: "",
      password: "",
      API: "http://localhost:8000",
      showRegister: false,
    }},
    methods: {
      ...mapActions(['login', 'logout']),
      register_new_user(){
          if(this.showRegister){
            try
            {
              console.log("Fred")
            }
            catch
            {
              return
            }
          }
      },
  login_try(){
    try {
    const response =  axios.post(this.API + "/login_try", null, {
      params: {
        username: this.username,
        password: this.password,
      }
    })
    this.login(this.username);
    console.log(response)
  } catch (error) {
    console.log(error)
  }
  },
  getUser(name){
    this.username = name
  }
  
},
computed: {
  ...mapState(['user']),
    count () {
      return this.$store.state.count
    },
    isLoggedIn() {
      return this.$store.getters.isLoggedIn;
    },
    currentUser() {
      return this.$store.getters.currentUser;
    },
  }
}

</script>

<style>
  
  .login-container {
    margin-left: auto;
    margin-right: auto;
    width: 300px;
    padding: 20px;
    background-color: #fff;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }
  
  .login-container h1 {
    text-align: center;
  }
  
  .login-container input[type="text"],
  .login-container input[type="password"] {
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
  }
  
  .login-container button {
    width: 100%;
    padding: 10px;
    background-color: #2200cd;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .login-container button:hover {
    background-color: #2200cd;
  }
  
</style>