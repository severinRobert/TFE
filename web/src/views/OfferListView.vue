<template>
    <section class="content">
        <h1>{{ $t("main.offerList") }}</h1>
        <form id="form" action="#" @submit="search">
            <fieldset>
                <legend> 
                    <Selection :options="products" :selected="productId" @id-selected="selectProduct" text="form.chooseProduct" />
                </legend>
                <template  v-if="productFields[`${productId}`] != undefined && filteredOffers != undefined">
                    <Filters :fields="productFields[`${productId}`]" :arrayToFilter="productOffers" @filtered="applyFiltersOnOffers"/>
                </template>
                <p v-if="productId==0">Please select a product</p>
            </fieldset>
        </form>
        <table>
            <thead>
                <tr>
                    <th v-for="field in productFields[`${productId}`]">{{ field.display_name }}</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="offer in filteredOffers">
                    <td v-for="field in productFields[`${productId}`]">{{ offer['fields'][field.id] }}</td>
                </tr>
            </tbody>
        </table>
    </section>
</template>

<script>
import { headers } from "@/api";
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
            products: [],
            productId: 0,
            productFields: {},
            types: {},
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
        this.fetchProducts();
        this.fetchTypes();
    },
    methods: {
        fetchOffers(id=this.productId) {
            headers().get(`/offers/product/${id}/details`).then((response) => {
                this.offers[`${id}`] = response.data;
                this.productOffers = response.data;
                this.filteredOffers = response.data;
            });
        },
        fetchProducts() {
            headers().get("/products").then((response) => {
                this.products = response.data;
            });
        },
        fetchTypes() {
            headers().get("/types").then((response) => {
                this.types = response.data.reduce((types, type) => {
                    types[type.id] = type.name;
                    return types;
                }, {});
            });
        },
        fetchFields() {
            headers().get(`/products/${this.productId}/fields`).then((response) => {
                this.productFields[`${this.productId}`] = response.data;
                for(let field of response.data) {
                    if(field.selections_groups_id && !this.$selectionsGroups[`${field.selections_groups_id}`]) {
                        this.fetchSelections(field.selections_groups_id);
                    }
                }
            }).catch((error) => {
                this.error = error;
            });
        },
        fetchSelections(id) {
            headers().get(`/selections_groups/${id}/selections`).then((response) => {
                this.$selectionsGroups[`${id}`] = response.data;
            }).catch((error) => {
                this.error = error;
            });
        },
        selectProduct(id) {
            this.productId = parseInt(id);
            if(!this.productFields[id] && id != 0) {
                this.fetchFields();
            }
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
