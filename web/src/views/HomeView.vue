<script>

export default {
  name: "HomeView",
  methods: {
    test() {
      console.log("test")
      console.log(this.$store)
    },
  },
};
</script>

<template>
    <section class="content">
        <h1> Home </h1>
        <button @click="test">Test</button>
    </section>
</template>

<style>
</style>
