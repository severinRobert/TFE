<template>
    <section class="content">
        <h1> Form </h1>
        <form>
            <Selection :options="products" :selected="products[productSelected]" text="form.chooseProduct" />
            
        </form>
    </section>
</template>

<script>
import Selection from "@/components/Selection.vue";

export default {
    name: 'form-view',
    components: {
        Selection,
    },
    created() {
        this.products=[
            { id: 1, name: "Banana", description: "This is a banana" },
            { id: 2, name: "Apple", description: "This is an apple" },
            { id: 3, name: "Orange", description: "This is an orange" },
            { id: 4, name: "Pineapple", description: "This is a pineapple" },
            { id: 5, name: "Strawberry", description: "This is a strawberry" }
        ];
        this.productSelected = 0;
        this.fetchData();
    },
    methods: {
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
    },
};
</script>

<style>
</style>
