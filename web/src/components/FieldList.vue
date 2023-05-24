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
                <td><Selection :options="selections_groups" :selected="field.selections_groups_id" /></td>
                <td><button @click="deleteField(field.id)">x</button></td>
            </tr>
            <tr>
                <td>
                    <input type="text" :placeholder="$t('dashboard.addField')" v-model="newField.name" />
                    <Selection :text="'dashboard.chooseField'" :options="allFields" :selected="fieldId" @id-selected="updateNewField" />
                </td>
                <td><Selection :options="types" :selected="newField.type_id" @id-selected="updateNewFieldType" /></td>
                <td><input type="text" :placeholder="$t('dashboard.addField')" v-model="newField.description" /></td>
                <td><input type="checkbox" v-model="newField.is_required"></td>
                <td><input type="checkbox" v-model="newField.is_filterable"></td>
                <td><Selection :options="selections_groups" :selected="newField.selections_groups_id" @id-selected="updateNewFieldSelectionsGroup" /></td>
                <td><button @click="addField">{{ $t("dashboard.addField") }}</button></td>
            </tr>
        </tbody>
    </table>
</template>

<script>
import { headers } from "@/api";
import SearchBar from "@/components/SearchBar.vue";
import Selection from "@/components/Selection.vue";

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
            allFields: [],
            fields: [],
            fieldsBuffer: [],
            filteredFields: [],
            newField: {},
            fieldTemplate: {
                name: "",
                type_id: 0,
                description: "",
                is_required: false,
                is_filterable: false,
                selections_group_id: null,
            },
            types: [],
            selections_groups: [],
            error: null,
            fieldId: null,
        };
    },
    components: {
        SearchBar,
        Selection,
    },
    created() {
        this.newField = Object.assign({}, this.fieldTemplate);
        this.fetchData();
    },
    methods: {
        searchField(text) {
            this.filteredFields = this.fieldsBuffer.filter((field) => {
                return field.name.toLowerCase().includes(text.toLowerCase());
            });
        },
        compareFields(a, b) {
            return JSON.stringify(a) === JSON.stringify(b);
        },
        saveProduct(ev) {
            console.log("Save product");
            for(field of this.fieldsBuffer) {
                const fieldInAllFields = this.allFields.find((f) => f.id == field.id);
                // If field is not in fields then  create it 
                if(!fieldInAllFields) {
                    this.createField(field);
                    continue;
                }
                // If field is in fields and 
                if(this.compareFields(field, fieldInFields)) {
                    
                }
            }
        },
        restoreProduct(ev) {
            console.log("Restore product");
            this.fetchData();
        },
        fetchData() {
            console.log("Fetch data");
            headers().get(`/products/${this.$route.params.id}/fields`).then((response) => {
                this.fields = response.data;
                this.fieldsBuffer = response.data;
                this.filteredFields = response.data;
                console.log(response.data);
            }).catch((error) => {
                this.error = error;
            });
            headers().get("/types").then((response) => {
                this.types = response.data;
            }).catch((error) => {
                this.error = error;
            });
            headers().get("/fields").then((response) => {
                this.allFields = response.data;
                this.ACFieldNames = response.data.map((field) => { return {'id': field.id, 'label': field.name} } );
            }).catch((error) => {
                this.error = error;
            });
            headers().get(`/selections_groups`).then((response) => {
                this.selections_groups = response.data;
            }).catch((error) => {
                this.error = error;
            });
        },
        updateNewField(id) {
            console.log("Update new field");
            console.log(id)
            id = parseInt(id);
            this.fieldId = id;
            if (id === 0) {
                this.newField = Object.assign({}, this.fieldTemplate);
                return;
            }
            this.newField = this.allFields.find((field) => field.id === id);
        },
        updateNewFieldType(id) {
            this.newField.type_id = parseInt(id);
        },
        updateNewFieldSelectionsGroup(id) {
            this.newField.selections_group_id = parseInt(id);
        },
        addField(ev) {
            console.log("Add field");
            const newField = this.newField;
            console.log(newField)
            // const row = ev.target.parentElement.parentElement;
            // newField.type_id = Number(row.children[1].children[0].value);

            console.log(newField)
            if(this.fieldsBuffer.find((field) => field.name === newField.name)) {
                this.$notify({
                    type: 'error',
                    text: this.$t('dashboard.fieldExists')
                })
                return;
            } else if(!(newField.name && newField.type_id)) {
                this.$notify({
                    type: 'error',
                    text: this.$t('dashboard.fieldEmpty')
                })
                return;
            }

            if(this.fieldId) {
                console.log("Link field to product", this.fieldId)
                if(this.newField !== this.allFields.find((field) => field.id === this.fieldId)) {
                    console.log("Update field")
                    headers().put(`/fields/${this.fieldId}`, newField).then((fieldResponse) => {
                        console.log("update field success")
                        this.linkFieldToProduct(this.fieldId);
                    }).catch((error) => {
                        this.error = error;
                        this.$notify({
                            type: 'error',
                            text: this.$t('dashboard.fieldNotAdded')
                        })
                    });
                    return;
                }
                this.linkFieldToProduct(this.fieldId);
                return;
            }

            headers().post("/fields", newField).then((fieldResponse) => {
                console.log("add field success")
                this.linkFieldToProduct(fieldResponse.data.id);
            }).catch((error) => {
                this.error = error;
                this.$notify({
                    type: 'error',
                    text: this.$t('dashboard.fieldNotAdded')
                })
            });
        },
        linkFieldToProduct(fieldId) {
            headers().post(`/product_fields`, {
                field_id: fieldId,
                product_id: this.product.id,
            }).then((response) => {
                console.log("add field to product success")
                this.fieldsBuffer.push(this.allFields.find((field) => field.id === fieldId));
                this.filteredFields.push(this.allFields.find((field) => field.id === fieldId));
                this.$notify({
                    type: 'success',
                    text: this.$t('dashboard.fieldAdded')
                })
            }).catch((error) => {
                this.error = error;
                this.$notify({
                    type: 'error',
                    text: this.$t('dashboard.fieldNotAdded')
                })
            });
        },
        deleteField(id) {
            headers().get(`/product_fields/product/${this.product.id}/field/${id}`).then((response) => {
                headers().delete(`/product_fields/${response.data.id}`).then((response) => {
                    console.log("delete field from product success")
                    this.fieldsBuffer = this.fieldsBuffer.filter((field) => field.id !== id);
                    this.filteredFields = this.filteredFields.filter((field) => field.id !== id);
                    this.$notify({
                        type: 'success',
                        text: this.$t('dashboard.fieldDeleted')
                    })
                }).catch((error) => {
                    error = error;
                    this.$notify({
                        type: 'error',
                        text: this.$t('dashboard.fieldNotDeleted')
                    })
                });
            }).catch((error) => {
                error = error;
                this.$notify({
                    type: 'error',
                    text: this.$t('dashboard.fieldNotDeleted')
                })
            });
        },
    },
};
</script>

<style></style>
