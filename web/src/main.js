import { createApp } from 'vue';
import { createI18n } from 'vue-i18n';

import '@dafcoe/vue-notification/dist/vue-notification.css';
import './assets/main.css';
import './assets/element.css';
import './assets/class.css';
import App from './App.vue';
import router from './router';
import Notifications from '@kyvg/vue3-notification';
import store from './utils/store';


// import translations
import fr from './locales/fr.json';
import en from './locales/en.json';

// configure i18n
const i18n = createI18n({
    seo: true,
    locale: import.meta.env.VITE_I18N_LOCALE || "en",
    fallbackLocale: import.meta.env.VITE_I18N_FALLBACK_LOCALE || "en",
    messages: { fr, en },
});

const app = createApp(App)

app.use(router);
app.use(store);
app.use(i18n);
app.use(Notifications);

app.config.globalProperties.currentUser = {
    user: null,
    token: null,
    isAuthentified: false,
    login(user, token, password) {
        console.log('login')
        console.log(user, token, password)
        this.user = user;
        this.token = token;
        this.isAuthentified = true;
        localStorage.setItem('user', user);
        localStorage.setItem('password', password);
        localStorage.setItem('token', token);
    },
    logout() {
        this.user = null;
        this.token = null;
        this.isAuthentified = false;
        localStorage.removeItem('user');
        localStorage.removeItem('password');
        localStorage.removeItem('token');
    }
};

app.mount('#app')
