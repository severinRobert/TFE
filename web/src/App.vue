<script >
  import { RouterView } from 'vue-router';
  import LocaleChanger from "@/components/LocaleChanger.vue";

  export default {
  components: {
    LocaleChanger
  }
}
</script>

<template>
  <header>
    <router-link to="/">{{ $t("main.home") }}</router-link>
    <router-link to="/productList">{{ $t("main.productList") }}</router-link>
    <router-link to="/form">{{ $t("main.form") }}</router-link>
    <router-link to="/profile">{{ $t("main.profile") }}</router-link>
    <router-link to="/dashboard">{{ $t("main.dashboard") }}</router-link>
    <LocaleChanger />
  </header>

  <router-view />

  <footer>
    <p>Footer</p>
  </footer>
</template>

<style>

</style>
