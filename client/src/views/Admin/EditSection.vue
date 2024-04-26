<script setup>
import InputError from "@/components/InputError.vue";
import SuccessAlert from "@/components/SuccessAlert.vue";
import ErrorAlert from "@/components/ErrorAlert.vue";
import store from "@/store";
import router from "@/router";
</script>
<template>
  <SuccessAlert
    v-show="edit_success"
    message="Updated section successfully"
    @dismiss="dismissAlert"
  ></SuccessAlert>
  <SuccessAlert
    v-show="delete_success"
    message="Deleted section successfully"
    @dismiss="dismissAlert"
  ></SuccessAlert>
  <ErrorAlert
    v-show="edit_failure"
    message="Failed to update section"
    @dismiss="dismissAlert"
  ></ErrorAlert>
  <ErrorAlert
    v-show="delete_failure"
    message="Failed to delete section"
    @dismiss="dismissAlert"
  ></ErrorAlert>
  <div class="container mt-5 p-5">
    <div class="row justify-content-center py-1">
      <div class="col-md-6 rounded border shadow bg-white p-4">
        <h1 class="h4 text-center text-secondary mb-4">Section Details</h1>
        <form @submit="updateSection">
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
              rows="2"
              id="Input2"
              name="content"
              v-model="desc"
            ></textarea>
            <InputError :message="error['desc']" />
          </div>
          <div class="mb-2 text-center px-3">
            <button
              type="submit"
              class="btn btn-lg shadow-sm rounded-pill fw-semibold me-5"
              style="
                --bs-btn-padding-y: 0.35rem;
                --bs-btn-padding-x: 1rem;
                --bs-btn-font-size: 1.15rem;
              "
            >
              Update
            </button>
            <button
              @click="deleteSection(section_id)"
              class="btn btn-lg shadow-sm rounded-pill fw-semibold btn-del"
              style="
                --bs-btn-padding-y: 0.4rem;
                --bs-btn-padding-x: 1.4rem;
                --bs-btn-font-size: 1.15rem;
              "
            >
              Delete
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "AdminEditSection",
  props: ["section_id"],
  data() {
    return {
      name: null,
      desc: null,
      error: {
        name: null,
        desc: null,
      },
      edit_success: false,
      delete_success: false,
      edit_failure: false,
      delete_failure: false,
    };
  },
  created() {
    this.name = this.$route.query.name;
    this.desc = this.$route.query.desc;
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
        this.error["name"] = "Invalid name";
      }
      if (!this.desc) {
        invalid = true;
        this.error["desc"] = "Invalid description";
      }
      return invalid;
    },
    updateSection(event) {
      event.preventDefault();
      if (!this.validate()) {
        fetch(store.getters.BASEURL + "/section/" + this.section_id + "/edit", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": store.getters.getToken,
          },
          body: JSON.stringify({
            name: this.name,
            desc: this.desc,
          }),
        })
          .then((response) => {
            return response.json();
          })
          .then((response) => {
            if (Object.keys(response).includes("error")) {
              this.delete_failure = true;
              let backend_error = response["error"];
              if (backend_error == "invalid_name") {
                this.error["name"] = "Invalid name";
              } else {
                this.error["desc"] = "Invalid description";
              }
            } else if (Object.keys(response).includes("SUCCESS")) {
              this.edit_success = true;
              this.error = { name: null, desc: null };
              setTimeout(() => {
                router.push("/admin/board");
              }, 1000);
            }
          });
      }
    },
    deleteSection(section_id) {
      fetch(store.getters.BASEURL + "/section/" + section_id + "/delete", {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": store.getters.getToken,
        },
      }).then((response) => {
        if (response.status == 200) {
          this.delete_success = true;
          setTimeout(() => {
            router.push("/admin/board");
          }, 1000);
        } else {
          this.delete_failure = true;
        }
      });
    },
    dismissAlert() {
      this.edit_success = false;
      this.delete_success = false;
      this.edit_failure = false;
      this.delete_failure = false;
    },
  },
};
</script>

<style scoped>
.btn {
  color: dimgray;
  border: 1px solid hsl(203, 55%, 38%);
}
.btn-del {
  color: dimgray;
  border: 1px solid #ed7966;
}
.btn:hover {
  text-shadow: 0.25px 0.25px 0 black;
  background: hsl(203, 55%, 38%);
  color: white;
}
.btn-del:hover {
  text-shadow: 0.25px 0.25px 0 black;
  background: #ed7966;
  color: white;
}
</style>
