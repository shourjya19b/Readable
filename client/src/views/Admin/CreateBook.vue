<script setup>
import InputError from "@/components/InputError.vue";
import SuccessAlert from "@/components/SuccessAlert.vue";
import ErrorAlert from "@/components/ErrorAlert.vue";
import store from "@/store";
import router from "@/router";
</script>
<script>
export default {
  name: "AdminCreateBook",
  data() {
    return {
      name: null,
      author: null,
      desc: null,
      section: null,
      img_file: null,
      img_url: null,
      error: {
        name: null,
        author: null,
        section: null,
      },
      success: false,
      failure: false,
    };
  },
  created() {
    this.section = this.$route.query["section"];
  },
  methods: {
    getImage(event) {
      this.img_file = event.target.files[0];
      this.readImageURL();
    },
    readImageURL() {
      const reader = new FileReader();
      reader.readAsDataURL(this.img_file);
      reader.addEventListener("load", (event) => {
        this.img_url = event.target.result;
      });
    },
    validate() {
      let invalid = false;
      this.error = {
        name: null,
        author: null,
        section: null,
      };
      if (!this.name) {
        invalid = true;
        this.error["name"] = "Name required";
      }
      if (!this.author) {
        invalid = true;
        this.error["author"] = "Author required";
      }
      return invalid;
    },
    createBook(event) {
      event.preventDefault();
      if (!this.validate()) {
        let form = new FormData();
        form.append("name", this.name);
        form.append("author", this.author);
        form.append("desc", this.desc);
        form.append("section", this.section);
        form.append("image", this.img_file);

        fetch(store.getters.BASEURL + "/book/create", {
          method: "POST",
          headers: {
            "Authentication-Token": store.getters.getToken,
          },
          body: form,
        })
          .then((response) => {
            return response.json();
          })
          .then((data) => {
            if (Object.keys(data).includes("error")) {
              this.failure = true;
              let backend_error = data["error"];
              if (backend_error == "invalid_title") {
                this.error["name"] = "Invalid title";
              } else if (backend_error == "invalid_author") {
                this.error["author"] = "Invalid author";
              } else if (backend_error == "invalid_section") {
                this.error["section"] = "Invalid section";
              }
            } else {
              this.success = true;
              this.error = { name: null, author: null, section: null };
              setTimeout(() => {
                router.push("/admin/section/" + this.section + "/view");
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
    message="Created book successfully"
  ></SuccessAlert>
  <ErrorAlert
    v-show="failure"
    message="Failed to create book"
    @dismiss="dismissAlert"
  ></ErrorAlert>
  <div class="container mt-5 p-5">
    <div class="row justify-content-center py-1">
      <div class="col-md-6 rounded border shadow bg-white p-4">
        <h1 class="h4 text-center text-secondary mb-4">Book Details</h1>
        <form @submit="createBook" enctype="multipart/form-data">
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
          <div class="mb-3 px-3">
            <label for="Input2" class="form-label">Author</label>
            <input
              type="text"
              class="form-control"
              name="title"
              id="Input2"
              v-model="author"
            />
            <InputError :message="error['author']" />
          </div>
          <div class="mb-3 px-3">
            <label for="Input3" class="form-label">Section</label>
            <input
              type="text"
              class="form-control"
              name="title"
              id="Input3"
              v-model="section"
              disabled
            />
          </div>
          <div class="mb-4 px-3">
            <label for="Input4" class="form-label">Description</label>
            <textarea
              class="form-control"
              rows="2"
              id="Input4"
              name="content"
              v-model="desc"
            ></textarea>
          </div>
          <div class="mb-4 px-3">
            <label for="formFile" class="form-label">Image</label>
            <input
              class="form-control"
              type="file"
              id="formFile"
              name="image"
              @change="getImage"
            />
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
