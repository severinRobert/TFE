<template>
    <section>
        <label for="SelectionsGroups-name">Group name:</label>
        <input type="text" name="SelectionsGroups-name" :value="selectionsGroup.name" />
        <label for="SelectionsGroups-description">Group description:</label>
        <textarea name="SelectionsGroups-description" :value="selectionsGroup.description" />
    </section>

    <SearchBar @search="searchSelection" />
    <button @click="save" :disabled="!Object.keys(selectionsBuffer).length">
        {{ `${$t("dashboard.save")} (${Object.keys(selectionsBuffer).length} changes)` }}
    </button>
    <button @click="restore">{{ $t("dashboard.restore") }}</button>
    <table>
        <thead>
            <tr>
                <th>{{ $t("dashboard.selectionName") }}</th>
                <th>{{ $t("main.description") }}</th>
                <th>{{ $t("dashboard.remove") }}</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="selection in filteredSelections" :key="selection.name">
                <td><input type="text" name="name" :id="selection.id" @change="updateBuffer" :value="selection.name"></td>
                <td><input type="text" name="description" :id="selection.id" @change="updateBuffer" :value="selection.description"></td>
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
import { headers } from "@/utils/api";
import SearchBar from "@/elements/SearchBar.vue";
import Selection from "@/elements/Selection.vue";

export default {
    name: 'selection-list',
    props: {
        selectionsGroupId: {
            type: Number,
            required: true,
        },
    },
    data() {
        return {
            selectionsFetched: {},
            selections: {},
            selectionsBuffer: {},
            filteredSelections: {},
            newSelection: {},
            selectionTemplate: {
                name: "",
                description: "",
            },
            selectionsGroup: {
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
    async created() {
        console.log("SelectionList created")
        let fetchedSelections = await this.$store.dispatch("fetchSelections", this.selectionsGroupId);

        let s = {};
        this.$store.state.selectionsGroups[`${this.selectionsGroupId}`].forEach((selection) => {
            s[selection.id] = selection;
        });

        this.selectionsFetched = Object.assign({}, s);
        this.selections = Object.assign({}, s);
        this.filteredSelections = Object.assign({}, s);

        let nothing = await this.$store.dispatch("fetchSelectionsGroupsArray");
        console.log("after fetchSelectionsGroupsArray")
        this.selectionsGroup = this.$store.getters.selectionsGroupById(this.selectionsGroupId);
        console.log(this.selectionsGroup);
    },
    methods: {
        searchSelection(text) {
            console.log(text);
            this.filteredSelections = Object.keys(this.selections).reduce((filtered, key) => {
                if(this.selections[key].name.toLowerCase().includes(text.toLowerCase())) {
                    filtered[key] = this.selections[key];
                }
                return filtered;
            }, {});
        },
        addSelection() {
            this.$store.dispatch("addSelection", {
                selectionsGroupId: this.selectionsGroupId,
                selection: this.newSelection,
            });
            this.newSelection = { ...this.selectionTemplate };
        },
        updateBuffer(e, type="update") {
            const value = e.target.value;
            const field = e.target.name;
            const id = e.target.id;

            if(!this.selectionsBuffer[id]) {
                this.selectionsBuffer[id] = {};
            }
            console.log("this.selectionsFetched[id]", this.selectionsFetched[id])
            console.log("this.selections[id]", this.selections[id])
            console.log("this.filteredSelections[id]", this.filteredSelections[id])
            console.log("this.selectionsBuffer[id]", this.selectionsBuffer[id])

            this.selectionsBuffer[id][field] = value;
            this.selections[id][field] = value;
            this.filteredSelections[id][field] = value;
            console.log(this.selectionsFetched[id])

            this.selectionsBuffer[id].type = type;

            let isSame = true;
            for(let key in this.selectionsBuffer[id]) {
                if(key==="type") continue;
                if(this.selectionsBuffer[id][key] !== this.selectionsFetched[id][key]) {
                    isSame = false;
                }
            }
            if(isSame) {
                delete this.selectionsBuffer[id];
            }
            console.log(this.selectionsBuffer);
        },
        deleteSelection(selectionId) {
            this.$store.dispatch("deleteSelection", {
                selectionsGroupId: this.selectionsGroupId,
                selectionId,
            });
        },
        save() {
            this.$store.dispatch("saveSelectionsGroup", {
                selectionsGroupId: this.selectionsGroupId,
                selections: this.selections,
            });
        },
        restore() {
            console.log("restore")
            this.selections = Object.assign({}, this.selectionsFetched);
            this.filteredSelections = Object.assign({}, this.selectionsFetched);
            this.selectionsBuffer = {};

        },
    },
};
</script>

<style></style>
