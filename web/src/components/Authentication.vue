<template>
  <div id="authentication">
    <template v-if="isAuthentified">
      <button class="cancel" @click="logout">{{ $t("auth.logout") }}</button>
      <span>{{ user }}</span>
    </template>
    <template v-else>
      <button class="validation" @click="showModal('login')">{{ $t("auth.login") }}</button>
      <button class="validation" @click="showModal('register')">{{ $t("auth.register") }}</button>
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
      <button class="validation" type="submit">{{ $t("auth.login") }}</button>
    </form>
    <button class="cancel" @click="cancel">{{ $t("main.cancel") }}</button>
  </dialog>
  <dialog id="dialog-register">
    <form action="#" @submit="register">
    <h1>{{ $t("auth.register") }}</h1>
      <p>{{ $t("auth.registerMessage") }}</p>
      <label for="username">{{ $t("auth.username") }}*</label>
      <input type="text" id="username" name="username" required /><br/>
      <label for="email">{{ $t("auth.email") }}</label>
      <input type="text" id="email" name="email" /><br/>
      <label for="password">{{ $t("auth.password") }}*</label>
      <input type="password" id="password" name="password" required /><br/>
      <label for="passwordCheck">{{ $t("auth.passwordConfirm") }}*</label>
      <input type="password" id="passwordCheck" name="passwordCheck" required /><br/>
      <p id="gdprConsent">
        <input type="checkbox" name="gdprConsent" v-model="isGdprConsent"> {{ $t("auth.gdprConsent") }} 
        <router-link to="/gdpr" target="_blank">{{ $t("auth.here") }}</router-link>
      </p>
      <button class="validation" type="submit" :disabled="!isGdprConsent">{{ $t("auth.register") }}</button>
    </form>
    <button @click="cancel">{{ $t("main.cancel") }}</button>
    <p class="warning">{{ $t("main.starIsRequired") }}</p>
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
      isGdprConsent: false,
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
      localStorage.removeItem('role');
      this.$router.push("/");
      this.isAuthentified = false;
      this.user = "";
      this.$store.commit("setUsername", "");
      this.$store.commit("setRole", "");
    },
    set_login(e, username, access_token, password) {
      localStorage.setItem('user', username);
      this.$store.commit("setUsername", username);
      localStorage.setItem('password', password);
      localStorage.setItem('token', access_token);
      this.$store.commit("resetFavorites");
      headers().get("/users/me").then((response) => {
        let user_id = Number(response.data.id);
        localStorage.setItem('user_id', user_id);
        localStorage.setItem('role', response.data.role);
        this.$store.commit("setRole", response.data.role);
      });
      this.cancel(e);
      this.isAuthentified = true;
      this.user = username
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
      if(form.password.value !== form.passwordCheck.value) {
        this.$notify({
          type: 'error',
          text: this.$t("auth.passwordMismatch")
        })
        return;
      }
      headers().post("/users/register", {
        username: form.username.value,
        email: form.email.value,
        password: form.password.value,
      }).then((response) => {
        this.set_login(e, form.username.value, response.data.access_token, form.password.value);
      }).catch((error) => {
          this.$notify({
              type: 'error',
              text: `${error} "${error.response.data["detail"]}"`
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

#gdprConsent {
  margin-top: 1rem;
  font-size: small;
}
</style>
