<script setup>
import { RouterView } from "vue-router";
import Navbar from "@/components/Navbar.vue";
</script>
<template>
  <Navbar :links="links" :admin="true" />
  <RouterView />
</template>
<script>
export default {
  name: "AdminLayout",
  data() {
    return {
      links: [
        { path: "/admin/board", name: "Home" },
        { path: "/admin/requests/view", name: "Requests" },
        { path: "/admin/issues/view", name: "Issues" },
        { path: "/admin/summary", name: "Stats" },
      ],
      admin: true,
    };
  },
  components: { Navbar },
};
</script>
