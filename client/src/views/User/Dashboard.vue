<script setup>
import BookCardUser from "@/components/BookCardUser.vue";
import store from "@/store";
</script>
<template>
  <div class="container mt-2 py-3">
    <div class="row py-3 g-4 my-3">
      <div class="col-8 p-4 bg-white rounded-3 shadow-sm">
        <form @submit="searchBooks" class="row" role="search">
          <div class="col-6 mb-4">
            <label for="inputName" class="form-label">Title</label>
            <input
              class="form-control"
              type="search"
              v-model="search"
              id="inputName"
            />
          </div>
          <div class="col-6 mb-4">
            <label for="inputAuthor" class="form-label">Author</label>
            <input
              class="form-control"
              type="search"
              v-model="author"
              id="inputAuthor"
            />
          </div>
          <div class="col-6">
            <label for="inputSection" class="form-label">Section</label>
            <select class="form-select" v-model="section" id="inputSection">
              <option selected disabled>Section</option>
              <option v-for="section in sections" :value="section.name">
                {{ section.name }}
              </option>
            </select>
          </div>
          <div class="col-4">
            <label for="inputRating" class="form-label">Rating</label>
            <select class="form-select" v-model="rating" id="inputRating">
              <option selected disabled>Rating</option>
              <option v-for="i in 5">{{ i }}</option>
            </select>
          </div>
          <div class="col-2 py-1">
            <button
              class="btn srch-btn shadow-sm rounded-pill fw-semibold mt-4"
              type="submit"
              style="
                --bs-btn-padding-y: 0.5rem;
                --bs-btn-padding-x: 1.25rem;
                --bs-btn-font-size: 1rem;
              "
            >
              Search
            </button>
          </div>
        </form>
      </div>
    </div>
    <div class="row py-3 g-4">
      <div class="col-3" v-for="book in books">
        <BookCardUser :book="book" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "UserDashboard",
  data() {
    return {
      search: null,
      rating: null,
      author: null,
      section: null,
    };
  },
  created() {
    store.dispatch("getBooks", {
      search: this.search,
      rating: this.rating,
      author: this.author,
      section: this.section,
    });
    store.dispatch("getSections", { search: null });
  },
  methods: {
    searchBooks(event) {
      event.preventDefault();
      store.dispatch("getBooks", {
        search: this.search,
        rating: this.rating,
        author: this.author,
        section: this.section,
      });
    },
  },
  computed: {
    books() {
      return store.getters.getBooks;
    },
    sections() {
      return store.getters.getSections;
    },
  },
  components: { BookCardUser },
};
</script>

<style scoped>
.btn {
  background: hsl(203, 55%, 38%);
  color: white;
}
.btn:hover {
  text-shadow: 1.5px 1.5px 0 black;
}
</style>
