<template>
    <section class="content">
        <Navigator :prevPage="$router.options.history.state.back" />
        <h1>{{ $t("main.dashboard") }}</h1>
        <ProductList v-if="$route.name === 'dashboard'" v-model:products="products" />
        <SelectionsGroupList v-if="$route.name === 'dashboard'" v-model:selectionsGroups="selectionsGroups" />
        <FieldList v-else-if="$route.name === 'dashboardProduct'"
            :product="products.filter((product) => product.id === parseInt($route.params.id))[0]" />
        <SelectionList v-else-if="$route.name === 'dashboardSelectionsGroup'"
            :selectionsGroups="selectionsGroups.filter((selectionsGroup) => selectionsGroup.id === parseInt($route.params.id))[0]" />
    </section>
</template>

<script>
import { headers } from "@/utils/api";
import Navigator from "@/components/Navigator.vue";
import ProductList from "@/components/ProductList.vue";
import SelectionsGroupList from "@/components/SelectionsGroupList.vue";
import FieldList from "@/components/FieldList.vue";
import SelectionList from "@/components/SelectionList.vue";

export default {
    data() {
        return {
            products: [],
            selectionsGroups: [],
        };
    },
    created() {
        this.fetchData();
    },
    components: {
        Navigator,
        ProductList,
        SelectionsGroupList,
        FieldList,
        SelectionList,
    },
    methods: {
        fetchData() {
            headers().get("/products").then((response) => {
                this.products = response.data;
            });
            headers().get("/selections_groups").then((response) => {
                this.selectionsGroups = response.data;
            });
        },
    },
};
</script>

<style></style>
