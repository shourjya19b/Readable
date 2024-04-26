<script setup>
import { RouterView } from "vue-router";
import Navbar from "@/components/Navbar.vue";
</script>
<template>
  <Navbar :links="links" :admin="false" />
  <RouterView />
</template>
<script>
export default {
  name: "UserLayout",
  data() {
    return {
      links: [
        { path: "/user/board", name: "Home" },
        { path: "/user/issues/view", name: "Issues" },
        { path: "/user/summary", name: "Stats" },
      ],
      admin: false,
    };
  },
  components: { Navbar },
};
</script>
