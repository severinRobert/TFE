<template>
    <div id="colors">
        <h2>{{ $t("dashboard.siteSettings") }}</h2>
        <form>
            <button @click.prevent="save">{{ $t("dashboard.save") }}</button><br>
            <label for="title">{{ $t("dashboard.siteTitle") }}</label>
            <input type="text" name="title" id="title" v-model="$store.state.title" @change="$store.dispatch('activeSettings')"><br>
            <label for="homeDescription">{{ $t("dashboard.homeDescription") }}</label><br>
            <textarea class="big" name="homeDescription" id="homeDescription" v-model="$store.state.homeDescription"></textarea>
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
