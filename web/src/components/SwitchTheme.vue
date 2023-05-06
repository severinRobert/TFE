<template>
  <div class="switch-theme">
    <input type="checkbox" @click="toggleTheme"/>
    <label>Toggle theme</label>
  </div>
</template>

<script>
export default {
    name: "SwitchTheme",
    data() {
        return {
            theme: "light-theme",
        };
    },
    methods: {
        toggleTheme() {
          this.theme = this.theme === "light-theme" ? "dark-theme" : "light-theme";
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
