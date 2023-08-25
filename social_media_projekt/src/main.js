import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHashHistory} from "vue-router"
import HelloWorld from "./components/HelloWorld"
import LoginPage from "./components/Login.vue"
import AccountInfo from "./components/AccountInfo.vue"
import PrivateMessenger from "./components/PrivateMessenger.vue"
import store from "./store"
import HomePage from "./components/Homepage"

import BootstrapVue3 from 'bootstrap-vue-3'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'
import '@fortawesome/fontawesome-free/css/all.css'

const app = createApp(App)
createApp(App)
const routes = [
    {path: "/", component: HelloWorld, meta: { requiresAuth: true }},
    {path: "/home", component: HomePage, meta: { requiresAuth: true }},

    {path:"/login", component: LoginPage},
    {path:"/account", component: AccountInfo, meta: { requiresAuth: true }},
    {path:"/messenger", component: PrivateMessenger, meta: { requiresAuth: true }}

]
const router = createRouter(
    {
        history: createWebHashHistory(),
        routes: routes,
        linkActiveClass: "active"
    }
)
// always check if user is logged in before allowing routes other then login
router.beforeEach((to, from, next) => {
    console.log("Logged in?")
    if (to.meta.requiresAuth && !store.getters.isLoggedIn) {
      next('/login');
    } else {
      next();
    }
  });
app.use(BootstrapVue3)
app.use(router)
app.use(store)
app.mount('#app')