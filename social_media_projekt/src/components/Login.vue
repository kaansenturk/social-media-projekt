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
      <input type="text" id="email" placeholder="Email" required v-model="email">
      <input type="password" id="password" placeholder="Password" required v-model="password">
      <input type="password" id="repeat_password" placeholder="Password wiederholen" required v-model="repeat_password">

      <button type="button" @click.prevent="register_new_user">Registrieren</button>
      <button type="button" @click.prevent="showRegister = !showRegister">Back to Login</button>
  
    </form>
  </div>
</template>

<script>
import axios from 'axios';
import { mapState } from 'vuex';
import Swal from 'sweetalert2/dist/sweetalert2.js'
import 'sweetalert2/dist/sweetalert2.min.css';
export default {
  name: 'LoginPage',
  props: {
    
  },
  data() {
    return {
      username: "",
      password: "",
      repeat_password:"",
      email: "",
      API: "http://localhost:8000",
      showRegister: false,
    }},
    methods: {
      // method to call api route to create a new user in the database
      async register_new_user(){
          if(this.showRegister && this.repeat_password === this.password){
            try
            {
              const response = await axios.post(this.$store.state.API + "/createUser",  {
              email: this.email,
              username: this.username,
              password: this.password,   
    })
    console.log(response.data)
    this.showSuccess();
            }
            catch
            {
              return
            }
          }
      },
      // method to create a Login for a user that exists in the db, also sets items in the vuex state management and localstorage
      async login_try(){
    try {
        const response = await axios.post(this.$store.state.API + "/login", {
            user: this.username,
            password: this.password,
        });
        if (response.data) {
          console.log(response.data.id)
            this.getUser(response.data.username);
            this.$store.dispatch('login', { user: response.data.username, user_id: response.data.id });
            localStorage.setItem('logged_user', response.data.username)
            localStorage.setItem('logged_user_id', response.data.id)
            this.$router.push('/');
            console.log(this.$store.state.logged_user,this.$store.state.logged_user_id)
        }
    } catch (error) {
      console.log(this.username, this.password)
        if (error.response && error.response.data && error.response.data.detail) {
            console.log(error.response.data.detail); 
        } else {
            console.log(error);
        }
    }
},
  getUser(name){
    this.username = name
  },
  // method to create a popup toast with sweetalert
  showSuccess(){
    Swal.fire({
      title: 'Erfolgreich registriert',
      text: 'Du kannst dich jetzt einloggen',
       icon: 'info',
      iconColor: '#2200cd',
      showCloseButton: false,
      confirmButtonText: 'Schließen',
      confirmButtonColor: '#2200cd',
    }).then((result) => {
      if (result.value) {
        console.log("Hi")
        this.showRegister = !this.showRegister
 } 
else{
  console.log("ciao")
}
})},
  
},
computed: {
  ...mapState(['user']),
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