import Vue from 'vue'
import VueRouter from 'vue-router'

import App from './App.vue'
import WakeUp from "./components/WakeUp.vue";
import Home from "./components/Home.vue";

Vue.config.productionTip = false
Vue.use(VueRouter)

const routes = [{
    path: "/",
    component: Home
  },
  {
    path: "/wakeup",
    component: WakeUp
  }
];

const router = new VueRouter({
  routes
});

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')