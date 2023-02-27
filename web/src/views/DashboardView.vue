<template>
    <section class="content">
        <h1>{{ $t("main.dashboard") }}</h1>
        <ProductList v-if="$route.name === 'dashboard'" 
            v-model:products="products"
            @delete-product="deleteProduct" />
        <FieldList v-else-if="$route.name === 'dashboardProduct'" 
            :product="products.filter((product) => product.id === parseInt($route.params.id))[0]" />
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
    },
    components: {
        ProductList,
        FieldList,
    },
    methods: {
        deleteProduct(id) {
            console.log(id)
            this.products = this.products.filter((product) => product.id !== id);
            console.log(this.products)
        },
    },
};
</script>

<style>

</style>
