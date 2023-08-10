<script>
import MarkdownRenderer from "@/utils/MarkdownRenderer.vue";

export default {
    name: "HomeView",
    components: {
        MarkdownRenderer,
    },
    created() {
        this.$store.dispatch("fetchProducts");
    },
};
</script>

<template>
    <section class="content">
        <h1> Home </h1>
        <MarkdownRenderer :source="$store.state.homeDescription" />
        <section id="product-links">
            <h2>{{ $t("home.productLinks") }}</h2>
            <router-link v-if="$store.state.products.length" v-for="product in $store.state.products" class="offer textSecondaryColor" :to="`/offerList?productId=${product.id}`">{{ product.name }}</router-link>
        </section>
    </section>
</template>

<style>
</style>
