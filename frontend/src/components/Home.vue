<template>
  <div>
    <h1>Hello, Welcome to the Home page!</h1>
    <h2 v-if="jumpCount">Your lifetime jumps: {{jumpCount}}</h2>
  </div>
</template>

<script>
export default {
  data: function() {
    return {
      jumpCount: null
    };
  },
  methods: {
    fetchCount: function() {
      fetch("/nick/jump")
        .then(r => r.json())
        .then(response => (this.jumpCount = response["lifetime_jumps"]))
        .catch(err => console.error(err));
    }
  },
  mounted: function() {
    this.fetchCount();
  }
};
</script>

<style>
</style>
