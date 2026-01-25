import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router"
import LoginView from "../views/LoginView.vue"
import RegistrationView from "@/views/RegistrationView.vue"
import HomeView from "@/views/HomeView.vue"

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
  },
  {
    path: "/registration",
    name: "registration",
    component: RegistrationView,
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes,
})

export default router
