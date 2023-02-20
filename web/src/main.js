import { createApp } from 'vue';
import { createI18n } from 'vue-i18n';

import './assets/main.css';
import './assets/element.css';
import App from './App.vue';
import router from './router';


// import translations
import fr from './locales/fr.json';
import en from './locales/en.json';

// configure i18n
const i18n = createI18n({
    locale: "en",
    fallbackLocale: "en",
    messages: { fr, en },
});

const app = createApp(App)

app.use(router)
app.use(i18n);

app.mount('#app')
