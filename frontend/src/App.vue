<template>
  <div id="app" class="conatiner">
    <!-- <router-link to="/" class="nav-link">Home</router-link>
    <router-link to="/nick" class="nav-link">Dashboard</router-link>
    <router-link to="/nick/wakeup" class="nav-link">Wake Up</router-link>-->
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "app"
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.big-number {
  font-size: 200px;
}

.h-half {
  min-width: 50%;
  max-width: 50%;
}
</style>
