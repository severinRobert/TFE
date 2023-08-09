<template>
    <section class="content">
        <h1>{{ $t("gdpr.title") }}</h1>
        <h2>{{ $t("gdpr.personalDataStored") }}</h2>
        <p>{{ $t("gdpr.personalDataStoredText") }}</p>
        <h2>{{ $t("gdpr.personalDataUsage") }}</h2>
        <p>{{ $t("gdpr.personalDataUsageText") }}</p>
    </section>
</template>

<script>

export default {
    name: 'gdpr-view',
};
</script>

<style>
</style>
