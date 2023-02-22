<template>
    <SearchBar @search="searchProduct" />
    <button @click="clickAdd">{{ $t("dashboard.addProduct") }}</button>
    <table>
        <thead>
            <tr>
                <th>{{ $t("dashboard.product") }}</th>
                <th>{{ $t("main.description") }}</th>
                <th>{{ $t("dashboard.remove") }}</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="(product, i) in filteredProducts" :id="i">
                <td @click="clickProduct(product)">{{ product.name }}</td>
                <td @click="clickProduct(product)">{{ product.description }}</td>
                <td><button @click="deleteProduct">x</button></td>
            </tr>
        </tbody>
    </table>
</template>

<script>
import SearchBar from "@/components/SearchBar.vue";

export default {
    name: 'product-list',
    props: {
        products: Array,
    },
    components: {
        SearchBar,
    },
    mounted() {
        this.filteredProducts = [...this.products];
    },
    data() {
        return {
            filteredProducts: [],
        };
    },
    methods: {
        searchProduct(text) {
            console.log(text);
            this.filteredProducts = this.products.filter((product) => {
                return product.name.toLowerCase().includes(text.toLowerCase());
            });
        },
        clickAdd() {
            this.$router.push({'path': '/dashboard/product/new'})
        },
        clickProduct(product) {
            console.log(product);
            this.$router.push({'path': '/dashboard/product/' + product.id})
        },
        deleteProduct(product) {
            console.log(product)
            this.$emit('delete-product', product);
        },
    },
};
</script>

<style></style>
