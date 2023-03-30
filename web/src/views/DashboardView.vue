<template>
    <section class="content">
        <Navigator :prevPage="$router.options.history.state.back" />
        <h1>{{ $t("main.dashboard") }}</h1>
        <ProductList v-if="$route.name === 'dashboard'" v-model:products="products" />
        <FieldList v-else-if="$route.name === 'dashboardProduct'"
            :product="products.filter((product) => product.id === parseInt($route.params.id))[0]" />
    </section>
</template>

<script>
import api from "@/api";
import Navigator from "@/components/Navigator.vue";
import ProductList from "@/components/ProductList.vue";
import FieldList from "@/components/FieldList.vue";

export default {
    data() {
        return {
            products: [],
        };
    },
    created() {
        this.fetchProducts();
    },
    components: {
        Navigator,
        ProductList,
        FieldList
    },
    methods: {
        fetchProducts() {
            api.get("/products").then((response) => {
                console.log(response.data)
                this.products = response.data;
                console.log(this.products)
            });
        },
    },
};
</script>

<style></style>
