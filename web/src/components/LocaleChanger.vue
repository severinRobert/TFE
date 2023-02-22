<template>
    <select v-model="$i18n.locale">
      <option v-for="(lang, i) in langs" :key="`Lang${i}`" :value="lang.code">
        {{ lang.text }}
      </option>
    </select>
</template>

<script>
export default {
  name: 'locale-changer',
  data() {
    return {
      langs: [
        { code: "en", text: "EN" },
        { code: "fr", text: "FR" },
      ],
    };
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
