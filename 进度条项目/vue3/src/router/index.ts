import {createRouter, createWebHashHistory} from "vue-router";
import History from "@/views/History.vue";
import HomePage from "@/views/HomePage.vue";
import ChatGPT from "@/views/ChatGPT.vue";
import Login from  "@/views/Login.vue"
import Echarts from "@/views/Echarts.vue"
import ViolationHandling from "@/views/ViolationHandling.vue"
import TempPage from "@/views/TempPage.vue"

const router = createRouter({
    history: createWebHashHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            redirect: '/login'
        },
        {
            path: '/home',
            redirect: '/home/chatgpt',
            meta: {islogin : true}
        },
        {
            path: '/home',
            name: 'home',
            component: HomePage,
            children: [
                {
                    path: 'chatgpt',
                    name: 'chatgpt',
                    component: ChatGPT,
                    meta: {islogin : true}
                },
                {
                    path: "history",
                    name: "history",
                    component: History,
                    meta: {islogin : true}
                },
                {
                    path: "echarts",
                    name: "echarts",
                    component: Echarts,
                    meta: {islogin : true}
                },
                {
                    path: "violation",
                    name: "ViolationHandling",
                    component: ViolationHandling,
                    meta: {islogin : true}
                },
                {
                    path: "temp",
                    name: "temp",
                    component: TempPage,
                    meta: {islogin : true}
                },


            ]
        },
        {
            path: "/login",
            name: "login",
            component: Login,
        }
    ],
});
router.beforeEach((to, from, next) => {
      console.log(to)
      console.log(from)
    if (to.meta.islogin){
        let token = localStorage.getItem('token') //获取存储对象
        if (token == null){
            return  next({path: '/login'})
        }

    }
      return next()
    }
)
export default router;
