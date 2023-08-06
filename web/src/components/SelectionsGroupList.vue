<template>
    <h2>{{ $t("main.selectionsGroups") }}</h2>
    <SearchBar @search="searchSelectionsGroup" />
    <table>
        <thead>
            <tr>
                <th>{{ $t("dashboard.selectionsGroup") }}</th>
                <th>{{ $t("main.description") }}</th>
                <th>{{ $t("dashboard.remove") }}</th>
            </tr>
        </thead>
        <tbody>
            <template v-if="filteredSelectionsGroups.length === 0">
                <tr class="clickable" v-for="selectionsGroup in $store.state.selectionsGroupsArray" :key="selectionsGroup.id">
                    <td @click="clickSelectionsGroup(selectionsGroup.id)">{{ selectionsGroup.name }}</td>
                    <td @click="clickSelectionsGroup(selectionsGroup.id)">{{ selectionsGroup.description }}</td>
                    <td><button @click="deleteSelectionsGroup(selectionsGroup.id)">x</button></td>
                </tr>
            </template>
            <template v-else>
                <tr class="clickable" v-for="selectionsGroup in filteredSelectionsGroups" :key="selectionsGroup.id">
                    <td @click="clickSelectionsGroup(selectionsGroup.id)">{{ selectionsGroup.name }}</td>
                    <td @click="clickSelectionsGroup(selectionsGroup.id)">{{ selectionsGroup.description }}</td>
                    <td><button @click="deleteSelectionsGroup(selectionsGroup.id)">x</button></td>
                </tr>
            </template>
            <tr>
                <td><input type="text" :placeholder="$t('dashboard.addSelectionsGroup')" v-model="newSelectionsGroup.name" @keyup.enter="addSelectionsGroup" id="newSelectionsGroupName" /></td>
                <td><input type="text" :placeholder="$t('dashboard.addSelectionsGroup')" v-model="newSelectionsGroup.description" @keyup.enter="addSelectionsGroup" /></td>
                <td><button class="validation" @click="addSelectionsGroup">{{ $t("dashboard.addSelectionsGroup") }}</button></td>
            </tr>
        </tbody>
    </table>
</template>

<script>
import { headers } from "@/utils/api";
import SearchBar from "@/elements/SearchBar.vue";

export default {
    name: 'selections-group-list',
    components: {
        SearchBar,
    },
    created() {
        this.$store.dispatch("fetchSelectionsGroupsArray");
        this.filteredSelectionsGroups = this.$store.state.selectionsGroupsArray;
    },
    data() {
        return {
            filteredSelectionsGroups: [],
            newSelectionsGroup: {
                name: "",
                description: "",
            },
        };
    },
    methods: {
        searchSelectionsGroup(text) {
            this.filteredSelectionsGroups = this.$store.state.selectionsGroupsArray.filter((selectionsGroup) => {
                return selectionsGroup.name.toLowerCase().includes(text.toLowerCase());
            });
        },
        clickSelectionsGroup(id) {
            this.$router.push({'path': '/dashboard/selectionsGroup/' + id})
        },
        deleteSelectionsGroup(id) {
            headers().delete("/selections_groups/" + id).then((response) => {
                this.$notify({
                    type: 'success',
                    text: this.$t('dashboard.selectionsGroupDeleted')
                });
                this.$store.state.selectionsGroupsArray = this.$store.state.selectionsGroupsArray.filter((selectionsGroup) => selectionsGroup.id !== id);
            }).catch((error) => {
                this.$notify({
                    type: 'error',
                    text: `${error} "${error.response.data["detail"]}"`
                });
                if(error.response.data["detail"] == "Selection group still has fields") {
                    const selectionsGroupName = this.$store.getters.selectionsGroupById(id).name;
                    const promptValue = prompt(this.$t('dashboard.selectionsGroupDeletePrompt', {selectionsGroupName: selectionsGroupName}));
                    if(promptValue === selectionsGroupName) {
                        headers().delete("/selections_groups/" + id + "?force=true").then((response) => {
                            if(response.status === 204) {
                                this.$notify({
                                    type: 'success',
                                    text: this.$t('dashboard.selectionsGroupDeleted')
                                });
                                this.$store.commit("deleteSelectionsGroup", id);
                            } else {
                                this.$notify({
                                    type: 'error',
                                    text: this.$t('dashboard.productError')
                                });
                            }
                        }).catch((error) => {
                            this.$notify({
                                type: 'error',
                                text: `${error} "${error.response.data["detail"]}"`
                            });
                        });
                    } else {
                        this.$notify({
                            type: 'success',
                            text: this.$t('dashboard.selectionsGroupDeleteCancelled')
                        });
                    }
                }
            });
        },
        addSelectionsGroup(ev) {
            const name = this.newSelectionsGroup.name;
            const description = this.newSelectionsGroup.description;

            if(this.$store.state.selectionsGroupsArray.find((selectionsGroup) => selectionsGroup.name === name)) {
                this.$notify({
                    type: 'error',
                    text: this.$t('dashboard.selectionsGroupExists')
                });
                return;
            } else if(!(name)) {
                this.$notify({
                    type: 'error',
                    text: this.$t('dashboard.selectionsGroupEmpty')
                });
                return;
            }
            headers().post("/selections_groups", {
                name: name,
                description: description,
            }).then((response) => {
                this.$store.state.selectionsGroupsArray.push(response.data);
                this.newSelectionsGroup.name = "";
                this.newSelectionsGroup.description = "";
                this.$notify({
                    type: 'success',
                    text: this.$t('dashboard.selectionsGroupAdded')
                })
            }).catch((error) => {
                this.$notify({
                    type: 'error',
                    text: error
                });
            });
            document.getElementById("newSelectionsGroupName").focus();
        },
    },
};
</script>

<style></style>
