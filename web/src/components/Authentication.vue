<template>
  <div id="authentication">
    <template v-if="isAuthentified">
      <button class="cancel" @click="logout">{{ $t("auth.logout") }}</button>
      <span>{{ user }}</span>
    </template>
    <template v-else>
      <button @click="showModal('login')">{{ $t("auth.login") }}</button>
      <button @click="showModal('register')">{{ $t("auth.register") }}</button>
    </template>
  </div>
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
import { authenticationHeaders, headers } from "@/utils/api";

export default {
  name: "Authentication",
  data() {
    return {
      authentication: true,
      isAuthentified: localStorage.getItem('token') !== null && localStorage.getItem('token') !== 'undefined',
      user: localStorage.getItem('user'),
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
    logout() {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      localStorage.removeItem('password');
      this.$router.push("/");
      this.isAuthentified = false;
    },
    set_login(e, username, access_token, password) {
      localStorage.setItem('user', username);
      localStorage.setItem('password', password);
      localStorage.setItem('token', access_token);
      headers().get("/users/me").then((response) => {
        let user_id = Number(response.data);
        localStorage.setItem('user_id', user_id);
      });
      this.cancel(e);
      this.isAuthentified = true;
    },
    login(e) {
      e.preventDefault(); // prevent the form from submitting 
      const form = e.target;
      authenticationHeaders().post("/users/login", {
        username: form.username.value,
        password: form.password.value,
      }).then((response) => {
        this.set_login(e, form.username.value, response.data.access_token, form.password.value);
      }).catch((error) => {
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
        this.set_login(e, form.username.value, response.data.access_token, form.password.value);
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

<style>
#authentication {
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  align-items: center;
}
</style>
