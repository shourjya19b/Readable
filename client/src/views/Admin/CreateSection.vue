<script setup>
import InputError from "@/components/InputError.vue";
import SuccessAlert from "@/components/SuccessAlert.vue";
import ErrorAlert from "@/components/ErrorAlert.vue";
import router from "@/router";
import store from "@/store";
</script>
<script>
export default {
  name: "AdminCreateSection",
  data() {
    return {
      name: null,
      desc: null,
      error: {
        name: null,
        desc: null,
      },
      success: false,
      failure: false,
    };
  },
  methods: {
    validate() {
      let invalid = false;
      this.error = {
        name: null,
        desc: null,
      };
      if (!this.name) {
        invalid = true;
        this.error["name"] = "Invalid title";
      }
      if (!this.desc) {
        invalid = true;
        this.error["desc"] = "Required field";
      }
      return invalid;
    },
    createSection(event) {
      event.preventDefault();
      if (!this.validate()) {
        fetch(store.getters.BASEURL + "/section/create", {
          method: "POST",
          headers: {
            "Authentication-Token": store.getters.getToken,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name: this.name,
            desc: this.desc,
          }),
        })
          .then((response) => {
            return response.json();
          })
          .then((data) => {
            if (Object.keys(data).includes("error")) {
              this.failure = true;
              let backend_error = data["error"];
              if (backend_error == "invalid_name") {
                this.error["name"] = "Invalid name";
              }
            } else {
              this.success = true;
              this.error = { name: null, desc: null };
              setTimeout(() => {
                router.push("/admin/board");
              }, 1000);
            }
          });
      }
    },
    dismissAlert() {
      this.success = false;
      this.failure = false;
    },
  },
};
</script>
<template>
  <SuccessAlert
    v-show="success"
    @dismiss="dismissAlert"
    message="Created section successfully"
  ></SuccessAlert>
  <ErrorAlert
    v-show="failure"
    message="Failed to create section"
    @dismiss="dismissAlert"
  ></ErrorAlert>
  <div class="container mt-5 p-5">
    <div class="row justify-content-center py-1">
      <div class="col-md-6 rounded border shadow bg-white p-4">
        <h1 class="h4 text-center text-secondary mb-4">Section Details</h1>
        <form @submit="createSection">
          <div class="mb-3 px-3">
            <label for="Input1" class="form-label">Name</label>
            <input
              type="text"
              class="form-control"
              name="title"
              id="Input1"
              v-model="name"
            />
            <InputError :message="error['name']" />
          </div>
          <div class="mb-4 px-3">
            <label for="Input2" class="form-label">Description</label>
            <textarea
              class="form-control"
              rows="3"
              id="Input2"
              name="content"
              v-model="desc"
            ></textarea>
            <InputError :message="error['desc']" />
          </div>
          <div class="mb-2 text-center px-3">
            <button
              type="submit"
              class="btn btn-lg shadow-sm rounded-pill fw-semibold"
              style="
                --bs-btn-padding-y: 0.35rem;
                --bs-btn-padding-x: 1.25rem;
                --bs-btn-font-size: 1.15rem;
              "
            >
              Create
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
<style scoped>
.btn {
  color: dimgray;
  border: 1px solid hsl(203, 55%, 38%);
}
.btn:hover {
  text-shadow: 0.25px 0.25px 0 black;
  background: hsl(203, 55%, 38%);
  color: white;
}
</style>
