<template>
    <div class="selection-filter">
        <label>{{ name }} : </label>
        <Selection
            text="main.notFiltered"
            :options="options"
            :selected="selected"
            @id-selected="addSelection" 
        />
        <span id="options-selected">
            <span class="option-selected" v-for="(id, name) in selectionsSelected" :key="id">
                {{ name }}
                <a class="reset-button" @click="deleteSelection(name)">x</a>
            </span>
        </span>

    </div>
</template>

<script>
import Selection from "@/elements/Selection.vue";

export default {
    name: 'selection-filter',
    props: {
        id: Number,
        name: String,
        options: Array,
    },
    components: {
        Selection,
    },
    data() {
        return {
            selectionsSelected: {},
            selected: 0,
        };
    },
    methods: {
        emitSelectionsSelected() {
            this.$emit('selectionFilterChange', this.selectionsSelected, this.id);
        },
        addSelection(id) {
            if(id == 0) {
                this.selectionsSelected = {};
            } else {
                let name = this.options.find((e) => e.id == id).name;
                this.selectionsSelected[name] = id;
            }
            this.emitSelectionsSelected();
        },
        deleteSelection(value) {
            delete this.selectionsSelected[value];
            this.emitSelectionsSelected();
        },
    },
};
</script>

<style>
#options-selected {
    border: 1px solid black;
    min-width: 5rem;
    padding: 0.2rem;
}
.option-selected {
    margin: 0.2rem 1rem;
}
</style>
