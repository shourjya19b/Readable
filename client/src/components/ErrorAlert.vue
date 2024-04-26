<template>
  <div class="alert alert-danger alert-dismissible fade show" role="alert">
    {{ message }}
    <button
      type="button"
      class="btn-close"
      @click="$emit('dismiss')"
      data-bs-dismiss="alert"
    ></button>
  </div>
</template>
<script>
export default {
  name: "ErrorAlert",
  props: ["message"],
};
</script>
