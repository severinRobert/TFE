<template>
    <SearchBar @search="searchField" />
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
                <td>{{ field.name }}</td>
                <td>{{ field.type }}</td>
                <td>{{ field.description }}</td>
            </tr>
        </tbody>
    </table>
</template>

<script>
import SearchBar from "@/components/SearchBar.vue";

export default {
    name: 'field-list',
    components: {
        SearchBar,
    },
    mounted() {
        let f=[
            { name: "name", type: "str", description: "This is a banana" },
            { name: "price", type: "int", description: "This is an apple" },
            { name: "description", type: "str", description: "This is an orange" },
        ];
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
    },
};
</script>

<style></style>
