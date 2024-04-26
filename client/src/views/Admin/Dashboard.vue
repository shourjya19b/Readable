<script setup>
import SectionCardAdmin from "@/components/SectionCardAdmin.vue";
import store from "@/store";
import { RouterLink } from "vue-router";
</script>
<script>
export default {
  name: "AdminDashboard",
  data() {
    return {
      search: null,
    };
  },
  created() {
    store.dispatch("getSections", {
      search: null,
    });
  },
  methods: {
    searchSections(event) {
      event.preventDefault();
      store.dispatch("getSections", {
        search: this.search,
      });
    },
  },
  computed: {
    sections() {
      return store.getters.getSections;
    },
  },
  components: { SectionCardAdmin },
};
</script>

<template>
  <div class="container mt-5 py-3">
    <div class="row py-3 g-4 my-3">
      <div class="col-6">
        <form
          class="d-flex bg-transparent"
          role="search"
          @submit="searchSections"
        >
          <input
            class="form-control"
            type="search"
            placeholder="Search Sections"
            v-model="search"
          />
          <button class="btn srch-btn" type="submit">
            <i class="fa-solid fa-search fa-xl"></i>
          </button>
        </form>
      </div>
    </div>
    <div class="row py-3 g-4">
      <div class="col-3" v-for="section in sections">
        <SectionCardAdmin :section="section" />
      </div>
    </div>
    <div class="row mt-3">
      <div class="text-center">
        <RouterLink
          class="btn add-btn rounded-pill fw-semibold text-dark shadow-sm"
          to="/admin/section/create"
          >Add Section
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
.srch-btn {
  color: #ed7966;
  background: transparent;
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
