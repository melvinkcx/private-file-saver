<template>
    <vs-sidebar reduce reduce-not-hover-expand hidden-background :parent="parent" default-index="1" :value="true"
                color="primary" static>
        <vs-sidebar-item index="1" icon="cloud_upload" @click="onItemClick('HOME')">Home</vs-sidebar-item>
        <vs-sidebar-item index="2" icon="info" @click="onItemClick('ABOUT')">About</vs-sidebar-item>
        <vs-sidebar-item index="3" icon="settings_input_component" @click="onItemClick('SETTINGS')">Settings
        </vs-sidebar-item>
    </vs-sidebar>
</template>

<script>
    export default {
        name: "Sidebar",
        props: {
            parent: String
        },
        methods: {
            onItemClick(page) {
                this.$emit("on-page-changed", page);
            }
        }
    };
</script>

<style scoped>

</style>