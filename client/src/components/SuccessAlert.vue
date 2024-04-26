<template>
  <div class="alert alert-success alert-dismissible fade show" role="alert">
    {{ message }}
    <button
      type="button"
      @click="$emit('dismiss')"
      class="btn-close"
      data-bs-dismiss="alert"
    ></button>
  </div>
</template>
<script>
export default {
  name: "SuccessAlert",
  props: ["message"],
};
</script>
