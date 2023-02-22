<template>
    <section class="content">
        <h1>{{ $t("main.dashboard") }}</h1>
        <ProductList v-if="$route.name === 'dashboard'" :products="products" />
        <FieldList v-else-if="$route.name === 'dashboardProduct'" 
            :product="products.filter((product) => product.id === parseInt($route.params.id))[0]" 
            :fields="fields[$route.params.id]" />
    </section>
</template>

<script>
import ProductList from "@/components/ProductList.vue";
import FieldList from "@/components/FieldList.vue";

export default {
    created() {
        this.products=[
            { id: 1, name: "Banana", description: "This is a banana" },
            { id: 2, name: "Apple", description: "This is an apple" },
            { id: 3, name: "Orange", description: "This is an orange" },
            { id: 4, name: "Pineapple", description: "This is a pineapple" },
            { id: 5, name: "Strawberry", description: "This is a strawberry" }
        ];
        this.fields={
            1: [
                { id: 1, name: "Color", type: 19, description: "This is a color" },
                { id: 2, name: "Size", type: 2, description: "This is a size" },
                { id: 3, name: "Weight", type: 3, description: "This is a weight" },
                { id: 4, name: "Price", type: 3, description: "This is a price" },
                { id: 5, name: "Quantity", type: 1, description: "This is a quantity" },
                { id: 6, name: "Available", type: 4, description: "This is an availability" },
                { id: 7, name: "Expiration date", type: 7, description: "This is an expiration date" },
                { id: 8, name: "Image", type: 11, description: "This is an image" },
                { id: 9, name: "Video", type: 12, description: "This is a video" },
                { id: 10, name: "Audio", type: 13, description: "This is an audio" },
                { id: 11, name: "URL", type: 14, description: "This is an URL" },
                { id: 12, name: "Email", type: 15, description: "This is an email" },
                { id: 13, name: "Phone", type: 16, description: "This is a phone" },
                { id: 14, name: "Address", type: 17, description: "This is an address" },
                { id: 15, name: "Location", type: 18, description: "This is a location" },
            ]
        };
    },
    components: {
        ProductList,
        FieldList,
    },
};
</script>

<style>

</style>
