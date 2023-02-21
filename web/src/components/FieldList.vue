<template>
    <section>
        <label for="product-name">Product name:</label>
        <input type="text" name="product-name" />
        <label for="product-description">Product description:</label>
        <textarea name="product-description" />
    </section>

    <SearchBar @search="searchField" />
    <button @click="saveProduct">{{ $t("dashboard.save") }}</button>
    <table>
        <thead>
            <tr>
                <th>{{ $t("dashboard.fieldName") }}</th>
                <th>{{ $t("dashboard.type") }}</th>
                <th>{{ $t("main.description") }}</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="field in filteredFields" :key="field.name">
                <td><input type="text" :value="field.name"></td>
                <td><input type="text" :value="field.type"></td>
                <td><input type="text" :value="field.description"></td>
            </tr>
        </tbody>
    </table>
</template>

<script>
import SearchBar from "@/components/SearchBar.vue";

let f=[
    { name: "name", type: "str", description: "This is a banana" },
    { name: "price", type: "int", description: "This is an apple" },
    { name: "description", type: "str", description: "This is an orange" },
];

export default {
    name: 'field-list',
    components: {
        SearchBar,
    },
    mounted() {
        this.fields = [...f];
        this.filteredFields = [...f];
    },
    data() {
        return {
            fields: [],
            filteredFields: [],
        };
    },
    methods: {
        searchField(text) {
            console.log(text);
            this.filteredProducts = this.products.filter((product) => {
                return product.name.toLowerCase().includes(text.toLowerCase());
            });
        },
        saveProduct(ev) {
            console.log(ev);
        },
    },
};
</script>

<style></style>
