<template>
  <div>
    <h1 v-if="jumpCount !== null">{{jumpCount}}</h1>
  </div>
</template>

<script>
export default {
  name: "wake-up",
  data: function() {
    return {
      jumpCount: null
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
    this.fetchCount();
  },
  socket: {
    events: {
      jumps: function(jumpCount) {
        this.jumpCount = jumpCount;
      }
    }
  }
};
</script>

<style>
</style>
