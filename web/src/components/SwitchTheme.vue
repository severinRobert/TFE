<template>
  <div class="switch-theme">
    <input type="checkbox" @click="toggleTheme" :checked="theme=='dark-theme'"/>
    <label>{{ $t("main.darkTheme") }}</label>
  </div>
</template>

<script>
export default {
    name: "SwitchTheme",
    created() {
      if(!localStorage.getItem("theme")) {
        localStorage.setItem("theme", "light-theme");
      }
      document.documentElement.className = localStorage.getItem("theme");
    },
    data() {
      return {
        theme: localStorage.getItem("theme"),
      };
    },
    methods: {
      toggleTheme() {
        let theme = localStorage.getItem("theme") === "light-theme" ? "dark-theme" : "light-theme";
        localStorage.setItem("theme", theme)
        document.documentElement.className = theme;
      },
    },
    
};
</script>

<style>
.switch-theme {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 1rem;
}
</style>
