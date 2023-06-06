<template>
    <section class="content">
        <h1>{{ $t("main.offerList") }}</h1>
        <form id="form" action="#" @submit="search">
            <fieldset>
                <legend> 
                    <Selection :options="$store.state.products" :selected="productId" @id-selected="selectProduct" text="form.chooseProduct" />
                </legend>
                <template  v-if="$store.state.productsFields[`${productId}`] != undefined && filteredOffers != undefined">
                    <Filters :fields="$store.state.productsFields[`${productId}`]" :arrayToFilter="productOffers" @filtered="applyFiltersOnOffers"/>
                </template>
                <p v-if="productId==0">Please select a product</p>
            </fieldset>
        </form>
        <table>
            <thead>
                <tr>
                    <th v-for="field in $store.state.productsFields[`${productId}`]">{{ field.display_name }}</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="offer in filteredOffers">
                    <td v-for="field in $store.state.productsFields[`${productId}`]">{{ offer['fields'][field.id] }}</td>
                </tr>
            </tbody>
        </table>
    </section>
</template>

<script>
import { headers } from "@/utils/api";
import Selection from "@/elements/Selection.vue";
import Filters from "@/components/Filters.vue";

export default {
    name: 'form-view',
    components: {
        Selection,
        Filters,
    },
    data() {
        return {
            offers: [],
            productOffers: [],
            filteredOffers: [],
            productId: 0,
            typeToInput: {
                'int' : 'number',
                'string' : 'text',
                'float' : 'number',
                'bool' : 'checkbox',
                'date' : 'date',
                'time' : 'time',
                'datetime' : 'datetime-local',
                'selection' : 'Selection',
                'multiselection' : 'MultiSelection',
                'file' : 'file',
                'image' : 'file',
                'video' : 'file',
                'audio' : 'file',
                'url' : 'url',
                'email' : 'email',
                'phone' : 'tel',
                'address' : 'Address',
                'color' : 'color',
            },
        };
    },
    created() {
        this.$store.dispatch('fetchProducts');
        this.$store.dispatch('fetchTypes');
    },
    methods: {
        fetchOffers(id=this.productId) {
            headers().get(`/offers/product/${id}/details`).then((response) => {
                this.offers[`${id}`] = response.data;
                this.productOffers = response.data;
                this.filteredOffers = response.data;
            });
        },
        selectProduct(id) {
            this.productId = parseInt(id);
            this.$store.dispatch('fetchFields', id);
            if(!this.offers[id] && id != 0) {
                this.fetchOffers();
            } else {
                this.filteredOffers = this.offers[`${id}`]
            }
        },
        applyFiltersOnOffers(offers) {
            this.filteredOffers = offers;
        },
    },
};
</script>

<style>
</style>
