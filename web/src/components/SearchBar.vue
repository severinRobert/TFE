<template>
    <section>
        <input type="text" v-model="searchValue" @change="search">
        <button @click="search">{{ $t("main.search") }}</button>
    </section>
</template>

<script>
export default {
    name: 'search-bar',
    data() {
        return {
            searchValue: '',
        };
    },
    methods: {
        search() {
            this.$emit('search', this.searchValue);
        }
    },
};
</script>

<style></style>
