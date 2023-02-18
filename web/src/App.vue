<script >
  import { RouterView } from 'vue-router'
</script>

<template>
  <header>
    <router-link to="/">Home</router-link>
    <router-link to="/productList">Product List</router-link>
    <router-link to="/form">Form</router-link>
    <router-link to="/profile">Profile</router-link>
    <router-link to="/dashboard">Dashboard</router-link>
  </header>

  <router-view />

  <footer>
    <p>Footer</p>
  </footer>
</template>

<style>

</style>
