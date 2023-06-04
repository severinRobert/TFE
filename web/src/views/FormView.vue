<template>
    <section class="content">
        <h1> {{ $t("main.addOffer") }} </h1>
        <form id="form" action="#" @submit="submit">
            <fieldset>
                <legend> 
                    <Selection :options="products" :selected="productId" @id-selected="selectProduct" text="form.chooseProduct" />
                </legend>
                <div v-for="field in productFields[`${productId}`]">
                    <label :for="field.name">{{ field.display_name }}</label>
                    <Selection v-if="types[field.type_id]=='selection'" :options="selectionsGroups[field.selections_groups_id]" :name="field.id" :id="field.name" />
                    <input v-else :type="typeToInput[types[field.type_id]]" :step="types[field.type_id]=='float' ? 0.01 : None" 
                        :name="field.id" :id="field.name" :required="field.is_required"
                    />
                </div>
                <p v-if="productId==0">Please select a product</p>
                <button type="submit">{{ $t("main.submit") }}</button>
            </fieldset>
        </form>
    </section>
</template>

<script>
import { headers } from "@/api";
import Selection from "@/elements/Selection.vue";

export default {
    name: 'form-view',
    components: {
        Selection,
    },
    data() {
        return {
            products: [],
            productId: 0,
            productFields: {},
            selectionsGroups: {},
            types: {},
            typeToInput: {
                'int' : 'number',
                'string' : 'text',
                'float' : 'number',
                'bool' : 'checkbox',
                'date' : 'date',
                'time' : 'time',
                'datetime' : 'datetime-local',
                'selection' : 'Selection',
                'multiselection' : 'MultiSelection',
                'file' : 'file',
                'image' : 'file',
                'video' : 'file',
                'audio' : 'file',
                'url' : 'url',
                'email' : 'email',
                'phone' : 'tel',
                'address' : 'Address',
                'color' : 'color',
            },
        };
    },
    created() {
        this.fetchProducts();
        this.fetchTypes();
    },
    methods: {
        submit(e) {
            e.preventDefault(); // prevent the form from submitting 
            let formData = new FormData(document.getElementById("form"));
            let offer = {
                "id": 2,
                "owner_id": localStorage.getItem('user_id'),
                "product_id": this.productId,
                "fields": formData
            }
            console.log("offer", offer)
            headers().post(`/offers/details`, formData).then((response) => {
                console.log(response);
            }).catch((error) => {
                this.error = error;
            });
        },
        fetchProducts() {
            headers().get("/products").then((response) => {
                this.products = response.data;
            });
        },
        fetchTypes() {
            headers().get("/types").then((response) => {
                this.types = response.data.reduce((types, type) => {
                    types[type.id] = type.name;
                    return types;
                }, {});
            });
        },
        fetchFields() {
            console.log("Fetch fields");
            headers().get(`/products/${this.productId}/fields`).then((response) => {
                console.log("fields : ", response.data);
                this.productFields[`${this.productId}`] = response.data;
                for(let field of response.data) {
                    console.log(field);
                    console.log(field.selections_groups_id);
                    if(field.selections_groups_id && !this.selectionsGroups[`${field.selections_groups_id}`]) {
                        this.fetchSelections(field.selections_groups_id);
                    }
                }
            }).catch((error) => {
                this.error = error;
            });
        },
        fetchSelections(id) {
            headers().get(`/selections_groups/${id}/selections`).then((response) => {
                console.log("selections : ", response.data)
                this.selectionsGroups[`${id}`] = response.data;
            }).catch((error) => {
                this.error = error;
            });
        },
        selectProduct(id) {
            this.productId = parseInt(id);
            if(this.productFields[id]) {
                this.createFields();
                return;
            }
            this.fetchFields();
        },
    },
};
</script>

<style>
</style>
