<script setup>
import { RouterLink } from "vue-router";
import store from "@/store";
</script>
<template>
  <div class="card bg-white shadow" style="height: 30rem">
    <img
      :src="imageURL(book.image)"
      class="card-img-top"
      style="max-width: 100%; height: 15rem"
    />
    <div class="card-body">
      <RouterLink
        class="card-title fw-semibold fs-5 d-block px-3 card-link text-dark"
        to="#"
      >
        {{ book.name }}
      </RouterLink>
      <div class="mb-3 px-3 card-subtitle fw-semibold text-secondary">
        {{ book.author }}
      </div>
      <p class="card-text text-truncate px-3 text-secondary mb-3">
        {{ book.desc }}
      </p>
      <div class="bg-transparent px-3 rounded">
        <div class="fw-semibold text-dark">
          <i class="fa-solid fa-star me-1"></i>{{ book.rating }}/5
        </div>
      </div>
    </div>
    <div class="card-footer bg-transparent text-center">
      <RouterLink
        class="btn rounded-pill card-link fw-semibold px-4 shadow-sm"
        :to="{
          name: 'book_edit',
          params: { book_id: book.id },
          query: {
            name: book.name,
            author: book.author,
            section: book.section,
            desc: book.desc,
            rating: book.rating,
            image: book.image,
          },
        }"
        >Edit</RouterLink
      >
    </div>
  </div>
</template>
<script>
export default {
  name: "BookCardAdmin",
  props: { book: Object },
  methods: {
    imageURL(image) {
      return `${store.getters.BASEURL}/static/uploads/${image}`;
    },
  },
};
</script>
<style scoped>
.card-title {
  text-decoration: none;
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
