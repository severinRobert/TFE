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
            <tr class="clickable" v-for="selectionsGroup in filteredSelectionsGroups" :key="selectionsGroup.id">
                <td @click="clickSelectionsGroup(selectionsGroup)">{{ selectionsGroup.name }}</td>
                <td @click="clickSelectionsGroup(selectionsGroup)">{{ selectionsGroup.description }}</td>
                <td><button @click="deletePrduct(selectionsGroup.id)">x</button></td>
            </tr>
            <tr>
                <td><input type="text" :placeholder="$t('dashboard.addSelectionsGroup')" v-model="newSelectionsGroup.name" /></td>
                <td><input type="text" :placeholder="$t('dashboard.addSelectionsGroup')" v-model="newSelectionsGroup.description" /></td>
                <td><button @click="addSelectionsGroup">{{ $t("dashboard.addSelectionsGroup") }}</button></td>
            </tr>
        </tbody>
    </table>
</template>

<script>
import { headers } from "@/api";
import SearchBar from "@/elements/SearchBar.vue";

export default {
    name: 'selections-group-list',
    props: {
        selectionsGroups: {
            type: Array,
            required: true,
        },
    },
    watch: {
        selectionsGroups: {
            handler: function (newVal) {
                this.filteredSelectionsGroups = [...newVal];
            },
            deep: true,
        },
    },
    components: {
        SearchBar,
    },
    mounted() {
        this.filteredSelectionsGroups = [...this.selectionsGroups];
    },
    emits: ['delete-selectionsGroup', 'update:selectionsGroups'],
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
            console.log(text);
            this.filteredSelectionsGroups = this.selectionsGroups.filter((selectionsGroup) => {
                return selectionsGroup.name.toLowerCase().includes(text.toLowerCase());
            });
        },
        clickSelectionsGroup(selectionsGroup) {
            this.$router.push({'path': '/dashboard/selectionsGroup/' + selectionsGroup.id})
        },
        deletePrduct(id) {
            headers().delete("/selectionsGroups/" + id).then((response) => {
                console.log(response)
                if(response.status === 204) {
                    this.$notify({
                        type: 'success',
                        text: this.$t('dashboard.selectionsGroupDeleted')
                    });
                    this.$emit("update:selectionsGroups", this.selectionsGroups.filter((selectionsGroup) => selectionsGroup.id !== id));
                } else {
                    this.$notify({
                        type: 'error',
                        text: this.$t('dashboard.selectionsGroupError')
                    });
                }
            }).catch((error) => {
                this.$notify({
                    type: 'error',
                    text: this.$t('dashboard.selectionsGroupError')
                });
            });
        },
        addSelectionsGroup(ev) {
            const name = this.newSelectionsGroup.name;
            const description = this.newSelectionsGroup.description;

            console.log("Add selectionsGroup", name, description)

            if(this.selectionsGroups.find((selectionsGroup) => selectionsGroup.name === name)) {
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
                console.log(response)

                this.selectionsGroups.push(response.data);
                this.newSelectionsGroup.name = "";
                this.newSelectionsGroup.description = "";
                this.$notify({
                    type: 'success',
                    TextTrackCueList: this.$t('dashboard.selectionsGroupAdded')
                })
            }).catch((error) => {
                this.$notify({
                    type: 'error',
                    text: this.$t('dashboard.selectionsGroupError')
                });
            });
        },
    },
};
</script>

<style></style>
