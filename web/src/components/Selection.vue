<template>
    <select @change="updateIdSelected">
      <option value="0">{{ $t(text) }}</option>
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
            text: {
              type: String,
              default: "main.chooseOption",
            }
    },
    methods: {
        updateIdSelected(event) {
          this.$emit("idSelected", event.target.value);
        }
    }
};
</script>

<style></style>
