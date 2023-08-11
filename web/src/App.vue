<template>
  <Navbar />

  <router-view />
  <notifications position="bottom right" :pauseOnHover="true" />
  <Footer />
</template>

<script >
  import { RouterView } from 'vue-router';
  import Navbar from '@/components/Navbar.vue';
  import Footer from '@/components/Footer.vue';

  export default {
  components: {
    Navbar,
    Footer,
  },
  created() {
    this.$store.dispatch("fetchColors");
    this.$store.dispatch("fetchSettings");
  },
}
</script>

<style>
</style>
