<template>
    <div class="bool-filter">
        <label :for="name">{{ display_name }}</label>
        <Selection
            :name="id.toString()"
            :text="text"
            :options="options"
            @id-selected="optionSelected" 
        />
    </div>
</template>

<script>
import Selection from "@/elements/Selection.vue";

export default {
    name: 'bool-filter',
    props: {
        id: Number,
        name: String,
        display_name: String,
        text: {
            type: String,
            default: "main.notFiltered",
        },
    },
    components: {
        Selection,
    },
    data() {
        return {
            options: [
                {id: 0, name: this.$t('main.no')}, 
                {id: 1, name: this.$t('main.yes')},
            ],
            translate: {
                "": null,
                "0": false,
                "1": true,
            },
        };
    },
    methods: {
        optionSelected(id) {
            let value = this.translate[id];
            this.$emit('boolFilterChange', value, this.id);
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
