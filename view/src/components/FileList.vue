<template>
    <vs-table :data="files" stripe hover-flat @selected="onClick" v-model="selected">
        <template slot="thead">
            <vs-th>Files</vs-th>
            <vs-th>Status</vs-th>
        </template>
        <template slot-scope="{data}">
            <vs-tr :data="f" :key="f" v-for="f in data">
                <vs-td :data="f">xxx-{{f}}.jpg</vs-td>
                <vs-td :data="f"></vs-td>
            </vs-tr>
        </template>
    </vs-table>
</template>

<script>
    export default {
        name: "FileList",
        data: () => ({
            selected: [],
            files: [1, 2, 3, 90, 4, 95, 6, 8, 7, 5, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        }),
        methods: {
            onClick() {
                console.log(`File ${this.selected} is clicked`);
            }
        }
    };
</script>

<style scoped>

</style>