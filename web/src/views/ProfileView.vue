<template>
    <section class="content">
        <h1> {{ $t("profile.title", { name: profile['username'] }) }} </h1>
        <p v-if="profile['username'] !== $store.state.username">{{ $t("main.contact") + " : " + profile['contact'] }}</p>
        <template v-else>
            <form id="form" action="#" @submit="submit">
                <p v-if="!profile['contact']" class="warning">{{ $t("profile.contactEmpty") }}</p>
                <div>
                    <label for="username">{{ $t("auth.username") }}</label>
                    <input name="username" id="username" :value="profile['username']" required />
                </div>
                <div>
                    <label for="contact">{{ $t("main.contact") }}</label>
                    <input name="contact" id="contact" :value="profile['contact']" title="test" />
                    <span>{{ $t("profile.contactHelp") }}</span>
                </div>
                <div>
                    <label for="email">{{ $t("auth.email") }}</label>
                    <input name="email" id="email" :value="profile['email']" />
                </div>
                <button class="validation" @click="showModal('profile')">{{ $t("main.submit") }}</button>
            </form>
            <dialog id="dialog-profile">
                <h1>{{ $t("profile.edit") }}</h1>
                <input type="password" id="password-check" name="password" /><br />
                <button class="validation" @click="putProfile">{{ $t("main.submit") }}</button>
                <button class="cancel" @click="cancel">{{ $t("main.cancel") }}</button>
            </dialog>
            <button class="validation" @click="showModal('password')">{{ $t("profile.changePassword") }}</button>
            <dialog id="dialog-password">
                <h1>{{ $t("profile.changePassword") }}</h1>
                <form action="#" @submit="changePassword">
                    <label for="password-old">{{ $t("profile.oldPassword") }}*</label>
                    <input type="password" id="passwordOld" name="password-old" required /><br />
                    <label for="password-new">{{ $t("profile.newPassword") }}*</label>
                    <input type="password" id="passwordNew" name="password-new" required /><br />
                    <label for="password-confirmation">{{ $t("auth.passwordConfirm") }}*</label>
                    <input type="password" id="passwordConfirmation" name="password-confirmation" required /><br />
                    <button class="validation"  type="submit">{{ $t("main.submit") }}</button>
                </form>
                <button class="cancel" @click="cancel">{{ $t("main.cancel") }}</button>
            </dialog>
        </template>
        <section v-if="profile['username'] === $store.state.username" id="profile-favorites">
            <h2>{{ $t("profile.favorites", { name: profile['username'] }) }}</h2>
            <div v-if="favorites.length" id="favorites" class="offers-list">
                <OfferList :offers="favorites" :favoritable="true" />
            </div>
        </section>
        <section id="profile-offers">
            <h2>{{ $t("profile.offers", { name: profile['username'] }) }}</h2>
            <div v-if="offers.length" id="offers" class="offers-list">
                <OfferList :offers="offers" :deletable="profile['username'] === $store.state.username"
                    :favoritable="profile['username'] !== $store.state.username && Boolean($store.state.role)"
                    @offer-deleted="deleteOffer" />
            </div>
        </section>
        <button v-if="profile['username'] === $store.state.username" class="cancel" @click="showModal('deleteProfile')">{{
            $t("profile.deleteProfile") }}</button>
        <dialog id="dialog-deleteProfile">
            <h1>{{ $t("profile.deleteProfile") }}</h1>
            <p class="warning">{{ $t("profile.deleteProfileWarning") }}</p>
            <input type="password" id="password-delete" name="password" /><br />
            <button class="validation" @click="deleteProfile">{{ $t("main.submit") }}</button>
            <button class="cancel" @click="cancel">{{ $t("main.cancel") }}</button>
        </dialog>
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
            favorites: [],
            userId: null,
            userIdLocalStorage: localStorage.getItem('user_id'),
        };
    },
    watch: {
        '$route.params.id': function () {
            this.userId = this.$route.params.id ? this.$route.params.id : localStorage.getItem('user_id');
            this.getProfile();
        },
        '$store.state.username': function () {
            this.getProfile();
        },
    },
    created() {
        this.userId = this.$route.params.id ? this.$route.params.id : localStorage.getItem('user_id');
        this.getProfile();
    },
    methods: {
        async getProfile() {
            await headers().get(`/users/${this.userId}/profile`).then((response) => {
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
            if (this.profile["username"] === this.$store.state.username) {
                headers().get(`/users/${this.userId}/favorites/details`).then((response) => {
                    this.favorites = response.data;
                }).catch((error) => {
                    this.$notify({
                        type: 'error',
                        text: error
                    })
                });
            }
        },
        changePassword(e) {
            e.preventDefault(); // prevent the form from submitting 
            const form = e.target;
            if (form.passwordNew.value !== form.passwordConfirmation.value) {
                this.$notify({
                    type: 'error',
                    text: this.$t("auth.passwordMismatch")
                })
                return;
            }
            let data = { 'username': this.$store.state.username, 'new_password': form.passwordNew.value, 'old_password': form.passwordOld.value }
            console.log(data)
            headers().put(`/users/${localStorage.getItem('user_id')}/password`, data).then((response) => {
                this.profile = response.data;
                this.cancel(e);
                this.$notify({
                    type: 'success',
                    text: this.$t("profile.passwordChanged")
                })
            }).catch((error) => {
                this.$notify({
                    type: 'error',
                    text: error
                })
            });
        },
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
            let data = { 'profile': profile, 'password': password }
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
        deleteProfile(e) {
            e.preventDefault();
            let password = document.getElementById("password-delete").value;
            headers().delete(`/users/${localStorage.getItem('user_id')}`, { 'data': { 'password': password } }).then((response) => {
                this.cancel(e);
                this.$notify({
                    type: 'success',
                    text: this.$t("profile.profileDeleted")
                })
                localStorage.removeItem('token');
                localStorage.removeItem('user');
                localStorage.removeItem('password');
                localStorage.removeItem('role');
                this.$store.commit("setUsername", "");
                this.$store.commit("setRole", "");
                this.$router.push("/");
            }).catch((error) => {
                this.$notify({
                    type: 'error',
                    text: error
                })
            });
        },
    },
};
</script>

<style></style>
