<template>
    <div class="string-filter">
        <label :for="`string-${id}`">{{ name }}</label>
        <input type="text" :name="`string-${id}`" v-model="stringValue" @change="stringChange" :placeholder="$t(placeholderText)">
        <a @click="reset">x</a>
    </div>
</template>

<script>
export default {
    name: 'string-filter',
    props: {
        id: Number,
        name: String,
        placeholderText: {
            type: String,
            default: 'main.searchbar'
        },
    },
    data() {
        return {
            stringValue: '',
        };
    },
    methods: {
        stringChange() {
            this.$emit('stringFilterChange', this.stringValue, this.id);
        },
        reset() {
            this.stringValue = '';
            this.$emit('stringFilterChange', this.stringValue, this.id);
        }
    },
};
</script>

<style></style>
