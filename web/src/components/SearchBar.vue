<template>
    <section>
        <input type="text" v-model="searchValue" @change="search" :placeholder="$t(placeholderText)">
        <a @click="reset">x</a>
        <button @click="search">{{ $t("main.search") }}</button>
    </section>
</template>

<script>
export default {
    name: 'search-bar',
    props: {
            placeholderText: {
                type: String,
                default: "main.searchbar"
            }
        },
    data() {
        return {
            searchValue: '',
        };
    },
    methods: {
        search() {
            this.$emit('search', this.searchValue);
        },
        reset() {
            this.searchValue = '';
            this.$emit('search', this.searchValue);
        }
    },
};
</script>

<style></style>
