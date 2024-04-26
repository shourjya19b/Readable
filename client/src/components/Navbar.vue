<script setup>
import { RouterLink } from "vue-router";
import ErrorAlert from "@/components/ErrorAlert.vue";
import store from "@/store";
</script>
<template>
  <nav class="navbar navbar-expand-lg bg-transparent">
    <div class="container">
      <div>
        <RouterLink
          class="navbar-brand fs-2 mb-4 fw-semibold fst-italic"
          to="#"
        >
          Read
        </RouterLink>
      </div>
      <div>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item px-1" v-for="link in links">
              <RouterLink class="nav-link fw-bold" :to="link.path">{{
                link.name
              }}</RouterLink>
            </li>
            <li class="nav-item px-1" v-if="admin">
              <RouterLink class="nav-link fw-bold" to="/admin/login"
                >Log out</RouterLink
              >
            </li>
            <li class="nav-item px-1" v-else>
              <RouterLink class="nav-link fw-bold" to="/user/login"
                >Log out</RouterLink
              >
            </li>
          </ul>
        </div>
      </div>
    </div>
  </nav>
  <ErrorAlert :message="error['export']" v-if="export_error" />
  <span v-else></span>
</template>

<script>
export default {
  name: "Navbar",
  props: { links: Array, admin: Boolean },
  data() {
    return {
      task_id: null,
      export_error: false,
      error: {
        export: null,
      },
    };
  },
  methods: {
    exportCSV() {
      fetch(store.getters.BASEURL + "/admin/export", {
        method: "GET",
        headers: {
          "Authentication-Token": store.getters.getToken,
        },
      })
        .then((response) => {
          if (response.status == 200) return response.json();
          return {};
        })
        .then((data) => {
          if (Object.keys(data).includes("id")) {
            this.task_id = data["id"];
          }
        });
      this.getStatus();
    },
    getStatus() {
      fetch(store.getters.BASEURL + "/admin/export?task=" + this.task_id, {
        method: "GET",
        headers: {
          "Authentication-Token": store.getters.getToken,
        },
      })
        .then((response) => {
          if (response.status == 200) {
            return response.json();
          } else {
            this.error["export"] = "Export job failed";
            this.export_error = true;
            return {};
          }
        })
        .then((data) => {
          if (Object.keys(data).includes("status")) {
            if (data["status"] == "SUCCESS") {
              open(
                store.getters.BASEURL + "/admin/download?task=" + this.task_id
              );
            } else {
              setTimeout(this.getStatus(), 1000);
            }
          }
        });
    },
    dismiss_error() {
      this.export_error = false;
    },
  },
  components: { ErrorAlert },
};
</script>

<style scoped>
.nav-link:hover {
  border-bottom: 2px solid dimgray;
  text-shadow: 0.25px 0.25px 0 black;
  color: hsl(203, 55%, 38%);
}
.navbar-brand {
  font-family: Sacramento;
  color: #ed7966;
}
.btn {
  background: hsl(203, 55%, 38%);
  color: white;
}
.btn:hover {
  text-shadow: 1.5px 1.5px 0 black;
}
.srch-btn {
  color: #ed7966;
  background: transparent;
}
</style>
