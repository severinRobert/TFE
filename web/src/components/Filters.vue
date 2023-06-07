<template>
    <div id="filters">
        <template v-for="field in fields">
            <template v-if="field.is_filterable">
                <StringFilter 
                    v-if="field.type_id==2"
                    :id="field.id"
                    :name="field.display_name"
                    @stringFilterChange="stringFilterChange"
                />
                <IntFilter 
                    v-else-if="[1,3,6].includes(field.type_id)"
                    :id="field.id"
                    :name="field.display_name"
                    @intFilterChange="intFilterChange"
                />
                <SelectionFilter 
                    v-else-if="[8,9].includes(field.type_id)"
                    :id="field.id"
                    :name="field.display_name"
                    :options="$store.state.selectionsGroups[`${field.selections_groups_id}`]"
                    @selectionFilterChange="selectionFilterChange"
                />
                <BoolFilter 
                    v-else-if="field.type_id==4"
                    :id="field.id"
                    :name="field.name"
                    :display_name="field.display_name"
                    @boolFilterChange="boolFilterChange"
                />
                <ColorFilter 
                    v-else-if="field.type_id==19"
                    :id="field.id"
                    :name="field.display_name"
                    @colorFilterChange="colorFilterChange"
                />
                <p v-else>{{ field.display_name }}</p>
            </template>
        </template>
    </div>
</template>

<script>
import StringFilter from "@/elements/StringFilter.vue";
import IntFilter from "@/elements/IntFilter.vue";
import SelectionFilter from "@/elements/SelectionFilter.vue";
import BoolFilter from "@/elements/BoolFilter.vue";
import ColorFilter from "@/elements/ColorFilter.vue";

export default {
    name: 'filters',
    props: {
        fields: Array,
        arrayToFilter: Array,
    },
    emits: ['filtered'],
    data() {
        return {
            arrayFiltered: this.arrayToFilter,
            filters: {},
        };
    },
    components: {
        StringFilter,
        IntFilter,
        SelectionFilter,
        BoolFilter,
        ColorFilter,
    },
    methods: {
        sendArrayFiltered() {
            let not_to_include = Object.values(this.filters).flat()
            this.arrayFiltered = this.arrayToFilter.filter((e) => {
                return !not_to_include.includes(e.id);
            });
            this.$emit('filtered', this.arrayFiltered);
        },
        stringFilterChange(stringValue, id) {
            // map ids to filter
            this.filters[`${id}`] = this.arrayToFilter.map((e) => {
                if(!e.fields[id].includes(stringValue)) {
                    return e.id;
                }
            });
            this.sendArrayFiltered();
        },
        intFilterChange(intFrom, intTo, id) {
            // map ids to filter
            this.filters[`${id}`] = this.arrayToFilter.map((e) => {
                if(!(e.fields[id] >= intFrom && e.fields[id] <= intTo)) {
                    return e.id;
                }
            });
            this.sendArrayFiltered();
        },
        selectionFilterChange(selections, id) {
            // map ids to filter
            if(Object.keys(selections).length == 0) {
                this.filters[`${id}`] = [];
                this.sendArrayFiltered();
                return;
            }
            this.filters[`${id}`] = this.arrayToFilter.map((e) => {
                if(!(e.fields[id] in selections)) {
                    return e.id;
                }
            });
            
            this.sendArrayFiltered();
        },
        boolFilterChange(bool, id) {
            // map ids to filter
            if(bool == null) {
                this.filters[`${id}`] = [];
                this.sendArrayFiltered();
                return;
            }
            this.filters[`${id}`] = this.arrayToFilter.map((e) => {
                if(!(e.fields[id] == bool)) {
                    return e.id;
                }
            });
            this.sendArrayFiltered();
        },
        ColorFilterChange(color, id) {
            // map ids to filter
            if(color == null) {
                this.filters[`${id}`] = [];
                this.sendArrayFiltered();
                return;
            }
            this.filters[`${id}`] = this.arrayToFilter.map((e) => {
                if(!(e.fields[id] == color)) {
                    return e.id;
                }
            });
            this.sendArrayFiltered();
        },
    },
};
</script>

<style>
#filters {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}
</style>
