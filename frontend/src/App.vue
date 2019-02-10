<template>
  <div id="app" class="conatiner">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <router-link to="/">Home</router-link>
      <router-link to="/wakeup">Wake Up</router-link>
    </nav>
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
}
</style>
