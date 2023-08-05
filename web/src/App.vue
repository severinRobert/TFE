<template>
  <nav>
    <section id="nav-links">
      <router-link to="/">{{ $t("main.home") }}</router-link>
      <router-link to="/offerList">{{ $t("main.offerList") }}</router-link>
      <router-link to="/form" v-if="['Administrator','User'].includes($store.state.role)">{{ $t("main.addOffer") }}</router-link>
      <router-link to="/profile" v-if="['Administrator','User'].includes($store.state.role)">{{ $t("main.profile") }}</router-link>
      <router-link to="/dashboard" v-if="$store.state.role==='Administrator'">{{ $t("main.dashboard") }}</router-link>
    </section>
    <section id="nav-options">
      <LocaleChanger />
      <SwitchTheme />
      <Authentication />
    </section>
  </nav>

  <router-view />
  <notifications position="bottom right" :pauseOnHover="true" />
  <footer>
    <p>Footer</p>
  </footer>
</template>

<script >
  import { RouterView } from 'vue-router';
  import LocaleChanger from "@/components/LocaleChanger.vue";
  import Authentication from "@/components/Authentication.vue";
  import SwitchTheme from '@/components/SwitchTheme.vue';

  export default {
  components: {
    LocaleChanger,
    Authentication,
    SwitchTheme
  },
  created() {
    this.$store.dispatch("fetchColors");
  },
}
</script>

<style>

nav {
  display: flex;
  flex-direction: row;

  background: var(--secondaryColor)
}

nav a {
  color: var(--textSecondaryColor);
  text-decoration: none;
  margin:1rem;
}

#nav-links {
  display: flex;
  flex-direction: row;
  flex-grow: 1;
  justify-content: center;
}

#nav-options {
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
}

.router-link-active {
  text-decoration: underline;
}

</style>
