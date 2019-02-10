<template>
  <div class="d-flex justify-content-around">
    <div :class="{'h-half': hasOpponent}" v-if="jumpCount !== null">
      <h1>Your jumps</h1>
      <h1 class="big-number text-success">{{jumpCount}}</h1>
    </div>
    <div class="h-half" v-if="hasOpponent">
      <h1>Their jumps</h1>
      <h1 class="big-number text-danger">{{otherUserJumpCount}}</h1>
    </div>
  </div>
</template>

<script>
export default {
  name: "wake-up",
  data: function() {
    return {
      jumpCount: null,
      otherUsername: "",
      otherUserJumpCount: null
    };
  },
  methods: {
    fetchCount: function() {
      fetch(`${this.$route.params.userId}/jump`)
        .then(r => r.json())
        .then(response => {
          this.jumpCount = response["jumps"];
        })
        .catch(err => console.error(err));
    }
  },
  computed: {
    hasOpponent: function() {
      return this.otherUserJumpCount !== null;
    }
  },
  mounted: function() {
    this.fetchCount();
  },
  socket: {
    events: {
      jumps(data) {
        console.log("[WS jump]", data);
        let otherUsers = Object.keys(data).filter(
          user => user !== this.$route.params.userId
        );
        if (otherUsers.length > 1) {
          console.warn(`[WS] There is ${otherUsers.length} other users...`);
        } else if (otherUsers.length == 1) {
          console.log(`[WS] Displaying other user's jump data...`);
          console.log(otherUsers);
          this.otherUser = otherUsers[0];
          this.otherUserJumpCount = data[this.otherUser]["jumps"];
        }

        if (data[this.$route.params.userId]) {
          this.jumpCount = data[this.$route.params.userId]["jumps"];
        }
      },
      connect() {
        this.$socket.emit("join", this.$route.params.userId);
        console.log("[WS] joined socket as", this.$socket.id);
      },
      disconnect() {
        this.$socket.emit("leave", this.$route.params.userId);
        console.log("[WS] left socket as", this.$socket.id);
      }
    }
  }
};
</script>

<style>
</style>
