import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHashHistory} from "vue-router"
import HelloWorld from "./components/HelloWorld"
import LoginPage from "./components/Login.vue"
import AccountInfo from "./components/AccountInfo.vue"
const app = createApp(App)
createApp(App)
const routes = [
    {path: "/", component: HelloWorld},
    {path:"/login", component: LoginPage},
    {path:"/my_account", component: AccountInfo},
]
const router = createRouter(
    {
        history: createWebHashHistory(),
        routes: routes,
        linkActiveClass: "active"
    }
)

app.use(router)
app.mount('#app')