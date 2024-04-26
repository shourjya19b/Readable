<script setup>
import IssueCardAdmin from "@/components/IssueCardAdmin.vue";
import store from "@/store";
</script>
<template>
  <div class="container mt-5 py-3">
    <div class="row py-3 g-4 justify-content-center">
      <div class="col-11" v-for="issue in issues">
        <IssueCardAdmin :issue="issue" @reload-issues="getIssues" />
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "AdminViewIssues",
  data() {
    return {
      issues: [],
    };
  },
  created() {
    this.getIssues();
  },
  methods: {
    getIssues() {
      fetch(store.getters.BASEURL + "/admin/issues", {
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
          this.issues = data;
        });
    },
  },
};
</script>

<style scoped></style>
