<template>
    <SearchBar @search="searchProduct" />
    <table>
        <thead>
            <tr>
                <th>{{ $t("dashboard.product") }}</th>
                <th>{{ $t("main.description") }}</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="product in filteredProducts" :key="product.name" v-on:click="clickProduct(product)">
                <td>{{ product.name }}</td>
                <td>{{ product.description }}</td>
            </tr>
        </tbody>
    </table>
</template>

<script>
import SearchBar from "@/components/SearchBar.vue";

export default {
    name: 'product-list',
    components: {
        SearchBar,
    },
    mounted() {
        let p=[
            { name: "Banana", description: "This is a banana" },
            { name: "Apple", description: "This is an apple" },
            { name: "Orange", description: "This is an orange" },
            { name: "Pineapple", description: "This is a pineapple" },
            { name: "Strawberry", description: "This is a strawberry" },
            { name: "Watermelon", description: "This is a watermelon" },
            { name: "Peach", description: "This is a peach" },
            { name: "Pear", description: "This is a pear" },
            { name: "Grape", description: "This is a grape" },
            { name: "Cherry", description: "This is a cherry" },
            { name: "Kiwi", description: "This is a kiwi" },
            { name: "Mango", description: "This is a mango" },
            { name: "Lemon", description: "This is a lemon" },
            { name: "Pomegranate", description: "This is a pomegranate" },
            { name: "Raspberry", description: "This is a raspberry" },
            { name: "Blueberry", description: "This is a blueberry" },
            { name: "Blackberry", description: "This is a blackberry" },
            { name: "Cranberry", description: "This is a cranberry" },
            { name: "Papaya", description: "This is a papaya" },
            { name: "Coconut", description: "This is a coconut" },
            { name: "Avocado", description: "This is an avocado" },
            { name: "Tomato", description: "This is a tomato" },
            { name: "Potato", description: "This is a potato" },
            { name: "Onion", description: "This is an onion" },
            { name: "Garlic", description: "This is a garlic" },
            { name: "Carrot", description: "This is a carrot" },
            { name: "Cucumber", description: "This is a cucumber" },
            { name: "Spinach", description: "This is a spinach" },
            { name: "Broccoli", description: "This is a broccoli" },
            { name: "Cabbage", description: "This is a cabbage" },
            { name: "Lettuce", description: "This is a lettuce" },
            { name: "Corn", description: "This is a corn" },
        ];
        this.products = [...p];
        this.filteredProducts = [...p];
    },
    data() {
        return {
            products: [],
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
        clickProduct(product) {
            console.log(product);
            this.$router.push({'path': '/dashboard/product/1'})
        },
    },
};
</script>

<style></style>
