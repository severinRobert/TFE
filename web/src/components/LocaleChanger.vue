<template>
    <select @change="changeLocale">
      <option v-for="(lang, i) in langs" :value="lang.code" :selected="lang.code==$i18n.locale">
        {{ lang.text }}
      </option>
    </select>
</template>

<script>
export default {
  name: 'locale-changer',
  created() {
    this.$i18n.locale = localStorage.getItem('locale') || 'en';
  },
  data() {
    return {
      langs: [
        { code: "en", text: "EN" },
        { code: "fr", text: "FR" },
      ],
    };
  },
  methods: {
    changeLocale(e) {
      console.log(e.target.value)
      this.$i18n.locale = e.target.value;
      localStorage.setItem('locale', e.target.value);
    },
  },
};
</script>

<style>

select {
  background: transparent;
  color: var(--textPrimaryColor);
  border: none;
}

</style>
