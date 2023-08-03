<template>
    <section class="content">
        <h1>{{ $t("main.offer") }}</h1>
        <section v-if="offer">
            <h2 v-if="$store.getters.getProductById(offer['product_id'])">{{ $store.getters.getProductById(offer.product_id).name }}</h2>
            <p>
                {{ $t("main.owner") }} : 
                <router-link :to="`/profile/${offer.owner_id}`">{{ offer.username }}</router-link>
            </p>
            <p>{{ $t("main.contact") }} : {{ offer.contact }}</p>
            <section>
                <p class="offer-field" v-for="field in $store.state.productsFields[`${offer['product_id']}`]">
                    {{ field.display_name }} : <b>{{ offer['fields'][`${field.id}`] ? offer['fields'][`${field.id}`] : "-" }}</b>
                </p>
            </section>
        </section>
    </section>
</template>

<script>
import { headers } from "@/utils/api";

export default {
    name: 'offer-view',
    data() {
        return {
            offerId: this.$route.params.id,
            offer: {},
        };
    },
    created() {
        this.$store.dispatch('fetchProducts');
        headers().get(`/offers/${this.offerId}/details`).then((response) => {
            this.offer = response.data;
            this.$store.dispatch('fetchProductFields', this.offer['product_id']);
        });
    },
};
</script>

<style>
#offerList-info {
    margin: 1rem;
}
</style>
