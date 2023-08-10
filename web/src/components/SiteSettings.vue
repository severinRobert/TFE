<template>
    <div id="colors">
        <h2>{{ $t("dashboard.siteSettings") }}</h2>
        <form>
            <label for="title">{{ $t("dashboard.siteTitle") }}</label>
            <input type="text" name="title" id="title" v-model="$store.state.title" @change="$store.dispatch('activeSettings')">
            <label for="homeDescription">{{ $t("dashboard.homeDescription") }}</label>
            <textarea name="homeDescription" id="homeDescription" cols="30" rows="10" v-model="$store.state.homeDescription"></textarea>
            <button @click.prevent="save">{{ $t("dashboard.save") }}</button>
        </form>
    </div>
</template>

<script>

export default {
    name: 'site-settings',
    methods: {
        async save() {
            const error = await this.$store.dispatch('saveSettings');
            console.log(error)
            if(error) {
                this.$notify({
                    type: 'error',
                    text: error
                })
            } else {
                this.$notify({
                    type: 'success',
                    text: this.$t("dashboard.settingsSaved")
                })
            }
        },
    }
};
</script>

<style>
</style>
