<script setup>
import store from "@/store";
import router from "@/router";
import InputError from "@/components/InputError.vue";
import SuccessAlert from "@/components/SuccessAlert.vue";
import ErrorAlert from "@/components/ErrorAlert.vue";
</script>
<template>
  <SuccessAlert
    v-show="success"
    message="Reviewed book successfully"
    @dismiss="dismissAlert"
  ></SuccessAlert>
  <ErrorAlert
    v-show="failure"
    message="Failed to review book"
    @dismiss="dismissAlert"
  ></ErrorAlert>
  <div class="container mt-3 p-5">
    <div class="row justify-content-center py-1">
      <div class="col-md-6 rounded border shadow bg-white p-4">
        <h1 class="h4 text-center text-secondary mb-4">Review Book</h1>
        <form @submit="reviewBook">
          <div class="mb-3 px-3">
            <label for="InputName" class="form-label">Name</label>
            <input
              type="text"
              class="form-control"
              name="title"
              id="InputName"
              v-model="name"
              disabled
            />
          </div>
          <div class="mb-3 px-3">
            <label for="InputSection" class="form-label">Section</label>
            <input
              type="text"
              class="form-control"
              name="title"
              id="InputSection"
              v-model="section"
              disabled
            />
          </div>
          <div class="mb-3 px-3">
            <label for="InputRating" class="form-label">Rating</label>
            <select class="form-select" v-model="rating" id="InputRating">
              <option selected disabled>Rating</option>
              <option v-for="i in 5">{{ i }}</option>
            </select>
            <InputError :message="error['rating']" />
          </div>
          <div class="mb-3 px-3">
            <label for="InputReview" class="form-label">Review</label>
            <textarea
              class="form-control"
              rows="3"
              id="InputReview"
              name="content"
              v-model="review"
            ></textarea>
            <InputError :message="error['review']" />
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
              Submit
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "UserReviewBook",
  props: ["book_id"],
  data() {
    return {
      name: null,
      section: null,
      review: null,
      rating: null,
      success: false,
      failure: false,
      error: {
        rating: null,
        review: null,
      },
    };
  },
  created() {
    this.name = this.$route.query["name"];
    this.section = this.$route.query["section"];
  },
  methods: {
    validate() {
      let invalid = false;
      this.error = {
        rating: null,
        review: null,
      };
      if (!this.rating) {
        invalid = true;
        this.error["rating"] = "Rating Required";
      }
      if (!this.review) {
        invalid = true;
        this.error["review"] = "Review Required";
      }
      return invalid;
    },
    reviewBook(event) {
      event.preventDefault();
      if (!this.validate()) {
        let form = new FormData();

        form.append("rating", this.rating);
        form.append("review", this.review);

        fetch(store.getters.BASEURL + "/book/" + this.book_id + "/review", {
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
              if (backend_error == "invalid_rating") {
                this.error["rating"] = "Invalid rating";
              } else if (backend_error == "invalid_review") {
                this.error["review"] = "Invalid review";
              }
            } else {
              this.success = true;
              this.error = {
                rating: null,
                review: null,
              };
              setTimeout(() => {
                router.push("/user/issues/view");
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
