<template>
    <p v-if="!offers.length">{{ $t("offerList.noOffersToShow") }}</p>
    <router-link :to="`/offer/${offer.id}`" class="offer clickable" v-for="offer in offers">
        <h3 v-if="$store.getters.getProductById(offer['product_id'])" class="offer-title">
            {{ $store.getters.getProductById(offer['product_id'])['name'] }}
        </h3>
        <p class="offer-field" v-for="field in $store.state.productsFields[`${offer['product_id']}`]">
            {{ field.display_name }} : <b>{{ offer['fields'][`${field.id}`] ? offer['fields'][`${field.id}`] : "-" }}</b>
        </p>
        <p class="offer-footer">
            <router-link :to="`/profile/${offer.owner_id}`">{{ offer.username }}</router-link>
            <span>{{ formatDate(offer.start_datetime) }}</span>
        </p>
        <button v-if="deletable" class="cancel offer-button" @click.prevent="deleteOffer(offer.id)">{{ $t("main.delete") }}</button>
        <button v-if="$store.state.favorites.includes(offer.id) && favoritable" class="cancel offer-button"  @click.prevent="favorite(offer.id)">{{ $t("offerList.removeFromFavorites") }}</button>
        <button v-else-if="favoritable" class="validation offer-button"  @click.prevent="favorite(offer.id)">{{ $t("offerList.addToFavorites") }}</button>
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
        deletable: {
            type: Boolean,
            default: false,
        },
        favoritable: {
            type: Boolean,
            default: false,
        },
    },
    emits: ['offer-deleted'],
    components: {
        Selection,
        Filters,
    },
    created() {
        this.$store.dispatch('fetchProducts');
        this.$store.dispatch('fetchTypes');
        if(this.$store.state.role) {
            this.$store.dispatch('fetchFavorites', localStorage.getItem('user_id'));
        }
        for (let offer of this.offers) {
            this.$store.dispatch('fetchProductFields', offer['product_id']);
        }
    },
    methods: {
        formatDate(date) {
            date = date.split(/[-T:.]/).slice(0,-1)
            date[1] = parseInt(date[1]) - 1;
            return new Date(Date.UTC(...date)).toLocaleDateString();
        },
        async favorite(id) {
            const data = {
                user_id: localStorage.getItem('user_id'),
                offer_id: id,
            };
            const isFavorite = this.$store.state.favorites.includes(id);
            let error = null;
            if(isFavorite) {
                error = await this.$store.dispatch("removeFavorite", data);
            } else {
                error = await this.$store.dispatch("addFavorite", data);
            }
            if(error) {
                this.$notify({
                    type: 'error',
                    text: error
                });
            } else {
                this.$notify({
                    type: 'success',
                    text: isFavorite ? this.$t('offerList.offerRemovedFromFavorites') : this.$t('offerList.offerAddedToFavorites')
                });
            }
        },
        deleteOffer(id) {
            if(confirm(this.$t('offerList.deleteConfirmation'))) {
                headers().delete("/offers/" + id).then((response) => {
                    this.$notify({
                        type: 'success',
                        text: this.$t('offerList.offerDeleted')
                    });
                    this.$emit('offer-deleted', id);
                }).catch((error) => {
                    this.$notify({
                        type: 'error',
                        text: error
                    });
                });
            }
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

.offer *:not(a) {
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

.offer-footer {
    display: flex;
    justify-content: space-between;
    width: 100%;
    margin: 0.5rem 0 0 0;
    font-size: small;
}

.offer-button {
    color: var(--textPrimaryColor) !important;
    width: 100%;
    border-radius: 5px;
    padding: 0.3rem;
    margin: 1rem 0 0 0;
}
</style>
