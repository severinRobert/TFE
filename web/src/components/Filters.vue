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
                <p v-else>{{ field.display_name }}</p>
            </template>
        </template>
    </div>
</template>

<script>
import StringFilter from "@/elements/StringFilter.vue";
import IntFilter from "@/elements/IntFilter.vue";

export default {
    name: 'filters',
    props: {
        fields: Array,
        arrayToFilter: Array,
    },
    emits: ['filtered'],
    data() {
        return {
            arrayFiltered: [],
        };
    },
    components: {
        StringFilter,
        IntFilter,
    },
    methods: {
        sendArrayFiltered() {
            this.$emit('filtered', this.arrayFiltered);
        },
        stringFilterChange(stringValue, id) {
            this.arrayFiltered = this.arrayToFilter.filter((e) => {
                return e.fields[id].includes(stringValue);
            });
            this.sendArrayFiltered();
        },
        intFilterChange(intFrom, intTo, id) {
            console.log(intFrom, intTo, id)
            console.log(this.arrayToFilter)
            this.arrayFiltered = this.arrayToFilter.filter((e) => {
                return e.fields[id] >= intFrom && e.fields[id] <= intTo;
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
