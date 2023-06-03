<script >
  import { RouterView } from 'vue-router';
  import LocaleChanger from "@/components/LocaleChanger.vue";
  import Authentification from "@/components/Authentification.vue";
  import SwitchTheme from '@/components/SwitchTheme.vue';

  export default {
  components: {
    LocaleChanger,
    Authentification,
    SwitchTheme
  }
}
</script>

<template>
  <nav>
    <router-link to="/">{{ $t("main.home") }}</router-link>
    <router-link to="/offerList">{{ $t("main.offerList") }}</router-link>
    <router-link to="/form">{{ $t("main.form") }}</router-link>
    <router-link to="/profile">{{ $t("main.profile") }}</router-link>
    <router-link to="/dashboard">{{ $t("main.dashboard") }}</router-link>
    <LocaleChanger />
    <Authentification />
    <SwitchTheme />
  </nav>

  <router-view />
  <notifications position="bottom right" pauseOnHover="true" />
  <footer>
    <p>Footer</p>
  </footer>
</template>

<style>

nav {
  display: flex;
  flex-direction: row;
  justify-content: center;

  background: var(--secondaryColor)
}

nav a {
  color: var(--textSecondaryColor);
  text-decoration: none;
  margin:1rem;
}

.router-link-active {
  text-decoration: underline;
}

</style>
