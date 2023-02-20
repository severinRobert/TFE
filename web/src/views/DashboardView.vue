<template>
    <section class="content">
        <h1>{{ $t("main.dashboard") }}</h1>
        <ProductList v-if="$route.name === 'dashboard'" />
        <FieldList v-else-if="$route.name === 'dashboardProduct'" />
    </section>
</template>

<script>
import ProductList from "@/components/ProductList.vue";
import FieldList from "@/components/FieldList.vue";

export default {
    mounted() {
        console.log(this.$route)
    },
    components: {
        ProductList,
        FieldList,
    },
};
</script>

<style></style>
