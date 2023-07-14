<template>
  <div class="switch-theme">
    <input name="theme" type="checkbox" @click="toggleTheme" :checked="theme=='dark-theme'"/>
    <label for="theme">{{ $t("main.darkTheme") }}</label>
  </div>
</template>

<script>
export default {
    name: "SwitchTheme",
    created() {
      // if no theme is set, set it to the user's OS preference
      if(!localStorage.getItem("theme")) {
        const userDarkPreferencOS = window.matchMedia("(prefers-color-scheme: dark)").matches;
        this.theme = userDarkPreferencOS ? "dark-theme" : "light-theme"
        localStorage.setItem("theme", this.theme);
      }
      console.log("localStorage.getItem")
      document.documentElement.className = localStorage.getItem("theme");
    },
    data() {
      return {
        theme: localStorage.getItem("theme"),
      };
    },
    methods: {
      toggleTheme() {
        this.theme = localStorage.getItem("theme") === "light-theme" ? "dark-theme" : "light-theme";
        localStorage.setItem("theme", this.theme)
        document.documentElement.className = this.theme;
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
