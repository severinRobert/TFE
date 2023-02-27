<template>
    <select>
      <option value="0">{{ $t("main.chooseOption") }}</option>
      <option v-for="(option, i) in options" :key="i" :value="option.id" :selected="selected==option.id">
        {{ option.name }}
      </option>
    </select>
</template>

<script>
export default {
    name: 'selection',
    props: {
            options: Array,
            selected: Number,
    },
};
</script>

<style></style>
