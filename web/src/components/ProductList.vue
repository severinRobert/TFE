<template>
    <SearchBar @search="searchProduct" />
    <button @click="clickAdd">{{ $t("dashboard.addProduct") }}</button>
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
import { headers } from "@/api";
import SearchBar from "@/components/SearchBar.vue";
import { useNotificationStore } from '@dafcoe/vue-notification';
const { setNotification } = useNotificationStore();

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
        clickAdd() {
            this.$router.push({'path': '/dashboard/product/new'})
        },
        clickProduct(product) {
            this.$router.push({'path': '/dashboard/product/' + product.id})
        },
        deletePrduct(id) {
            headers().delete("/products/" + id).then((response) => {
                console.log(response)
                if(response.status === 204) {
                    setNotification({
                        type: 'success',
                        message: this.$t('dashboard.productDeleted')
                    });
                    this.$emit("update:products", this.products.filter((product) => product.id !== id));
                } else {
                    setNotification({
                        type: 'error',
                        message: this.$t('dashboard.productError')
                    });
                }
            }).catch((error) => {
                setNotification({
                    type: 'error',
                    message: this.$t('dashboard.productError')
                });
            });
        },
        addProduct(ev) {
            const name = this.newProduct.name;
            const description = this.newProduct.description;

            console.log("Add product", name, description)

            if(this.products.find((product) => product.name === name)) {
                setNotification({
                    type: 'error',
                    message: this.$t('dashboard.productExists')
                });
                return;
            } else if(!(name)) {
                setNotification({
                    type: 'error',
                    message: this.$t('dashboard.productEmpty')
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
                setNotification({
                    type: 'success',
                    message: this.$t('dashboard.productAdded')
                })
            }).catch((error) => {
                setNotification({
                    type: 'error',
                    message: this.$t('dashboard.productError')
                });
            });
        },
    },
};
</script>

<style></style>
