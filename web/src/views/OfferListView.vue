<template>
    <section class="content">
        <h1>{{ $t("main.offerList") }}</h1>
        <form id="form" action="#" @submit="search">
            <fieldset>
                <legend> 
                    <Selection :options="$store.state.products" :selected="productId" @id-selected="selectProduct" text="form.chooseProduct" />
                </legend>
                <template  v-if="$store.state.productsFields[`${productId}`] != undefined && filteredOffers != undefined">
                    <h2>{{ $t("main.filters") }}</h2>
                    <Filters :fields="$store.state.productsFields[`${productId}`]" :arrayToFilter="productOffers" @filtered="applyFiltersOnOffers"/>
                </template>
                <p v-if="productId==0">{{ $t("form.pleaseSelectProduct") }}</p>
            </fieldset>
        </form>
        <div id="offerList-info">
            <span>{{ $t("offerList.resultNumber") + " : " + filteredOffers.length }}</span>
            <span class="bigSpaceLeft">{{ $t("offerList.displayMode") }} : </span>
            <Selection :options="[{id: 'card', name: 'card'}, {id: 'list', name: 'list'}]" 
                :selected="mode" @id-selected="selectMode" text="" />
        </div>
        <section v-if="filteredOffers.length && mode=='card'" id="offers">
            <OfferList :offers="filteredOffers" />
        </section>
        <table  v-if="filteredOffers.length && mode=='list'">
            <thead>
                <tr>
                    <th v-for="field in $store.state.productsFields[`${productId}`]">{{ field.display_name }}</th>
                    <th>{{ $t("main.owner") }}</th>
                    <th>{{ $t("main.created") }}</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="offer in filteredOffers" class="clickable" @click="clickOffer(offer.id)">
                    <td v-for="field in $store.state.productsFields[`${productId}`]">
                        {{ typeof(offer['fields'][field.id])== 'boolean' ? (offer['fields'][field.id] ? $t('main.yes') : $t('main.no')) : offer['fields'][field.id] }}
                    </td>
                    <td>{{ offer.username }}</td>
                    <td>{{ offer.start_datetime.toLocaleString() }}</td>
                </tr>
            </tbody>
        </table>
    </section>
</template>

<script>
import { headers } from "@/utils/api";
import Selection from "@/elements/Selection.vue";
import Filters from "@/components/Filters.vue";
import OfferList from "../components/OfferList.vue";

export default {
    name: 'form-view',
    components: {
        Selection,
        Filters,
        OfferList,
    },
    data() {
        return {
            offers: [],
            productOffers: [],
            filteredOffers: [],
            productId: 0,
            mode: 'card',
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
        if(this.$route.query.productId) {
            this.selectProduct(this.$route.query.productId);
        }
    },
    methods: {
        fetchOffers(id=this.productId) {
            headers().get(`/offers/product/${id}/details`).then((response) => {
                console.log("offers", response.data)
                this.offers[`${id}`] = response.data;
                this.productOffers = response.data;
                this.filteredOffers = response.data;
            });
        },
        selectProduct(id) {
            this.productId = parseInt(id);
            this.$router.push({ query: { productId: id } });
            this.$store.dispatch('fetchProductFields', id);
            if(!this.offers[id] && id != 0) {
                this.fetchOffers();
            } else {
                this.filteredOffers = this.offers[`${id}`]
            }
        },
        applyFiltersOnOffers(offers) {
            this.filteredOffers = offers;
        },
        selectMode(mode) {
            this.mode = mode;
        },
        clickOffer(id) {
            this.$router.push({ name: 'offer', params: { id: id } });
        },
    },
};
</script>

<style>
#offerList-info {
    margin: 1rem;
}
</style>
