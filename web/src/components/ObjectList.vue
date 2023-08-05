<template>
    <section>
        <input :list="title" v-model="objectSelected" @change="inputChange()" placeholder="Search in the list ...">
        <datalist :id="title">
            <option v-for="object in objects" :value="object.name">
                {{ object.name }}
            </option>
        </datalist>
        <button class="validation" @click="addObject">{{ name }}</button>
    </section>
</template>

<script>
export default {
    name: 'object-list',
    props: ['objects', 'name'],
    data() {
        return {
            objectSelected: '',
        };
    },
    methods: {
        inputChange() {
            this.$emit('object-selected', this.objectSelected);
        }
    },
};
</script>

<style></style>
