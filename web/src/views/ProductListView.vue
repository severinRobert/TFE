<template>
    <section class="content">
        <h1> Product List </h1>
        <form id="form" action="#" @submit="search">
            <fieldset>
                <legend> 
                    <Selection :options="products" :selected="productId" @id-selected="selectProduct" text="form.chooseProduct" />
                </legend>
                <div v-for="field in productFields[`${productId}`]">
                    <div v-if="field.is_filterable">
                        <p>{{ field.display_name }}</p>
                    </div>
                </div>
                <p v-if="productId==0">Please select a product</p>
                <button type="submit">{{ $t("main.search") }}</button>
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

export default {
    name: 'form-view',
    components: {
        Selection,
    },
    data() {
        return {
            offers: [],
            filteredOffers: [],
            products: [],
            productId: 0,
            productFields: {},
            selectionsGroups: {},
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
        search(e) {
            e.preventDefault(); // prevent the form from submitting 
            console.log("Search");
            console.log(e);
            let formData = new FormData(document.getElementById("severin"));
            console.log(formData)
            if(!this.offers[`${this.productId}`]) {
                this.fetchOffers();
            }
            this.filteredOffers = this.offers[`${this.productId}`]
            console.log("filtered offers : ", this.filteredOffers)
        },
        fetchOffers(id=this.productId) {
            console.log("Fetch offers")
            headers().get(`/offers/product/${id}/details`).then((response) => {
                console.log("offers : ", response.data)
                this.offers[`${id}`] = response.data;
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
            console.log("Fetch fields");
            headers().get(`/products/${this.productId}/fields`).then((response) => {
                console.log("fields : ", response.data);
                this.productFields[`${this.productId}`] = response.data;
                for(let field of response.data) {
                    if(field.selections_groups_id && !this.selectionsGroups[`${field.selections_groups_id}`]) {
                        this.fetchSelections(field.selections_groups_id);
                    }
                }
            }).catch((error) => {
                this.error = error;
            });
        },
        fetchSelections(id) {
            headers().get(`/selections_groups/${id}/selections`).then((response) => {
                console.log("selections : ", response.data)
                this.selectionsGroups[`${id}`] = response.data;
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
            console.log("filtered offers : ", this.filteredOffers)
        },
    },
};
</script>

<style>
</style>
