<template>
    <div id="colors">
        <h2>{{ $t("dashboard.siteColors") }}</h2>
        <table>
            <thead>
                <tr>
                    <th>{{ $t("dashboard.colorName") }}</th>
                    <th>{{ $t("dashboard.colorValueLight") }}</th>
                    <th>{{ $t("dashboard.colorValueDark") }}</th>
                    <th>{{ $t("dashboard.save") }}</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="[id, color] in Object.entries($store.state.colors)" :id="id" :key="color.name">
                    <td><label :for="`color-${color.name}`">{{ color.name }}</label></td>
                    <td><input type="color" :name="`color-${color.name}`" theme="value" :value="color.value" @change="setColor"></td>
                    <td><input type="color" :name="`color-${color.name}`" theme="value_dark" :value="color.value_dark" @change="setColor"></td>
                    <td><button @click="save(id)">{{ $t("dashboard.save") }}</button></td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>

export default {
    name: 'site-colors',
    methods: {
        setColor(e) {
            console.log(e)
            const id = e.target.parentElement.parentElement.id;
            const theme = e.target.getAttribute('theme');
            const color = e.target.value;
            this.$store.commit('setColor', { 'id': id, 'theme': theme, 'color': color });
            this.$store.dispatch('activeColors');
        },
        async save(id) {
            const error = await this.$store.dispatch('saveColor', id);
            console.log(error)
            if(error) {
                this.$notify({
                    type: 'error',
                    text: error
                })
            } else {
                this.$notify({
                    type: 'success',
                    text: this.$t("dashboard.colorsSaved")
                })
            }
        },
    }
};
</script>

<style>
</style>
