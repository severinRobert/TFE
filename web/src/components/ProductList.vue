<template>
    <h2>{{ $t("main.products") }}</h2>
    <SearchBar @search="searchProduct" />
    <table>
        <thead>
            <tr>
                <th>{{ $t("dashboard.product") }}</th>
                <th>{{ $t("main.description") }}</th>
                <th>{{ $t("dashboard.remove") }}</th>
            </tr>
        </thead>
        <tbody>
            <tr class="clickable" v-for="product in filteredProducts" :key="product.id">
                <td @click="clickProduct(product)">{{ product.name }}</td>
                <td @click="clickProduct(product)">{{ product.description }}</td>
                <td><button @click="deletePrduct(product.id)">x</button></td>
            </tr>
            <tr>
                <td><input type="text" :placeholder="$t('dashboard.addProduct')" v-model="newProduct.name" /></td>
                <td><input type="text" :placeholder="$t('dashboard.addProduct')" v-model="newProduct.description" /></td>
                <td><button @click="addProduct">{{ $t("dashboard.addProduct") }}</button></td>
            </tr>
        </tbody>
    </table>
</template>

<script>
import { headers } from "@/utils/api";
import SearchBar from "@/elements/SearchBar.vue";

export default {
    name: 'product-list',
    props: {
        products: {
            type: Array,
            required: true,
        },
    },
    watch: {
        products: {
            handler: function (newVal) {
                this.filteredProducts = [...newVal];
            },
            deep: true,
        },
    },
    components: {
        SearchBar,
    },
    mounted() {
        this.filteredProducts = [...this.products];
    },
    emits: ['delete-product', 'update:products'],
    data() {
        return {
            filteredProducts: [],
            newProduct: {
                name: "",
                description: "",
            },
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
            this.$router.push({'path': '/dashboard/product/' + product.id})
        },
        deletePrduct(id) {
            headers().delete("/products/" + id).then((response) => {
                console.log(response)
                if(response.status === 204) {
                    this.$notify({
                        type: 'success',
                        text: this.$t('dashboard.productDeleted')
                    });
                    this.$emit("update:products", this.products.filter((product) => product.id !== id));
                } else {
                    this.$notify({
                        type: 'error',
                        text: this.$t('dashboard.productError')
                    });
                }
            }).catch((error) => {
                this.$notify({
                    type: 'error',
                    text: this.$t('dashboard.productError')
                });
            });
        },
        addProduct(ev) {
            const name = this.newProduct.name;
            const description = this.newProduct.description;

            console.log("Add product", name, description)

            if(this.products.find((product) => product.name === name)) {
                this.$notify({
                    type: 'error',
                    text: this.$t('dashboard.productExists')
                });
                return;
            } else if(!(name)) {
                this.$notify({
                    type: 'error',
                    text: this.$t('dashboard.productEmpty')
                });
                return;
            }
            headers().post("/products", {
                name: name,
                description: description,
            }).then((response) => {
                console.log(response)

                this.products.push(response.data);
                this.newProduct.name = "";
                this.newProduct.description = "";
                this.$notify({
                    type: 'success',
                    text: this.$t('dashboard.productAdded')
                })
            }).catch((error) => {
                this.$notify({
                    type: 'error',
                    text: this.$t('dashboard.productError')
                });
            });
        },
    },
};
</script>

<style></style>
