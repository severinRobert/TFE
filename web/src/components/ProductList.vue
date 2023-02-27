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
            <tr v-for="product in filteredProducts" :key="product.id">
                <td @click="clickProduct(product)">{{ product.name }}</td>
                <td @click="clickProduct(product)">{{ product.description }}</td>
                <td><button @click="deletePrduct(product.id)">x</button></td>
            </tr>
        </tbody>
    </table>
</template>

<script>
import SearchBar from "@/components/SearchBar.vue";

export default {
    name: 'product-list',
    props: {
        products: {
            type: Array,
            required: true,
        },
    },
    components: {
        SearchBar,
    },
    mounted() {
        this.filteredProducts = [...this.products];
    },
    emits: ['delete-product', 'update:products'],
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
            this.$router.push({'path': '/dashboard/product/' + product.id})
        },
        deletePrduct(id) {
            this.$emit("delete-product", id);
            this.$emit("update:products", this.products.filter((product) => product.id !== id));
        },
    },
};
</script>

<style></style>
