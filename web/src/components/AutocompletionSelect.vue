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
      <button @click="unselect">x</button>
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
        console.log("AC search")
        console.log(this.options)
        this.filteredOptions = this.options.filter((option) =>
          option.label
            .toLowerCase()
            .includes(this.inputValue.toLowerCase())
        );
        this.isOpen = true;
      },
      unselect() {
        console.log("AC unselect")
        this.inputValue = "";
        this.$emit("update:value", "");
        this.$emit("idSelected", null);
      },
      onBlur() {
        console.log("AC onBlur")
        this.isOpen = false;
      },
      selectHighlighted() {
        console.log("AC selectHighlighted")
        if (this.filteredOptions.length > 0) {
          this.selectItem(this.filteredOptions[this.highlightedIndex]);
        }
      },
      incrementHighlight() {
        console.log("AC incrementHighlight")
        if (this.highlightedIndex < this.filteredOptions.length - 1) {
          this.highlightedIndex++;
        }
      },
      decrementHighlight() {
        console.log("AC decrementHighlight")
        if (this.highlightedIndex > 0) {
          this.highlightedIndex--;
        }
      },
      selectItem(item) {
        console.log("AC selectItem")
        this.inputValue = item.label;
        this.isOpen = false;
        this.$emit("update:value", item.label);
        this.$emit("idSelected", item.id);
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
    background-color: #e2e2e2;
  }
  </style>
  