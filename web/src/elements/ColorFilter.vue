<template>
    <div class="color-filter">
        <span>{{ name }} : </span>
        <label :for="`from-${id}`">{{ $t("main.from") }}</label>
        <input type="color" class="color-input" :name="`from-${id}`" v-model="colorFrom" @change="colorChange">
        <a class="reset-button" @click="resetFrom">x</a>

        <label class="littleSpaceLeft" :for="`to-${id}`">{{ $t("main.to") }}</label>
        <input type="color" class="color-input" :name="`to-${id}`" v-model="colorTo" @change="colorChange">
        <a class="reset-button" @click="resetTo">x</a>
    </div>
</template>

<script>
export default {
    name: 'color-filter',
    props: {
        id: Number,
        name: String,
    },
    data() {
        return {
            colorFrom: "#000000",
            colorTo: "#FFFFFF",
        };
    },
    methods: {
        colorChange() {
            this.$emit('colorFilterChange', this.colorFrom, this.colorTo, this.id);
        },
        resetFrom() {
            this.colorFrom = "#000000";
            this.$emit('colorFilterChange', this.colorFrom, this.colorTo, this.id);
        },
        resetTo() {
            this.colorTo = "#FFFFFF";
            this.$emit('colorFilterChange', this.colorFrom, this.colorTo, this.id);
        },
    },
};
</script>

<style>
</style>
