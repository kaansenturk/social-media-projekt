<template>
    <div class="post-container">  
    <form>
      <textarea  id="post_text" placeholder="What's on your mind..." required v-model="text" />
      
      <button type="button" @click.prevent="upload_post(this.text)">posten</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'postCreator',
  props: {
    
  },
  data() {
    return {
      API: "http://localhost:8000",
    }},
    methods: {
      upload_post(text){
          {
            try
            {
              const response =  axios.post(this.API + "/create_post", null, {
      params: {
        username: this.username,
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
  width: 100%;
  height: 100px;
}
  
  .post-container {
    margin-left: auto;
    margin-right: auto;
    width: 30%;
    height: 20%;
    padding: 30px;
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