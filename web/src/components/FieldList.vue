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
                <th>{{ $t("dashboard.isRequired") }}</th>
                <th>{{ $t("dashboard.isFilterable") }}</th>
                <th>{{ $t("dashboard.selectionGroup") }}</th>
                <th>{{ $t("dashboard.remove") }}</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="field in filteredFields" :key="field.name">
                <td><input type="text" :value="field.name"></td>
                <td><Selection :options="types" :selected="field.type_id" /></td>
                <td><input type="text" :value="field.description"></td>
                <td><input type="checkbox" :checked="field.is_required"></td>
                <td><input type="checkbox" :checked="field.is_filterable"></td>
                <td><input type="number" :value="field.selections_group_id"></td>
                <td><button @click="deleteField(field.id)">x</button></td>
            </tr>
            <tr>
                <td><AutocompletionSelect :options="ACFieldName" :id="ACId" :value="ACValue" /></td>
                <td><Selection :options="types" :selected="newField.type_id" /></td>
                <td><input type="text" :placeholder="$t('dashboard.addField')" v-model="newField.description" /></td>
                <td><input type="checkbox" :checked="newField.is_required"></td>
                <td><input type="checkbox" :checked="newField.is_filterable"></td>
                <td><input type="number" :value="newField.selections_group_id"></td>
                <td><button @click="addField">{{ $t("dashboard.addField") }}</button></td>
            </tr>
        </tbody>
    </table>
</template>

<script>
import api from "@/api";
import SearchBar from "@/components/SearchBar.vue";
import AutocompletionSelect from "@/components/AutocompletionSelect.vue";
import Selection from "@/components/Selection.vue";
import { useNotificationStore } from '@dafcoe/vue-notification';
const { setNotification } = useNotificationStore();

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
                is_required: false,
                is_filterable: false,
                type_id: null,
                selections_group_id: null,
            },
            types: [],
            error: null,
            ACFieldName: [],
            ACId: null,
            ACValue: "",
        };
    },
    components: {
        SearchBar,
        Selection,
        AutocompletionSelect,
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
            api.get(`/products/${this.$route.params.id}/fields`).then((response) => {
                this.fields = response.data;
                this.filteredFields = response.data;
                console.log(this.fields)
            }).catch((error) => {
                error = error;
            });
            api.get("/types").then((response) => {
                this.types = response.data;
            }).catch((error) => {
                error = error;
            });
            api.get("/fields").then((response) => {
                this.ACFieldName = response.data.map((field) => { return {'id': field.id, 'label': field.name} } );
            }).catch((error) => {
                error = error;
            });
        },
        addField(ev) {
            console.log("Add field");
            console.log(this.newField)
            const name = this.newField.name;
            const type_id = Number(ev.target.parentElement.parentElement.children[1].children[0].value);
            const description = this.newField.description;

            console.log(name, type_id, description)

            if(this.fields.find((field) => field.name === name)) {
                setNotification({
                    type: 'error',
                    message: this.$t('dashboard.fieldExists')
                })
                return;
            } else if(!(name && type_id)) {
                setNotification({
                    type: 'error',
                    message: this.$t('dashboard.fieldEmpty')
                })
                return;
            }

            api.post("/fields", {
                name: name,
                description: description,
                is_required: this.newField.is_required,
                is_filterable: this.newField.is_filterable,
                type_id: type_id,
                selections_group_id: null,
            }).then((fieldResponse) => {
                console.log("add field success")
                api.post(`/product_fields`, {
                    field_id: fieldResponse.data.id,
                    product_id: this.product.id,
                }).then((response) => {
                    console.log("add field to product success")
                    this.fields.push(fieldResponse.data);
                    this.filteredFields.push(fieldResponse.data);
                    setNotification({
                        type: 'success',
                        message: this.$t('dashboard.fieldAdded')
                    })
                }).catch((error) => {
                    error = error;
                    setNotification({
                        type: 'error',
                        message: this.$t('dashboard.fieldNotAdded')
                    })
                });
            }).catch((error) => {
                error = error;
                setNotification({
                    type: 'error',
                    message: this.$t('dashboard.fieldNotAdded')
                })
            });
        },
        deleteField(id) {
            api.get(`/product_fields/product/${this.product.id}/field/${id}`).then((response) => {
                api.delete(`/product_fields/${response.data.id}`).then((response) => {
                    console.log("delete field from product success")
                    this.fields = this.fields.filter((field) => field.id !== id);
                    this.filteredFields = this.filteredFields.filter((field) => field.id !== id);
                    setNotification({
                        type: 'success',
                        message: this.$t('dashboard.fieldDeleted')
                    })
                }).catch((error) => {
                    error = error;
                    setNotification({
                        type: 'error',
                        message: this.$t('dashboard.fieldNotDeleted')
                    })
                });
            }).catch((error) => {
                error = error;
                setNotification({
                    type: 'error',
                    message: this.$t('dashboard.fieldNotDeleted')
                })
            });
        },
    },
};
</script>

<style></style>
