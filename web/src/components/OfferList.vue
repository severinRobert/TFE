<template>
    <router-link :to="`/offer/${offer.id}`" class="offer clickable" v-for="offer in offers">
        <h3 class="offer-title">{{ $store.getters.getProductById(offer['product_id'])['name'] }}</h3>
        <p class="offer-field" v-for="field in $store.state.productsFields[`${offer['product_id']}`]">
            {{ field.display_name }} : <b>{{ offer['fields'][`${field.id}`] ? offer['fields'][`${field.id}`] : "-" }}</b>
        </p>
        <p class="offer-date">{{ formatDate(offer.start_datetime) }}</p>
    </router-link>
</template>

<script>
import { headers } from "@/utils/api";
import Selection from "@/elements/Selection.vue";
import Filters from "@/components/Filters.vue";

export default {
    name: 'form-view',
    props: {
        offers: {
            type: Array,
            required: true,
        },
    },
    components: {
        Selection,
        Filters,
    },
    created() {
        this.$store.dispatch('fetchProducts');
        this.$store.dispatch('fetchTypes');
        for (let offer of this.offers) {
            this.$store.dispatch('fetchFields', offer['product_id']);
        }
        console.log("offers : ", this.offers)
        console.log("products : ", this.$store.state.productsFields)
    },
    methods: {
        formatDate(date) {
            date = date.split(/[-T:.]/).slice(0,-1)
            date[1] = parseInt(date[1]) - 1;
            return new Date(Date.UTC(...date)).toLocaleDateString();
        },
    },
};
</script>

<style>
.offer {
    border: 1px solid var(--secondaryColor);
    margin: 10px;
    padding: 10px;
    border-radius: 10px;
    transition: 0.3s;
    background-color: var(--secondaryColor);
    text-decoration: none;
}

.offer * {
    color: var(--primaryColor);
}

.offer:hover {
    transform: translate(-5px, -5px);
    box-shadow: 5px 5px 10px -5px var(--shadowColor);
}

.offer:active {
    transform: translate(0px, 0px);
    box-shadow: 0px 0px 0px 0px var(--shadowColor);
}

.offer-title {
    text-align: center;
    margin: 0 0 0.5rem 0;
}

.offer-field {
    width: fit-content;
}

.offer-date {
    width: 100%;
    text-align: right;
    margin: 0;
    font-size: small;
}
</style>