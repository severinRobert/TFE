<template>
    <footer>
        <span>{{ $t("footer.madeWith") }} <a href="https://github.com/severinRobert/TFE"
                target="_blank">MarketEase</a></span>
        <router-link to="/gdpr">{{ $t("footer.privacyPolicy") }}</router-link>
        <a v-if="this.contact" :href="`mailto:${contact}`">{{ $t("main.contact") }}</a>
    </footer>
</template>

<script>
import { headers } from "@/utils/api";

export default {
    name: "Footer",
    data() {
        return {
            contact: "",
        }
    },
    created() {
        headers().get(`/users/1/profile`).then((response) => {
            console.log(response.data)
            this.contact = response.data.contact;
        }).catch((error) => {
            this.$notify({
                type: 'error',
                text: error
            })
        });
    },
};
</script>

<style>
footer {
    display: flex;
    justify-content: space-around;
    padding: 1rem;
    background-color: var(--secondaryColor);
}
</style>
