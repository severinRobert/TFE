<template>
  <div v-if="isAuthentified" style="display: flex;">
    <button class="cancel" @click="showModal('logout')">{{ $t("auth.logout") }}</button>
  </div>
  <div v-else style="display: flex;">
    <button @click="showModal('login')">{{ $t("auth.login") }}</button>
    <button @click="showModal('register')">{{ $t("auth.register") }}</button>
  </div>
  <dialog id="dialog-logout">
    <h1>{{ $t("auth.logout") }}</h1>
    <p>{{ $t("auth.logoutMessage") }}</p>
    <button @click="logout">{{ $t("auth.logout") }}</button>
    <button class="cancel" @click="cancel">{{ $t("main.cancel") }}</button>
  </dialog>
  <dialog id="dialog-login">
    <form action="#" @submit="login">
      <h1>{{ $t("auth.login") }}</h1>
      <p>{{ $t("auth.loginMessage") }}</p>
      <label for="username">{{ $t("auth.username") }}</label>
      <input type="text" id="username" name="username" /><br/>
      <label for="password">{{ $t("auth.password") }}</label>
      <input type="password" id="password" name="password" /><br/>
      <button type="submit">{{ $t("auth.login") }}</button>
    </form>
    <button class="cancel" @click="cancel">{{ $t("main.cancel") }}</button>
  </dialog>
  <dialog id="dialog-register">
    <form action="#" @submit="register">
    <h1>{{ $t("auth.register") }}</h1>
      <p>{{ $t("auth.registerMessage") }}</p>
      <label for="username">{{ $t("auth.username") }}</label>
      <input type="text" id="username" name="username" /><br/>
      <label for="email">{{ $t("auth.email") }}</label>
      <input type="text" id="email" name="email" /><br/>
      <label for="password">{{ $t("auth.password") }}</label>
      <input type="password" id="password" name="password" /><br/>
      <button type="submit">{{ $t("auth.register") }}</button>
    </form>
    <button @click="cancel">{{ $t("main.cancel") }}</button>
  </dialog>
</template>

<script>
import { authentificationHeaders, headers } from "@/api";

export default {
  name: "Authentification",
  data() {
    return {
      authentification: true,
      isAuthentified: localStorage.getItem('token') !== null && localStorage.getItem('token') !== 'undefined',
    };
  },
  methods: {
    showModal(type) {
      const dialog = document.getElementById("dialog-"+type);
      dialog.showModal();
      dialog.addEventListener("click", e => {
        const dialogDimensions = dialog.getBoundingClientRect();
        if (
          e.clientX < dialogDimensions.left ||
          e.clientX > dialogDimensions.right ||
          e.clientY < dialogDimensions.top ||
          e.clientY > dialogDimensions.bottom
        ) {
          dialog.close();
        }
      })
    },
    logout(e) {
      this.currentUser.logout();
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      this.$router.push("/");
      this.cancel(e);
      this.isAuthentified = false;
    },
    set_login(e, username, access_token) {
      this.currentUser.login(username, access_token);
      headers().get("/users/me").then((response) => {
        console.log(response.data)
        let user_id = Number(response.data);
        localStorage.setItem('user_id', user_id);
      });
      this.cancel(e);
      this.isAuthentified = true;
    },
    login(e) {
      e.preventDefault(); // prevent the form from submitting 
      console.log(e)
      console.log(e.target.username.value, e.target.password.value)
      const form = e.target;
      authentificationHeaders().post("/users/login", {
        username: form.username.value,
        password: form.password.value,
      }).then((response) => {
        this.set_login(e, form.username.value, response.data.access_token);
      }).catch((error) => {
          this.error = error;
          this.$notify({
              type: 'error',
              text: this.$t('auth.loginFailed')
          })
      });
    },
    register(e) {
      e.preventDefault(); // prevent the form from submitting 
      const form = e.target;
      headers().post("/users/register", {
        username: form.username.value,
        email: form.email.value,
        password: form.password.value,
      }).then((response) => {
        console.log(response.data)
        this.set_login(e, form.username.value, response.data.access_token);
      }).catch((error) => {
          this.error = error;
          this.$notify({
              type: 'error',
              text: error
          })
      });
    },
    cancel(e) {
      const dialog = e.target.closest("dialog");
      dialog.close();
    },
  },
};
</script>

<style></style>
