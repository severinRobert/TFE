<template>
    <div class="int-filter">
        <span>{{ name }} : </span>
        <label :for="`from-${id}`">{{ $t("main.from") }}</label>
        <input type="number" class="number-input" :name="`from-${id}`" v-model="intFrom" @change="intChange">
        <a class="reset-button" @click="resetFrom">x</a>

        <label class="littleSpaceLeft" :for="`to-${id}`">{{ $t("main.to") }}</label>
        <input type="number" class="number-input" :name="`to-${id}`" v-model="intTo" @change="intChange">
        <a class="reset-button" @click="resetTo">x</a>
    </div>
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
        resetFrom() {
            this.intFrom = -Infinity;
            this.$emit('intFilterChange', this.intFrom, this.intTo, this.id);
        },
        resetTo() {
            this.intTo = Infinity;
            this.$emit('intFilterChange', this.intFrom, this.intTo, this.id);
        },
    },
};
</script>

<style>
.number-input {
    width: 5rem;
    text-align: center;
}
.reset-button {
    border: 1px solid black;
}
</style>
