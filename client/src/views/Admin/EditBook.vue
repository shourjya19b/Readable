<script setup>
import store from "@/store";
import router from "@/router";
import SuccessAlert from "@/components/SuccessAlert.vue";
import ErrorAlert from "@/components/ErrorAlert.vue";
</script>
<template>
  <SuccessAlert
    v-show="edit_success"
    message="Updated book successfully"
    @dismiss="dismissAlert"
  ></SuccessAlert>
  <SuccessAlert
    v-show="delete_success"
    message="Deleted book successfully"
    @dismiss="dismissAlert"
  ></SuccessAlert>
  <ErrorAlert
    v-show="edit_failure"
    message="Failed to update book"
    @dismiss="dismissAlert"
  ></ErrorAlert>
  <ErrorAlert
    v-show="delete_failure"
    message="Failed to delete book"
    @dismiss="dismissAlert"
  ></ErrorAlert>
  <div class="container mt-5 p-5">
    <div class="row justify-content-center py-1">
      <div class="col-md-6 rounded border shadow bg-white p-4">
        <h1 class="h4 text-center text-secondary mb-4">Book Details</h1>
        <form @submit="updateBook">
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
            <label for="Input3" class="form-label">Description</label>
            <textarea
              class="form-control"
              rows="2"
              id="Input3"
              name="content"
              v-model="desc"
            ></textarea>
          </div>
          <div class="mb-3 px-3">
            <label for="Input4" class="form-label">Section</label>
            <input
              type="text"
              class="form-control"
              name="title"
              id="Input4"
              v-model="section"
              disabled
            />
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
              @click="deleteBook(book_id)"
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
  name: "AdminEditBook",
  props: ["book_id"],
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
      edit_success: false,
      delete_success: false,
      edit_failure: false,
      delete_failure: false,
    };
  },
  created() {
    this.name = this.$route.query["name"];
    this.author = this.$route.query["author"];
    this.desc = this.$route.query["desc"];
    this.img_url = this.getImageURL();
    this.section = this.$route.query["section"];
  },
  methods: {
    getImageURL() {
      if (this.$route.query["image"])
        return (
          store.getters.BASEURL +
          "/static/uploads/" +
          this.$route.query["image"]
        );
      else return null;
    },
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
        this.error["name"] = "Title Required";
      }
      if (!this.author) {
        invalid = true;
        this.error["author"] = "Author Required";
      }
      if (!this.section) {
        invalid = true;
        this.error["section"] = "Section Required";
      }
      return invalid;
    },
    updateBook(event) {
      event.preventDefault();
      if (!this.validate()) {
        let form = new FormData();
        form.append("name", this.name);
        form.append("author", this.author);
        form.append("desc", this.desc);
        form.append("section", this.section);
        form.append("image", this.img_file);

        fetch(store.getters.BASEURL + "/book/" + this.book_id + "/edit", {
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
              this.edit_failure = true;
              let backend_error = data["error"];
              if (backend_error == "invalid_title") {
                this.error["name"] = "Invalid title";
              } else if (backend_error == "invalid_author") {
                this.error["author"] = "Invalid author";
              } else if (backend_error == "invalid_section") {
                this.error["section"] = "Invalid section";
              }
            } else {
              this.edit_success = true;
              this.error = { name: null, author: null, section: null };
              setTimeout(() => {
                router.push("/admin/section/" + this.section + "/view");
              }, 1000);
            }
          });
      }
    },
    deleteBook(book_id) {
      fetch(store.getters.BASEURL + "/book/" + book_id + "/delete", {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": store.getters.getToken,
        },
      }).then((response) => {
        if (response.status == 200) {
          this.delete_success = true;
          setTimeout(() => {
            router.push("/admin/section/" + this.section + "/view");
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
