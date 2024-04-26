<script setup>
import { RouterLink } from "vue-router";
</script>
<template>
  <div class="card bg-white shadow" style="height: 12rem">
    <div class="card-body">
      <RouterLink
        class="card-title fw-semibold fs-4 d-block px-3 card-link"
        :to="{ name: 'section_view', params: { section_name: section.name } }"
      >
        {{ section.name }}
      </RouterLink>
      <p class="card-text text-truncate px-3 text-secondary mb-3">
        {{ section.desc }}
      </p>
    </div>
    <div class="card-footer bg-transparent text-center py-2">
      <RouterLink
        class="btn rounded-pill card-link fw-semibold"
        :to="{
          name: 'section_edit',
          params: { section_id: section.id },
          query: { name: section.name, desc: section.desc },
        }"
        >Edit Section</RouterLink
      >
    </div>
  </div>
</template>
<script>
export default {
  name: "SectionCardAdmin",
  props: { section: Object },
  data() {
    return {};
  },
};
</script>
<style scoped>
.card-header {
  text-decoration: none;
  color: dimgray;
  border-bottom: none;
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
.card-link {
  text-decoration: none;
}
.card-link:hover {
  text-shadow: 0.25px 0.25px 0 black;
}
.card-footer {
  border-top: none;
}
</style>
