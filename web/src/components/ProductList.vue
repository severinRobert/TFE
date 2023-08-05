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
            <template v-if="filteredProducts.length === 0">
                <tr role=button class="clickable" v-for="product in $store.state.products" :key="product.id">
                    <td @click="clickProduct(product)">{{ product.name }}</td>
                    <td @click="clickProduct(product)">{{ product.description }}</td>
                    <td><button @click="deleteProduct(product.id)">x</button></td>
                </tr>
            </template>
            <template v-else>
                <tr role=button class="clickable" v-for="product in filteredProducts" :key="product.id">
                    <td @click="clickProduct(product)">{{ product.name }}</td>
                    <td @click="clickProduct(product)">{{ product.description }}</td>
                    <td><button @click="deleteProduct(product.id)">x</button></td>
                </tr>
            </template>
            <tr>
                <td><input type="text" :placeholder="$t('dashboard.addProduct')" v-model="newProduct.name" /></td>
                <td><input type="text" :placeholder="$t('dashboard.addProduct')" v-model="newProduct.description" /></td>
                <td><button class="validation" @click="addProduct">{{ $t("dashboard.addProduct") }}</button></td>
            </tr>
        </tbody>
    </table>
</template>

<script>
import { headers } from "@/utils/api";
import SearchBar from "@/elements/SearchBar.vue";

export default {
    name: 'product-list',
    components: {
        SearchBar,
    },
    created() {
        this.$store.dispatch("fetchProducts");
        this.filteredProducts = this.$store.state.products;
    },
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
            this.filteredProducts = this.$store.state.products.filter((product) => {
                return product.name.toLowerCase().includes(text.toLowerCase());
            });
        },
        clickProduct(product) {
            this.$router.push({'path': '/dashboard/product/' + product.id})
        },
        deleteProduct(id) {
            headers().delete("/products/" + id).then((response) => {
                if(response.status === 204) {
                    this.$notify({
                        type: 'success',
                        text: this.$t('dashboard.productDeleted')
                    });
                    this.$store.commit("deleteProduct", id);
                } else {
                    this.$notify({
                        type: 'error',
                        text: this.$t('dashboard.productError')
                    });
                }
            }).catch((error) => {
                this.$notify({
                    type: 'error',
                    text: `${error} "${error.response.data["detail"]}"`
                });
                if(error.response.data["detail"] == "Product is linked to offers") {
                    const productName = this.$store.getters.getProductById(id).name;
                    const promptValue = prompt(this.$t('dashboard.productDeletePrompt', {productName: productName}));
                    if(promptValue === productName) {
                        headers().delete("/products/" + id + "?force=true").then((response) => {
                            if(response.status === 204) {
                                this.$notify({
                                    type: 'success',
                                    text: this.$t('dashboard.productDeleted')
                                });
                                this.$store.commit("deleteProduct", id);
                            } else {
                                this.$notify({
                                    type: 'error',
                                    text: this.$t('dashboard.productError')
                                });
                            }
                        }).catch((error) => {
                            this.$notify({
                                type: 'error',
                                text: `${error} "${error.response.data["detail"]}"`
                            });
                        });
                    } else {
                        this.$notify({
                            type: 'success',
                            text: this.$t('dashboard.productDeleteCancelled')
                        });
                    }
                }
            });
        },
        addProduct(ev) {
            const name = this.newProduct.name;
            const description = this.newProduct.description;

            if(this.$store.state.products.find((product) => product.name === name)) {
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
                this.$store.state.products.push(response.data);
                this.newProduct.name = "";
                this.newProduct.description = "";
                this.$notify({
                    type: 'success',
                    text: this.$t('dashboard.productAdded')
                })
            }).catch((error) => {
                this.$notify({
                    type: 'error',
                    text: `${error} "${error.response.data["detail"]}"`
                });
            });
        },
    },
};
</script>

<style></style>
