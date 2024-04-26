<script setup>
import RequestCardAdmin from "@/components/RequestCardAdmin.vue";
import store from "@/store";
</script>
<template>
  <div class="container mt-5 py-3">
    <div class="row py-3 g-4 justify-content-center">
      <div class="col-11" v-for="request in requests">
        <RequestCardAdmin :request="request" @reload-requests="getRequests" />
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "AdminViewRequests",
  data() {
    return {
      requests: [],
    };
  },
  created() {
    this.getRequests();
  },
  methods: {
    getRequests() {
      fetch(store.getters.BASEURL + "/requests", {
        method: "GET",
        headers: {
          "Authentication-Token": store.getters.getToken,
        },
      })
        .then((response) => {
          if (response.status == 200) return response.json();
          return [];
        })
        .then((data) => {
          this.requests = data;
        });
    },
  },
};
</script>

<style scoped></style>
