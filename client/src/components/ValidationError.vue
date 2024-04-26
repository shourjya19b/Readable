<template>
  <div
    class="my-2"
    :style="{ display: invalid ? 'block' : 'none' }"
    style="color: red"
  >
    Invalid email or password
  </div>
</template>

<script>
export default {
  props: ["invalid"],
};
</script>
