<template>
    <section class="int-filter">
        <span>{{ name }} : </span>
        <label :for="`from-${id}`">{{ $t("main.from") }}</label>
        <input type="number" :name="`from-${id}`" v-model="intFrom" @change="intChange">
        <a @click="reset">x</a>

        <label :for="`to-${id}`">{{ $t("main.to") }}</label>
        <input type="number" :name="`to-${id}`" v-model="intTo" @change="intChange">
        <a @click="reset">x</a>
    </section>
</template>

<script>
export default {
    name: 'int-filter',
    props: {
        id: Number,
        name: String,
    },
    data() {
        return {
            intFrom: -Infinity,
            intTo: Infinity,
        };
    },
    methods: {
        intChange() {
            this.$emit('intFilterChange', this.intFrom, this.intTo, this.id);
        },
        reset() {
            this.intFrom = -Infinity;
            this.intTo = Infinity;
            this.$emit('intFilterChange', this.intFrom, this.intTo, this.id);
        }
    },
};
</script>

<style></style>
