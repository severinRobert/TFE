<template>
    <section>
        <label for="product-name">Product name:</label>
        <input type="text" name="product-name" :value="product.name" />
        <label for="product-description">Product description:</label>
        <textarea name="product-description" :value="product.description" />
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
                <td><Selection :options="types" /></td>
                <td><input type="text" :value="field.description"></td>
            </tr>
        </tbody>
    </table>
</template>

<script>
import SearchBar from "@/components/SearchBar.vue";
import Selection from "@/components/Selection.vue";


export default {
    name: 'field-list',
    props: {
        product: {
            type: Object,
            default: {},
        },
        fields: {
            type: Array,
            default: [],
        }
    },
    components: {
        SearchBar,
        Selection,
    },
    created() {
        console.log(this.product);
        console.log(this.fields);

        this.types=[
            {id: 1, name: "int"},
            {id: 2, name: "string"},
            {id: 3, name: "float"},
            {id: 4, name: "bool"},
            {id: 5, name: "date"},
            {id: 6, name: "time"},
            {id: 7, name: "datetime"},
            {id: 8, name: "selection"},
            {id: 9, name: "multiselection"},
            {id: 10, name: "file"},
            {id: 11, name: "image"},
            {id: 12, name: "video"},
            {id: 13, name: "audio"},
            {id: 14, name: "url"},
            {id: 15, name: "email"},
            {id: 16, name: "phone"},
            {id: 17, name: "address"},
            {id: 18, name: "location"},
            {id: 19, name: "color"}
        ]
    },
    data() {
        return {
            filteredFields: [...this.fields],
        };
    },
    methods: {
        searchField(text) {
            this.filteredProducts = this.products.filter((product) => {
                return product.name.toLowerCase().includes(text.toLowerCase());
            });
        },
        saveProduct(ev) {
            console.log("Save product");
        },
    },
};
</script>

<style></style>
