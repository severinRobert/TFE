import { createApp } from 'vue';
import { createI18n } from 'vue-i18n';

import '@dafcoe/vue-notification/dist/vue-notification.css';
import './assets/main.css';
import './assets/element.css';
import App from './App.vue';
import router from './router';
import VueNotificationList from '@dafcoe/vue-notification';

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
app.use(i18n);
app.use(VueNotificationList);

app.mount('#app')
