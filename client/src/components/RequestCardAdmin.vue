<script setup>
import store from "@/store";
</script>
<template>
  <div class="row p-4 bg-white shadow-sm rounded">
    <div class="col-3 fw-semibold py-2">
      {{ request.book_name }}
    </div>
    <div class="col-2 py-2 fw-semibold text-secondary">
      {{ request.book_section }}
    </div>
    <div class="col-2 py-2 fw-semibold text-secondary">
      <i class="fa-solid fa-user me-2"></i>{{ request.username }}
    </div>
    <div class="col-5 text-center">
      <div class="row justify-content-end">
        <button
          class="col-2 btn rounded-pill fw-semibold me-3"
          @click="grantRequest"
        >
          Grant
        </button>
        <button
          class="col-3 btn cnl-btn rounded-pill fw-semibold me-2"
          @click="cancelRequest"
        >
          Cancel
        </button>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "RequestCardAdmin",
  props: ["request"],
  data() {
    return {
      granted: false,
      cancelled: false,
    };
  },
  methods: {
    grantRequest(event) {
      event.preventDefault();
      fetch(store.getters.BASEURL + `/request/grant`, {
        method: "POST",
        headers: {
          "Authentication-Token": store.getters.getToken,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          request_id: this.request.id,
        }),
      }).then((response) => {
        if (response.status == 200) {
          this.granted = true;
          this.$emit("reloadRequests");
        }
      });
    },
    cancelRequest(event) {
      event.preventDefault();
      fetch(store.getters.BASEURL + `/request/cancel`, {
        method: "POST",
        headers: {
          "Authentication-Token": store.getters.getToken,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          request_id: this.request.id,
        }),
      }).then((response) => {
        if (response.status == 200) {
          this.cancelled = true;
          this.$emit("reloadRequests");
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
.cnl-btn {
  color: dimgray;
  background: white;
  border: 1px solid #ed7966;
}
.cnl-btn:hover {
  background: #ed7966;
  color: white;
}
i {
  color: #ed7966;
}
.card-link:hover {
  text-shadow: 1.5px 1.5px 0 black;
}
.card-footer {
  border-top: none;
}
</style>
