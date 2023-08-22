<template>
    <div class="post-container">  
    <form>
        <span>
      <input  id="post_text" placeholder="What's on your mind..." required v-model="text" />
      <button class="search-button" @click="handleSearch">
    <i class="fa-solid fa-magnifying-glass"  style="color: #f1dbff;"></i>
    
  </button>
</span>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SearchModule',
  props: {
    
  },
  data() {
    return {
      API: "http://localhost:8000",
    }},
    methods: {
      search(text){
          {
            try
            {
              const response =  axios.get(this.API + "/get_users", null, {
      params: {
        text: text,
      }
      
    })
    console.log(response)
              console.log("Fred")
            }
            catch
            {
              return
            }
          }
      },
  login_try(){
    
    
  },
  getUser(name){
    this.username = name
  }
  
}
}

</script>

<style>
#post_text {
  width: 70%;
  height: 20px;
}
.search-button {
    background-color: #2200cd;
    border-radius: 10px;
    margin-left: 5px;

}
  
  .post-container {
    margin-left: auto;
    margin-right: auto;
    width: 25%;
    height: 10%;
    padding: 15px;
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