<template>
    <vs-list id="file-list">
        <vs-list-item icon="arrow_upward" title=".."></vs-list-item>
        <vs-list-item icon="image" :title="`xxx-${i}.jpg`" :key="i" v-for="i in files"></vs-list-item>
    </vs-list>
</template>

<script>
    export default {
        name: "FileList",
        data: () => ({
            files: [1, 2, 3, 90, 4, 95, 6, 8, 7, 5, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        })
    };
</script>

<style scoped>

</style>