<template>
  <div>
    <h1 v-if="jumpCount !== null">Your jumps: {{jumpCount}}</h1>
    <h1 v-if="otherUserJumpCount !== null">{{otherUser}}'s jumps: {{otherUserJumpCount}}</h1>
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
        this.jumpCount = data[this.$route.params.userId]["jumps"];
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
