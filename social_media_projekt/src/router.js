import Vue from 'vue';
import VueRouter from 'vue-router';
import HelloWorld from "./components/HelloWorld" 
import LoginPage from "./components/Login.vue"
import AccountInfo from "./components/AccountInfo.vue"

Vue.use(VueRouter);


  const routes  = [
     
      {path: "/", component: HelloWorld},
      {path:"/login", component: LoginPage},
      {path:"/my_account", component: AccountInfo},
  
  ]

  const router = new VueRouter({
    routes
  });


export default router;
