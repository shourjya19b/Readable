<script setup>
import BookCardAdmin from "@/components/BookCardAdmin.vue";
import store from "@/store";
import { RouterLink } from "vue-router";
</script>
<template>
  <div class="container mt-2 py-3">
    <div class="row py-3 g-4 my-3">
      <div class="col-8 p-4 shadow-sm bg-white rounded-3">
        <form class="row" role="search" @submit="searchBooks">
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
            <select class="form-select" id="inputSection">
              <option selected disabled>Section</option>
              <option :value="section_name">
                {{ section_name }}
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
        <BookCardAdmin :book="book" />
      </div>
    </div>
    <div class="row mt-3">
      <div class="text-center">
        <RouterLink
          class="btn add-btn rounded-pill fw-semibold text-dark shadow-sm"
          :to="{ name: 'book_create', query: { section: section_name } }"
          >Add Book</RouterLink
        >
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "AdminViewSection",
  props: ["section_name"],
  data() {
    return {
      search: null,
      rating: null,
      author: null,
      error: {
        search: null,
        rating: null,
        author: null,
      },
    };
  },
  created() {
    store.dispatch("getBooks", {
      search: this.search,
      rating: this.rating,
      author: this.author,
      section: this.section_name,
    });
  },
  methods: {
    searchBooks(event) {
      event.preventDefault();
      store.dispatch("getBooks", {
        search: this.search,
        rating: this.rating,
        author: this.author,
        section: this.section_name,
      });
    },
  },
  computed: {
    books() {
      return store.getters.getBooks;
    },
  },
};
</script>

<style scoped>
.srch-btn {
  background: hsl(203, 55%, 38%);
  color: white;
}
.srch-btn:hover {
  text-shadow: 1.5px 1.5px 0 black;
}
.add-btn {
  background: white;
  color: dimgray;
  border: 1px solid #ed7966;
}
.add-btn:hover {
  text-shadow: 0.25px 0.25px 0 black;
}
</style>
