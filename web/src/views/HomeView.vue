<script>

export default {
    name: "HomeView",
    created() {
        this.$store.dispatch("fetchProducts");
    },
};
</script>

<template>
    <section class="content">
        <h1> Home </h1>
        <section id="product-links">
            <h2>{{ $t("home.productLinks") }}</h2>
            <router-link v-if="$store.state.products.length" v-for="product in $store.state.products" class="offer textSecondaryColor" :to="`/offerList?productId=${product.id}`">{{ product.name }}</router-link>
        </section>
    </section>
</template>

<style>
</style>
