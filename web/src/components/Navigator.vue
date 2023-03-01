<template>
    <section>
        <button @click="previous" :disabled="previousDisabled"> &lt; </button>
        <button @click="next" :disabled="nextDisabled"> > </button>
    </section>
</template>

<script>
export default {
    name: 'navigator',
    props: {
        prevPage: String
    },
    methods: {
        previous() {
            if (this.prevPage === '/dashboard') {
                this.$router.push(this.prevPage);
            }
        },
        next() {
            if (this.prevPage.indexOf('/dashboard/product') > -1) {
                this.$router.push(this.prevPage);
            }
        }
    },
    computed: {
        previousDisabled: function(){
            return this.prevPage !== '/dashboard';
        },
        nextDisabled: function(){
            return this.prevPage.indexOf('/dashboard/product') === -1;
        }
    }
};
</script>

<style></style>
