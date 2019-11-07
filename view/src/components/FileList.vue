<template>
    <vs-table :data="files" stripe hover-flat @selected="onClick" v-model="selected" no-data-text="No files">
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
        props: {
            files: Object,
        },
        data: () => ({
            selected: [],
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