<template>
    <select :name="name" @change="updateIdSelected" :required="isRequired">
        <option v-if="text" value="">{{ $t(text) }}</option>
        <option v-for="(option, i) in options" :key="i" :value="option.id" :selected="selected == option.id">
            {{ option.name }}
        </option>
    </select>
</template>

<script>
export default {
    name: 'selection',
    props: {
        options: Array,
        selected: Number | String,
        name: {
            type: String,
            default: "",
        },
        text: {
            type: String,
            default: "main.chooseOption",
        },
        isRequired: {
            type: Boolean,
            default: false,
        },
    },
    methods: {
        updateIdSelected(event) {
            this.$emit("idSelected", event.target.value);
            this.$emit("selectEvent", event);
        }
    }
};
</script>

<style></style>
