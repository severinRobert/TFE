<template>
    <form id="form" action="#" @submit="saveName">
        <label for="SelectionsGroups-name">Group name:</label>
        <input type="text" name="SelectionsGroups-name" :value="selectionsGroup.name" />
        <label for="SelectionsGroups-description">Group description:</label>
        <textarea name="SelectionsGroups-description" :value="selectionsGroup.description" />
        <button type="submit">{{$t("dashboard.save")}}</button>
    </form>

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
                <td><input type="text" :placeholder="$t('dashboard.addSelection')" v-model="newSelection.name" autofocus /></td>
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
            newSelectionId: 1,
            newSelection: {
                name: "",
                description: "",
            },
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
        const fetchedSelections = await this.$store.dispatch("fetchSelections", this.selectionsGroupId);

        let s = {};
        this.$store.state.selectionsGroups[`${this.selectionsGroupId}`].forEach((selection) => {
            s[selection.id] = selection;
        });

        // Deep copy of the object
        this.selectionsFetched = JSON.parse(JSON.stringify(s));
        this.selections = JSON.parse(JSON.stringify(s));
        this.filteredSelections = JSON.parse(JSON.stringify(s));

        const nothing = await this.$store.dispatch("fetchSelectionsGroupsArray");
        this.selectionsGroup = this.$store.getters.selectionsGroupById(this.selectionsGroupId);
        console.log(this.selectionsGroup);
    },
    methods: {
        saveName(e) {
            e.preventDefault(); // prevent the form from submitting 
            console.log("saveName")
            let data = {
                "name": e.target["SelectionsGroups-name"].value,
                "description": e.target["SelectionsGroups-description"].value,
            };
            headers().put(`/selections_groups/${this.selectionsGroupId}`, data)
                .then((response) => {
                    console.log(response);
                    this.$notify({
                        type: 'success',
                        text: this.$t('dashboard.changesSaved')
                    })
                })
                .catch((error) => {
                    console.log(error);
                    this.error = error;
                }
            );
        },
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
            const id = `new${this.newSelectionId}`;
            let newSelection = Object.assign({}, this.newSelection);
            newSelection.id = id;
            newSelection.type = "add";
            this.selectionsBuffer[id] = newSelection;
            this.selections[id] = newSelection;
            this.filteredSelections[id] = newSelection;
            this.newSelectionId += 1;
            this.newSelection = Object.assign({}, this.selectionTemplate);
            console.log(this.selectionsBuffer);
        },
        updateBuffer(e, type="update") {
            const value = e.target.value;
            const field = e.target.name;
            const id = e.target.id;

            if(!this.selectionsBuffer[id]) {
                this.selectionsBuffer[id] = {};
            }

            console.log(id, field, value)
            console.log(this.selections)

            this.selectionsBuffer[id][field] = value;
            this.selections[id][field] = value;
            this.filteredSelections[id][field] = value;

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
        deleteSelection(id) {
            console.log(id)
            delete this.selectionsBuffer[id];
            delete this.selections[id];
            delete this.filteredSelections[id];
            if(typeof(id)==="number") {
                this.selectionsBuffer[id] = {type: "delete"};
            }
            console.log(this.selectionsBuffer);
        },
        save() {
            console.log("save")
            console.log({"selections_groups_id": this.selectionsGroupId, "changes": this.selectionsBuffer});
            const data = {
                "selections_groups_id": this.selectionsGroupId, 
                "changes": this.selectionsBuffer,
                "force": false
            };
            headers().post(`/selections/details`, data)
                .then((response) => {
                    console.log(response);
                    this.selectionsBuffer = {};
                    this.selectionsFetched = JSON.parse(JSON.stringify(this.selections));
                    this.$notify({
                        type: 'success',
                        text: this.$t('dashboard.changesSaved')
                    })
                })
                .catch((error) => {
                    console.log(error);
                    this.error = error;
                }
            );
        },
        restore() {
            console.log("restore")
            this.selections = JSON.parse(JSON.stringify(this.selectionsFetched));
            this.filteredSelections = JSON.parse(JSON.stringify(this.selectionsFetched));
            this.selectionsBuffer = {};
            this.$notify({
                type: 'success',
                text: this.$t('dashboard.changesCancelled')
            })
        },
    },
};
</script>

<style></style>
