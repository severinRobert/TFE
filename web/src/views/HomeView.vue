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
        <h1>{{ $t("main.home") }}</h1>
        <MarkdownRenderer :source="$store.state.homeDescription" />
        <section>
            <h2>{{ $t("home.productLinks") }}</h2>
            <div v-if="$store.state.products.length" id="product-links">
                <router-link v-for="product in $store.state.products" class="offer textSecondaryColor" :to="`/offerList?productId=${product.id}`">{{ product.name }}</router-link>
            </div>
        </section>
    </section>
</template>

<style>
#product-links {
    display: flex;
    flex-wrap: wrap;
}
</style>
