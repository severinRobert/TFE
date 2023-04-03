<template>
    <div>
      <input
        type="text"
        v-model="inputValue"
        @input="search"
        @blur="onBlur"
        @keydown.down="incrementHighlight"
        @keydown.up="decrementHighlight"
        @keydown.enter="selectHighlighted"
      />
      <div v-if="isOpen" class="autocomplete-menu">
        <div
          v-for="(item, index) in filteredOptions"
          :key="item.id"
          :class="['autocomplete-item', { highlighted: index === highlightedIndex }]"
          @click="selectItem(item)"
        >
          {{ item.label }}
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "AutocompletionSelect",
    props: {
      options: Array,
      value: [String, Number],
      id: [String, Number],
    },
    data() {
      return {
        inputValue: "",
        isOpen: false,
        highlightedIndex: 0,
        filteredOptions: [],
      };
    },
    methods: {
      search() {
        this.filteredOptions = this.options.filter((option) =>
          option.label
            .toLowerCase()
            .includes(this.inputValue.toLowerCase())
        );
        this.isOpen = true;
      },
      onBlur() {
        this.isOpen = false;
      },
      selectHighlighted() {
        if (this.filteredOptions.length > 0) {
          this.selectItem(this.filteredOptions[this.highlightedIndex]);
        }
      },
      incrementHighlight() {
        if (this.highlightedIndex < this.filteredOptions.length - 1) {
          this.highlightedIndex++;
        }
      },
      decrementHighlight() {
        if (this.highlightedIndex > 0) {
          this.highlightedIndex--;
        }
      },
      selectItem(item) {
        this.inputValue = item.label;
        this.isOpen = false;
        this.$emit("update:id", item.id);
        this.$emit("update:value", item.label);
      },
    },
  };
  </script>
  
  <style>
  .autocomplete-menu {
    position: absolute;
    background-color: #fff;
    border: 1px solid #ddd;
    max-height: 200px;
    overflow-y: auto;
  }
  
  .autocomplete-item {
    padding: 5px;
    cursor: pointer;
  }
  
  .autocomplete-item.highlighted {
    background-color: #f2f2f2;
  }
  </style>
  