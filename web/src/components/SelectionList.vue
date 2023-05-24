<template>
    <section>
        <label for="SelectionsGroups-name">Group name:</label>
        <input type="text" name="SelectionsGroups-name" :value="SelectionsGroups.name" />
        <label for="SelectionsGroups-description">Group description:</label>
        <textarea name="SelectionsGroups-description" :value="SelectionsGroups.description" />
    </section>

    <SearchBar @search="searchSelection" />
    <button @click="saveSelectionsGroup">{{ $t("dashboard.save") }}</button>
    <button @click="restoreSelectionsGroup">{{ $t("dashboard.restore") }}</button>
    <table>
        <thead>
            <tr>
                <th>{{ $t("dashboard.selectionName") }}</th>
                <th>{{ $t("dashboard.type") }}</th>
                <th>{{ $t("main.description") }}</th>
                <th>{{ $t("dashboard.isRequired") }}</th>
                <th>{{ $t("dashboard.isFilterable") }}</th>
                <th>{{ $t("dashboard.selectionGroup") }}</th>
                <th>{{ $t("dashboard.remove") }}</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="selection in filteredSelections" :key="selection.name">
                <td><input type="text" :value="selection.name"></td>
                <td><input type="text" :value="selection.description"></td>
                <td><button @click="deleteSelection(selection.id)">x</button></td>
            </tr>
            <tr>
                <td><input type="text" :placeholder="$t('dashboard.addSelection')" v-model="newSelection.name" /></td>
                <td><input type="text" :placeholder="$t('dashboard.addSelection')" v-model="newSelection.description" /></td>
                <td><button @click="addSelection">{{ $t("dashboard.addSelection") }}</button></td>
            </tr>
        </tbody>
    </table>
</template>

<script>
import { headers } from "@/api";
import SearchBar from "@/components/SearchBar.vue";
import Selection from "@/components/Selection.vue";

export default {
    name: 'selection-list',
    props: {
        SelectionsGroups: {
            type: Object,
            default: {},
        }
    },
    data() {
        return {
            selections: [],
            selectionsBuffer: [],
            filteredSelections: [],
            newSelection: {},
            selectionTemplate: {
                name: "",
                description: "",
            },
            error: null,
            selectionId: null,
        };
    },
    components: {
        SearchBar,
        Selection,
    },
    created() {
        console.log(this.SelectionsGroups)
        this.newSelection = Object.assign({}, this.selectionTemplate);
        this.fetchData();
    },
    methods: {
    },
};
</script>

<style></style>
