<script setup>
import { RouterLink } from "vue-router";
import store from "@/store";
</script>
<template>
  <div class="row p-4 bg-white shadow-sm rounded">
    <div class="col-3 fw-semibold py-2">
      {{ issue.book_name }}
    </div>
    <div class="col-4 py-2 fw-semibold text-secondary">
      {{ issue.book_section }}
    </div>
    <div class="col-5">
      <div class="row justify-content-end">
        <RouterLink
          class="col-3 btn rounded-pill fw-bold mx-3"
          :to="{
            name: 'book_review',
            params: { book_id: issue.book_id },
            query: {
              name: issue.book_name,
              section: issue.book_section,
            },
          }"
        >
          Review
        </RouterLink>
        <button class="col-3 btn rounded-pill fw-bold me-3" @click="returnBook">
          Return
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
      returned: false,
    };
  },
  methods: {
    returnBook(event) {
      event.preventDefault();
      fetch(store.getters.BASEURL + `/issue/return`, {
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
          this.returned = true;
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
  border: 1px solid hwb(203 17% 41%);
}
.btn:hover {
  background: hsl(203, 55%, 38%);
  color: white;
}
i {
  color: #ed7966;
}
.card-link:hover {
  text-shadow: 0.25px 0.25px 0 black;
}
.card-footer {
  border-top: none;
}
</style>
