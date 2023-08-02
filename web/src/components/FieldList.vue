<template>
    <form id="form" action="#" @submit="saveName">
        <label for="product-name">Product name:</label>
        <input type="text" name="product-name" :value="product.name" />
        <label for="product-description">Product description:</label>
        <textarea name="product-description" :value="product.description" />
        <button type="submit">{{$t("dashboard.save")}}</button>
    </form>

    <SearchBar @search="searchField" />
    <button @click="save" :disabled="!Object.keys(fieldsBuffer).length">
        {{ `${$t("dashboard.save")} (${Object.keys(fieldsBuffer).length} changes)` }}
    </button>
    <button @click="restore">{{ $t("dashboard.restore") }}</button>
    <table>
        <thead>
            <tr>
                <th>{{ $t("dashboard.fieldName") }}</th>
                <th>{{ $t("dashboard.fieldDisplayName") }}</th>
                <th>{{ $t("dashboard.type") }}</th>
                <th>{{ $t("main.description") }}</th>
                <th>{{ $t("dashboard.isRequired") }}</th>
                <th>{{ $t("dashboard.isFilterable") }}</th>
                <th>{{ $t("dashboard.selectionGroup") }}</th>
                <th>{{ $t("dashboard.remove") }}</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="field in filteredFields" :key="field.name" :id="field.id">
                <td><input type="text" name="name" @change="updateBuffer" :value="field.name"></td>
                <td><input type="text" name="display_name" @change="updateBuffer" :value="field.display_name"></td>
                <td><Selection v-if="$store.state.typesArray" name="type_id" :options="$store.state.typesArray" @select-event="updateBuffer" :selected="field.type_id" /></td>
                <td><input type="text" name="description" @change="updateBuffer" :value="field.description"></td>
                <td><input type="checkbox" name="is_required" @change="updateBuffer" :checked="field.is_required"></td>
                <td><input type="checkbox" name="is_filterable" @change="updateBuffer" :checked="field.is_filterable"></td>
                <td><Selection name="selections_groups_id" :options="$store.state.selectionsGroupsArray" @select-event="updateBuffer" :selected="field.selections_groups_id" /></td>
                <td><button @click="deleteField(field.id)">x</button></td>
            </tr>
            <tr>
                <td>
                    <input type="text" :placeholder="$t('dashboard.addField')" :value="newField.name" @input="inputName" />
                    <Selection v-if="$store.state.fieldsArray" :text="'dashboard.chooseField'" :options="$store.state.fieldsArray" :selected="fieldId" @id-selected="updateNewField" />
                </td>
                <td><input type="text" :placeholder="$t('dashboard.addField')" v-model="newField.display_name" /></td>
                <td><Selection v-if="$store.state.typesArray" :options="$store.state.typesArray" :selected="newField.type_id" @id-selected="updateNewFieldType" /></td>
                <td><input type="text" :placeholder="$t('dashboard.addField')" v-model="newField.description" /></td>
                <td><input type="checkbox" v-model="newField.is_required"></td>
                <td><input type="checkbox" v-model="newField.is_filterable"></td>
                <td><Selection :options="$store.state.selectionsGroupsArray" :selected="newField.selections_groups_id" @id-selected="updateNewFieldSelectionsGroup" /></td>
                <td><button @click="addField">{{ $t("dashboard.addField") }}</button></td>
            </tr>
        </tbody>
    </table>
</template>

<script>
import { headers } from "@/utils/api";

import SearchBar from "@/elements/SearchBar.vue";
import Selection from "@/elements/Selection.vue";

export default {
    name: 'field-list',
    props: {
        productId: {
            type: Number,
            required: true,
        }
    },
    data() {
        return {
            fieldsFetched: {},
            fields: {},
            fieldsBuffer: {},
            filteredFields: {},
            newFieldId: 1,
            newField: {},
            fieldTemplate: {
                name: "",
                display_name: "",
                type_id: 0,
                description: "",
                is_required: false,
                is_filterable: false,
                selections_groups_id: null,
            },
            product: {
                name: "",
                description: "",
            },
            error: null,
            fieldId: null,
        };
    },
    components: {
        SearchBar,
        Selection,
    },
    async created() {
        this.newField = Object.assign({}, this.fieldTemplate);
        this.$store.dispatch("fetchTypes");
        this.$store.dispatch("fetchFieldsArray");
        this.$store.dispatch("fetchSelectionsGroupsArray");
        let fetchedFields = await this.$store.dispatch("fetchProductFields", this.productId);

        let f = {};
        this.$store.state.productsFields[`${this.productId}`].forEach((field) => {
            f[field.id] = field;
        });

        // Deep copy of the object
        this.fieldsFetched = JSON.parse(JSON.stringify(f));
        this.fields = JSON.parse(JSON.stringify(f));
        this.filteredFields = JSON.parse(JSON.stringify(f));

        const nothing = await this.$store.dispatch("fetchProducts");
        this.product = this.$store.getters.getProductById(this.productId);
    },
    methods: {
        inputName(e) {
            const newValue = e.target.value;
            if(this.newField.display_name == this.newField.name) {
                this.newField.display_name = newValue;
            }
            this.newField.name = newValue;
        },
        saveName(e) {
            e.preventDefault(); // prevent the form from submitting
            let data = {
                "name": e.target["product-name"].value,
                "description": e.target["product-description"].value,
            };
            headers().put(`/products/${this.productId}`, data)
                .then((response) => {
                    this.$notify({
                        type: 'success',
                        text: this.$t('dashboard.changesSaved')
                    })
                })
                .catch((error) => {
                    this.error = error;
                }
            );
        },
        searchField(text) {
            this.filteredFields = Object.keys(this.fields).reduce((filtered, key) => {
                if(this.fields[key].name.toLowerCase().includes(text.toLowerCase())) {
                    filtered[key] = this.fields[key];
                }
                return filtered;
            }, {});
        },
        updateNewField(id) {
            id = parseInt(id);
            this.fieldId = id;
            if (id === 0 || !id) {
                this.newField = Object.assign({}, this.fieldTemplate);
                return;
            }
            this.newField = this.$store.state.fieldsArray.find((field) => field.id === id);
        },
        updateNewFieldType(id) {
            this.newField.type_id = parseInt(id);
        },
        updateNewFieldSelectionsGroup(id) {
            this.newField.selections_groups_id = parseInt(id);
        },
        addField(ev) {
            const id = this.fieldId ? this.fieldId : `new${this.newFieldId}`;
            let newField = Object.assign({}, this.newField);
            newField.id = id;
            newField.type = "add";
            this.fieldsBuffer[id] = newField;
            this.fields[id] = newField;
            this.filteredFields[id] = newField;
            this.newFieldId += 1;
            this.newField = Object.assign({}, this.fieldTemplate);
        },
        checkDiff(id) {
            let isSame = true;
            for(let key in this.fieldsBuffer[id]) {
                if(key==="type") continue;
                if(this.fieldsBuffer[id][key] !== this.fieldsFetched[id][key]) {
                    isSame = false;
                }
            }
            if(isSame) {
                delete this.fieldsBuffer[id];
            }
        },
        setFieldValue(id, field, value) {
            if(!this.fieldsBuffer[id]) {
                this.fieldsBuffer[id] = {};
            }
            this.fieldsBuffer[id][field] = value;
            this.fields[id][field] = value;
            this.filteredFields[id][field] = value;

            this.fieldsBuffer[id].type = "update";
        },
        updateBuffer(e) {
            const value = e.target.type==="checkbox" ? e.target.checked : e.target.value;
            const field = e.target.name;
            const id = e.target.parentElement.parentElement.id;

            this.setFieldValue(id, field, value);

            this.checkDiff(id);
        },
        deleteField(id) {
            delete this.fieldsBuffer[id];
            delete this.fields[id];
            delete this.filteredFields[id];
            if(typeof(id)==="number") {
                this.fieldsBuffer[id] = {type: "delete"};
            }
        },
        save(ev) {
            const data = {
                "product_id": this.productId,
                "changes": this.fieldsBuffer,
                "force": false
            };
            headers().post(`/fields/details`, data)
                .then((response) => {
                    this.fieldsBuffer = {};
                    this.fieldsFetched = JSON.parse(JSON.stringify(this.fields));
                    this.$notify({
                        type: 'success',
                        text: this.$t('dashboard.changesSaved')
                    })
                })
                .catch((error) => {
                    this.error = error;
                }
            );
        },
        restore(ev) {
            this.fields = JSON.parse(JSON.stringify(this.fieldsFetched));
            this.filteredFields = JSON.parse(JSON.stringify(this.fieldsFetched));
            this.fieldsBuffer = {};
            this.$notify({
                type: 'success',
                text: this.$t('dashboard.changesCancelled')
            })
        },
    },
};
</script>

<style></style>
