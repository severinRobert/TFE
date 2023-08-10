<template>
    <section class="content">
        <!-- <Navigator :prevPage="$router.options.history.state.back" /> -->
        <h1>{{ $t("main.dashboard") }}</h1>
        <template v-if="$route.name === 'dashboard'">
            <SiteSettings />
            <SiteColors />
            <ProductList />
            <SelectionsGroupList />
        </template>
        <FieldList v-if="$route.name === 'dashboardProduct'"
            :productId="parseInt($route.params.id)" />
        <SelectionList v-if="$route.name === 'dashboardSelectionsGroup'"
            :selectionsGroupId="parseInt($route.params.id)" />
    </section>
</template>

<script>
import Navigator from "@/components/Navigator.vue";
import ProductList from "@/components/ProductList.vue";
import SelectionsGroupList from "@/components/SelectionsGroupList.vue";
import FieldList from "@/components/FieldList.vue";
import SelectionList from "@/components/SelectionList.vue";
import SiteColors from "@/components/SiteColors.vue";
import SiteSettings from "@/components/SiteSettings.vue";

export default {
    components: {
        Navigator,
        ProductList,
        SelectionsGroupList,
        FieldList,
        SelectionList,
        SiteColors,
        SiteSettings,
    },
    created() {
        if(this.$store.state.role !== 'Administrator') {
            this.$router.push('/')
        }
    },
};
</script>

<style></style>
