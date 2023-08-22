import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHashHistory} from "vue-router"
import HelloWorld from "./components/HelloWorld"
import LoginPage from "./components/Login.vue"
import AccountInfo from "./components/AccountInfo.vue"
import PrivateMessenger from "./components/PrivateMessenger.vue"
import store from "./store"

import BootstrapVue3 from 'bootstrap-vue-3'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'
import '@fortawesome/fontawesome-free/css/all.css'

const app = createApp(App)
createApp(App)
const routes = [
    {path: "/", component: HelloWorld},
    {path:"/login", component: LoginPage},
    {path:"/my_account", component: AccountInfo},
    {path:"/private_messenger", component: PrivateMessenger}

]
const router = createRouter(
    {
        history: createWebHashHistory(),
        routes: routes,
        linkActiveClass: "active"
    }
)
app.use(BootstrapVue3)
app.use(router)
app.use(store)
app.mount('#app')