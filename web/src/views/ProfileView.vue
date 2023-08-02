<template>
    <section class="content">
        <h1> {{ $t("profile.title", {name: profile['username']}) }} </h1>
        <p v-if="$route.name=='profileWithId'">{{ $t("profile.contact") + " : " + profile['contact'] }}</p>
        <template v-else>
            <form id="form" action="#" @submit="submit">
                <div>
                    <label for="username">username</label>
                    <input name="username" id="username" :value="profile['username']" required />
                </div>
                <div>
                    <label for="contact">contact</label>
                    <input name="contact" id="contact" :value="profile['contact']" required />
                </div>
                <div>
                    <label for="email">email</label>
                    <input name="email" id="email" :value="profile['email']" required />
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
                <OfferList :offers="offers" />
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
        };
    },
    created() {
        let user_id = localStorage.getItem('user_id');
        headers().get(`/users/${user_id}/profile`).then((response) => {
            this.profile = response.data;
        }).catch((error) => {
            this.error = error;
        });
        headers().get(`/offers/user/${user_id}/details`).then((response) => {
            this.offers = response.data;
        }).catch((error) => {
            this.error = error;
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
            let profile = { 'id': localStorage.getItem('user_id') };
            formData.forEach((value, key) => profile[key] = value);
            let data = {'password': password}
            headers().put(`/users/${localStorage.getItem('user_id')}`, password).then((response) => {
                this.profile = response.data;
                this.cancel(e);
            }).catch((error) => {
                this.error = error;
            });
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
