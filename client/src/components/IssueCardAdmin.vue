<script setup>
import store from "@/store";
</script>
<template>
  <div class="row p-4 bg-white shadow-sm rounded">
    <div class="col-3 fw-semibold py-2">
      {{ issue.book_name }}
    </div>
    <div class="col-2 py-2 fw-semibold text-secondary">
      {{ issue.book_section }}
    </div>
    <div class="col-2 py-2 fw-semibold text-secondary">
      <i class="fa-solid fa-user me-2"></i>{{ issue.username }}
    </div>
    <div class="col-5 text-center">
      <div class="row justify-content-end">
        <button class="col-3 btn rounded-pill fw-semibold me-3" @click="revoke">
          Revoke
        </button>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "IssueCardAdmin",
  props: ["issue"],
  data() {
    return {
      revoked: false,
    };
  },
  methods: {
    revoke(event) {
      event.preventDefault();
      fetch(store.getters.BASEURL + `/issue/revoke`, {
        method: "POST",
        headers: {
          "Authentication-Token": store.getters.getToken,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          issue_id: this.issue.id,
        }),
      }).then((response) => {
        if (response.status == 200) {
          this.revoked = true;
          this.$emit("reloadIssues");
        }
      });
    },
  },
};
</script>
<style scoped>
.card-title {
  text-decoration: none;
  color: dimgray;
}
.card-img-top {
  opacity: 0.8;
}
.btn {
  color: dimgray;
  background: white;
  border: 1px solid #ed7966;
}
.btn:hover {
  background: #ed7966;
  color: white;
}
i {
  color: hwb(203 17% 41%);
}
.card-link:hover {
  text-shadow: 0.25px 0.25px 0 black;
}
.card-footer {
  border-top: none;
}
</style>
