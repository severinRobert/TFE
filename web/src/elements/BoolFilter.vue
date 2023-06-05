<template>
    <div class="bool-filter">
        <label :for="name">{{ name }}</label>
        <Selection :options="options" @id-selected="optionSelected" />
    </div>
</template>

<script>
import Selection from "@/elements/Selection.vue";

export default {
    name: 'bool-filter',
    props: {
        id: Number,
        name: String,
    },
    components: {
        Selection,
    },
    data() {
        return {
            options: [
                {id: 1, name: this.$t('main.no')}, 
                {id: 2, name: this.$t('main.yes')},
            ],
            translate: {
                0: null,
                1: false,
                2: true,
            },
        };
    },
    methods: {
        optionSelected(id) {
            this.$emit('boolFilterChange', this.translate[`${id}`], this.id);
        },
    },
};
</script>

<style>
.number-input {
    width: 5rem;
    text-align: center;
}
.reset-button {
    border: 1px solid black;
}
</style>
