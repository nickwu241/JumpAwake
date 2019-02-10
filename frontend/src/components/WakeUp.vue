<template>
  <div>
    <h1>{{jumpCount}}</h1>
  </div>
</template>

<script>
export default {
  name: "wake-up",
  data: function() {
    return {
      jumpCount: 0
    };
  },
  methods: {
    fetchCount: function() {
      fetch("/nick/jump")
        .then(r => r.json())
        .then(response => (this.jumpCount = response["jumps"]))
        .catch(err => console.error(err));
    }
  },
  mounted: function() {
    this.interval = setInterval(() => {
      this.fetchCount();
    }, 1000);
  },
  beforeDestroy: function() {
    clearInterval(this.interval);
  }
};
</script>

<style>
</style>
