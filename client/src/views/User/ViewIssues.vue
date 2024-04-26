<script setup>
import IssueCardUser from "@/components/IssueCardUser.vue";
import store from "@/store";
</script>
<template>
  <div class="container mt-5 py-3">
    <div class="row py-3 g-4 justify-content-center">
      <div class="col-11" v-for="issue in issues">
        <IssueCardUser :issue="issue" @reload-issues="getIssues" />
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "UserViewIssues",
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
      fetch(store.getters.BASEURL + "/user/issues", {
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

<style scoped>
.btn {
  background: white;
  color: dimgray;
}
.btn:hover {
  text-shadow: 0.25px 0.25px 0 black;
}
</style>
