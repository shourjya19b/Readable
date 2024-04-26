<script setup>
import { RouterView } from "vue-router";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.min.js";
import store from "@/store";
</script>

<template>
  <RouterView />
</template>
<script>
export default {
  created() {
    let user = JSON.parse(sessionStorage.getItem("user"));
    if (!user) user = { roles: [], token: null };
    store.commit("setUser", user);
  },
};
</script>
<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
body {
  background: #faeecd;
  background: #fffbf1;
}
#app {
  font-family: Poppins;
}
</style>
