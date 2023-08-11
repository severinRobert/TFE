<template>
  <nav>
    <section id="nav-content" class="animate__animated animate__faster">
      <section id="nav-links">
        <router-link class="navbar-title" to="/">{{ $t("main.home") }}</router-link>
        <router-link class="navbar-title" to="/offerList">{{ $t("main.offerList") }}</router-link>
        <router-link class="navbar-title" to="/form" v-if="['Administrator', 'User'].includes($store.state.role)">{{
          $t("main.addOffer") }}</router-link>
        <router-link class="navbar-title" to="/profile" v-if="['Administrator', 'User'].includes($store.state.role)">{{
          $t("main.profile") }}</router-link>
        <router-link class="navbar-title" to="/dashboard" v-if="$store.state.role === 'Administrator'">{{
          $t("main.dashboard") }}</router-link>
      </section>
      <section id="nav-options">
        <LocaleChanger />
        <SwitchTheme />
        <Authentication />
      </section>
    </section>
    <button id="burger" @click="toggleMenu()">v</button>
  </nav>
</template>

<script >
import LocaleChanger from "@/components/LocaleChanger.vue";
import Authentication from "@/components/Authentication.vue";
import SwitchTheme from '@/components/SwitchTheme.vue';

export default {
  components: {
    LocaleChanger,
    Authentication,
    SwitchTheme,
  },
  methods: {
    toggleMenu() {
      var nav = document.getElementById("nav-content");

      document.getElementById("nav-links").addEventListener("click", () => {
        this.toggleMenu();
      });

      if (nav.style.display === "block") {
        nav.classList.remove("animate__slideInDown");
        nav.classList.add("animate__slideOutUp");
        setTimeout(() => {
          nav.style.display = "none";
        }, 150);
      } else {
        nav.style.display = "block";
        nav.classList.remove("animate__slideOutUp");
        nav.classList.add("animate__slideInDown");
      }
    }
  }
}
</script>

<style>
@charset "UTF-8";
/*!
 * animate.css - https://animate.style/
 * Version - 4.1.1
 * Licensed under the MIT license - http://opensource.org/licenses/MIT
 *
 * Copyright (c) 2020 Animate.css
 */:root {
 --animate-duration:0.3s;
 --animate-delay:0s;
 --animate-repeat:1
}
.animate__animated {
 -webkit-animation-duration:1s;
 animation-duration:1s;
 -webkit-animation-duration:var(--animate-duration);
 animation-duration:var(--animate-duration);
 -webkit-animation-fill-mode:both;
 animation-fill-mode:both
}
.animate__animated.animate__faster {
 -webkit-animation-duration:.5s;
 animation-duration:.5s;
 -webkit-animation-duration:calc(var(--animate-duration)/2);
 animation-duration:calc(var(--animate-duration)/2)
}
@media (prefers-reduced-motion:reduce),print {
 .animate__animated {
  -webkit-animation-duration:1ms!important;
  animation-duration:1ms!important;
  -webkit-transition-duration:1ms!important;
  transition-duration:1ms!important;
  -webkit-animation-iteration-count:1!important;
  animation-iteration-count:1!important
 }
 .animate__animated[class*=Out] {
  opacity:0
 }
}
@-webkit-keyframes slideOutUp {
  from {
    transform: translate3d(0, 0, 0);
  }

  to {
    visibility: hidden;
    transform: translate3d(0, -100%, 0);
  }
}
@keyframes slideOutUp {
  from {
    transform: translate3d(0, 0, 0);
  }

  to {
    visibility: hidden;
    transform: translate3d(0, -100%, 0);
  }
}
.animate__slideOutUp {
 -webkit-animation-name:slideOutUp;
 animation-name:slideOutUp
}
@-webkit-keyframes slideInDown {
  from {
    transform: translate3d(0, -100%, 0);
    visibility: visible;
  }

  to {
    transform: translate3d(0, 0, 0);
  }
}
@keyframes slideInDown {
  from {
    transform: translate3d(0, -100%, 0);
    visibility: visible;
  }

  to {
    transform: translate3d(0, 0, 0);
  }
}
.animate__slideInDown {
 -webkit-animation-name:slideInDown;
 animation-name:slideInDown 
}

nav {
  display: flex;
  flex-direction: column;
  background: var(--secondaryColor);
}

#nav-content {
  display: none;
}

#nav-links {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.navbar-title {
  color: var(--textSecondaryColor);
  text-decoration: none;
  margin: 0.5rem;
  border-bottom: 1px solid var(--textSecondaryColor);
}

#nav-options {
  display: flex;
  flex-direction: row;
  justify-content: center;
}

@media (min-width: 930px) {
  #burger {
    display: none;
  }

  nav {
    display: flex;
    flex-direction: row;
    background: var(--secondaryColor)
  }

  #nav-content {
    display: flex;
    width: 100%;
  }

  .navbar-title {
    color: var(--textSecondaryColor);
    text-decoration: none;
    border-bottom: none;
    margin: 1rem;
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
    padding-right: 1rem;
  }

  .router-link-active {
    text-decoration: underline;
  }
}
</style>
