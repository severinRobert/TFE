<template>
    <section class="content">
        <h1> {{ $t("main.addOffer") }} </h1>
        <form id="form" action="#" @submit="submit">
            <fieldset>
                <legend> 
                    <Selection
                        text="form.chooseProduct"
                        :options="$store.state.products"
                        :selected="productId"
                        @id-selected="selectProduct"
                    />
                </legend>
                <div v-for="field in $store.state.productsFields[`${productId}`]">
                    <label :for="field.name">{{ field.display_name }}</label>
                    <Selection
                        v-if="$store.state.typesObject[field.type_id]=='selection'"
                        text="main.notSelected"
                        :options="$store.state.selectionsGroups[field.selections_groups_id]"
                        :name="field.id"
                        :id="field.name"
                    />
                    <input v-else :type="typeToInput[$store.state.typesObject[field.type_id]]" :step="$store.state.typesObject[field.type_id]=='float' ? 0.01 : None" 
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
import { headers } from "@/utils/api";
import Selection from "@/elements/Selection.vue";

export default {
    name: 'form-view',
    components: {
        Selection,
    },
    data() {
        return {
            productId: 0,
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
        this.$store.dispatch('fetchProducts');
        this.$store.dispatch('fetchTypes');
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
        selectProduct(id) {
            this.productId = parseInt(id);
            this.$store.dispatch('fetchFields', this.productId);
        },
    },
};
</script>

<style>
</style>
