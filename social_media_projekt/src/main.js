import { createApp } from "vue";
import App from "./App.vue";
import { createRouter, createWebHashHistory } from "vue-router";
import LoginPage from "./components/Login.vue";
import AccountInfo from "./components/AccountInfo.vue";
import PrivateMessenger from "./components/PrivateMessenger.vue";
import store from "./store";
import HomePage from "./components/Homepage";
import FollowerPage from "./components/FollowerPage";
import PostComments from "./components/PostComments";
import CreditPage from "./components/CreditPage";

import BootstrapVue3 from "bootstrap-vue-3";

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue-3/dist/bootstrap-vue-3.css";
import "@fortawesome/fontawesome-free/css/all.css";
import FriendPage from "./components/FriendPage";
import PostLikeList from "./components/PostLikeList";
import CommentLikeList from "./components/CommentLikeList";

const app = createApp(App);
createApp(App);
const routes = [
  { path: "/", component: HomePage, meta: { requiresAuth: true } },
  { path: "/login", component: LoginPage },
  { path: "/account", component: AccountInfo, meta: { requiresAuth: true } },
  {
    path: "/messenger",
    component: PrivateMessenger,
    meta: { requiresAuth: true },
  },
  {
    path: "/friend",
    component: FriendPage,
    meta: { requiresAuth: true },
    name: "friend",
  },
  { path: "/follower", component: FollowerPage, meta: { requiresAuth: true } },
  {
    path: "/postComments",
    component: PostComments,
    meta: { requiresAuth: true },
    name: "postComments",
  },
  {
    path: "/postLikeList",
    component: PostLikeList,
    meta: { requiresAuth: true },
    name: "postLikeList",
  },
  {
    path: "/commentLikeList",
    component: CommentLikeList,
    meta: { requiresAuth: true },
    name: "commentLikeList",
  },
  { path: "/credits", component: CreditPage, meta: { requiresAuth: true } },
];
const router = createRouter({
  history: createWebHashHistory(),
  routes: routes,
  linkActiveClass: "active",
});
// always check if user is logged in before allowing routes other then login
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !store.getters.isLoggedIn) {
    next("/login");
  } else {
    next();
  }
});
// for refresh of page, if user hasn't logged out, the important info gets reloaded into the store
if (
  localStorage.getItem("logged_user") &&
  localStorage.getItem("logged_user_id")
) {
  const user = localStorage.getItem("logged_user");
  const user_id = localStorage.getItem("logged_user_id");
  store.commit("setUser", user);
  store.commit("setUserId", user_id);
}
store.commit("setApi", process.env.VUE_APP_API_URL);
app.use(BootstrapVue3);
app.use(router);
app.use(store);

app.mount("#app");
