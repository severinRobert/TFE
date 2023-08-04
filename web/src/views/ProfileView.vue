<template>
    <section class="content">
        <h1> {{ $t("profile.title", {name: profile['username']}) }} </h1>
        <p v-if="userId!==userIdLocalStorage">{{ $t("main.contact") + " : " + profile['contact'] }}</p>
        <template v-else>
            <form id="form" action="#" @submit="submit">
                <p v-if="!profile['contact']" class="warning">{{ $t("profile.contactEmpty") }}</p>
                <div>
                    <label for="username">{{ $t("auth.username") }}</label>
                    <input name="username" id="username" :value="profile['username']" required />
                </div>
                <div>
                    <label for="contact">{{ $t("main.contact") }}</label>
                    <input name="contact" id="contact" :value="profile['contact']" />
                </div>
                <div>
                    <label for="email">{{ $t("auth.email") }}</label>
                    <input name="email" id="email" :value="profile['email']" />
                </div>
                <button @click="showModal('profile')">{{ $t("main.submit") }}</button>
            </form>
            <dialog id="dialog-profile">
                <h1>{{ $t("profile.edit") }}</h1>
                <input type="password" id="password-check" name="password" /><br/>
                <button @click="putProfile">{{ $t("main.submit") }}</button>
                <button class="cancel" @click="cancel">{{ $t("main.cancel") }}</button>
            </dialog>
        </template>
        <section id="profile-offers">
            <h2>{{ $t("profile.offers", {name: profile['username']}) }}</h2>
            <div id="offers" v-if="offers.length">
                <OfferList :offers="offers" :deletable="userId===userIdLocalStorage" @offer-deleted="deleteOffer"/>
            </div>
        </section>
    </section>
</template>

<script>
import { headers } from "@/utils/api";
import OfferList from "../components/OfferList.vue";

export default {
    name: 'form-view',
    components: {
        OfferList,
    },
    data() {
        return {
            profile: {},
            offers: [],
            userId: null,
            userIdLocalStorage: localStorage.getItem('user_id'),
        };
    },
    created() {
        this.userId = this.$route.params.id ? this.$route.params.id : localStorage.getItem('user_id');
        headers().get(`/users/${this.userId}/profile`).then((response) => {
            this.profile = response.data;
        }).catch((error) => {
            this.$notify({
                type: 'error',
                text: error
            })
        });
        headers().get(`/offers/user/${this.userId}/details`).then((response) => {
            this.offers = response.data;
        }).catch((error) => {
            this.$notify({
                type: 'error',
                text: error
            })
        });
    },
    methods: {
        showModal(type) {
            const dialog = document.getElementById("dialog-" + type);
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
        cancel(e) {
            const dialog = e.target.closest("dialog");
            dialog.close();
        },
        submit(e) {
            e.preventDefault();
        },
        putProfile(e) {
            e.preventDefault();
            let formData = new FormData(document.getElementById("form"));
            let password = document.getElementById("password-check").value;
            let profile = {};
            formData.forEach((value, key) => profile[key] = value);
            let data = {'profile': profile, 'password': password}
            console.log(data)
            headers().put(`/users/${localStorage.getItem('user_id')}`, data).then((response) => {
                this.profile = response.data;
                this.cancel(e);
                this.$notify({
                    type: 'success',
                    text: this.$t("profile.profileModified")
                })
            }).catch((error) => {
                this.$notify({
                    type: 'error',
                    text: error
                })
            });
        },
        deleteOffer(offerId) {
            this.offers = this.offers.filter(offer => offer.id !== offerId);
        },
    },
};
</script>

<style>
#offers {
    display: flex;
    flex-wrap: wrap;
}
</style>
