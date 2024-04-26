<template>
  <div
    class="my-2"
    :style="{ display: message ? 'block' : 'none' }"
    style="color: red"
  >
    {{ message }}
  </div>
</template>

<script>
export default {
  props: ["message"],
};
</script>
