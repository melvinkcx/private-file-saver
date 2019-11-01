<template>
    <div id="main">
        <slot></slot>
    </div>
</template>

<script>
    export default {
        name: "MainPanel"
    }
</script>

<style scoped>
    #main {
        margin-left: 54px;
        padding: 12px;
    }
</style>