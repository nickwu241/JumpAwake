<template>
  <div>
    <h1>Welcome {{$route.params.userId}}!</h1>
    <div class="d-flex justify-content-around">
      <div class="h-half">
        <h2 v-if="jumpCount !== 'null'">Lifetime jumps</h2>
        <h2 v-if="jumpCount !== 'null'" class="big-number">{{jumpCount}}</h2>
      </div>
      <div class="h-half">
        <div id="plotly-graph"></div>
      </div>
    </div>
  </div>
</template>

<script>
import Plotly from "plotly.js-dist";

export default {
  data: function() {
    return {
      jumpCount: null
    };
  },
  methods: {
    fetchCount: function() {
      fetch(`${this.$route.params.userId}/jump`)
        .then(r => r.json())
        .then(response => (this.jumpCount = response["lifetime_jumps"]))
        .catch(err => console.error(err));

      fetch(`${this.$route.params.userId}/time_series`)
        .then(r => r.json())
        .then(r => Plotly.newPlot("plotly-graph", r[0], r[1]))
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
