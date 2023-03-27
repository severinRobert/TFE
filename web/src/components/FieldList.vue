<template>
    <section>
        <label for="product-name">Product name:</label>
        <input type="text" name="product-name" :value="product.name" />
        <label for="product-description">Product description:</label>
        <textarea name="product-description" :value="product.description" />
    </section>

    <SearchBar @search="searchField" />
    <button @click="saveProduct">{{ $t("dashboard.save") }}</button>
    <button @click="restoreProduct">{{ $t("dashboard.restore") }}</button>
    <table>
        <thead>
            <tr>
                <th>{{ $t("dashboard.fieldName") }}</th>
                <th>{{ $t("dashboard.type") }}</th>
                <th>{{ $t("main.description") }}</th>
                <th>{{ $t("dashboard.remove") }}</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="field in filteredFields" :key="field.name">
                <td><input type="text" :value="field.name"></td>
                <td><Selection :options="types" :selected="field.type" /></td>
                <td><input type="text" :value="field.description"></td>
                <td><button @click="deleteField(field.id)">x</button></td>
            </tr>
            <tr>
                <td><input type="text" :placeholder="$t('dashboard.addField')" v-model="newField.name" /></td>
                <td><Selection :options="types" :selected="newField.type" /></td>
                <td><input type="text" :placeholder="$t('dashboard.addField')" v-model="newField.description" /></td>
                <td><button @click="addField">{{ $t("dashboard.addField") }}</button></td>
            </tr>
        </tbody>
    </table>
</template>

<script>
import SearchBar from "@/components/SearchBar.vue";
import Selection from "@/components/Selection.vue";
import { useNotificationStore } from '@dafcoe/vue-notification'
const { setNotification } = useNotificationStore()

export default {
    name: 'field-list',
    props: {
        product: {
            type: Object,
            default: {},
        }
    },
    data() {
        return {
            fields: [],
            filteredFields: [],
            newField: {
                name: "",
                description: "",
            },
        };
    },
    components: {
        SearchBar,
        Selection,
    },
    created() {
        this.fetchData();
    },
    methods: {
        searchField(text) {
            this.filteredFields = this.fields.filter((field) => {
                return field.name.toLowerCase().includes(text.toLowerCase());
            });
        },
        saveProduct(ev) {
            console.log("Save product");
        },
        restoreProduct(ev) {
            console.log("Restore product");
            this.fetchData();
        },
        fetchData() {
            console.log("Fetch data");
            this.fields=[
                { id: 1, name: "Color", type: 19, description: "This is a color" },
                { id: 2, name: "Size", type: 2, description: "This is a size" },
                { id: 3, name: "Weight", type: 3, description: "This is a weight" },
                { id: 4, name: "Price", type: 3, description: "This is a price" },
                { id: 5, name: "Quantity", type: 1, description: "This is a quantity" },
                { id: 6, name: "Available", type: 4, description: "This is an availability" },
                { id: 7, name: "Expiration date", type: 7, description: "This is an expiration date" },
                { id: 8, name: "Image", type: 11, description: "This is an image" },
                { id: 9, name: "Video", type: 12, description: "This is a video" },
                { id: 10, name: "Audio", type: 13, description: "This is an audio" },
                { id: 11, name: "URL", type: 14, description: "This is an URL" },
                { id: 12, name: "Email", type: 15, description: "This is an email" },
                { id: 13, name: "Phone", type: 16, description: "This is a phone" },
                { id: 14, name: "Address", type: 17, description: "This is an address" },
                { id: 15, name: "Location", type: 18, description: "This is a location" },
            ];
            this.filteredFields = this.fields;
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
        addField(ev) {
            console.log("Add field");
            const name = this.newField.name;
            const type = Number(ev.target.parentElement.parentElement.children[1].children[0].value);
            const description = this.newField.description;

            console.log(name, type, description)

            if(this.fields.find((field) => field.name === name)) {
                setNotification({
                    type: 'error',
                    message: this.$t('dashboard.fieldExists')
                })
                return;
            } else if(!(name && type)) {
                setNotification({
                    type: 'error',
                    message: this.$t('dashboard.fieldEmpty')
                })
                return;
            }

            this.fields.push({ id: this.fields[this.fields.length-1].id+1, name: name, type: type, description: description });
            this.newField.name = "";
            this.newField.description = "";
            setNotification({
                type: 'success',
                message: this.$t('dashboard.fieldAdded')
            })
        },
        deleteField(id) {
            console.log("Delete field");
            this.fields = this.fields.filter((field) => field.id !== id);
            this.filteredFields = this.filteredFields.filter((field) => field.id !== id);
            setNotification({
                type: 'success',
                message: this.$t('dashboard.fieldRemoved')
            })
        },
    },
};
</script>

<style></style>
