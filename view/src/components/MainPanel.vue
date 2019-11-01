<template>
    <div id="main">
        <slot></slot>
    </div>
</template>

<script>
    export default {
        name: "MainPanel"
    };
</script>

<style scoped>
    #main {
        padding: 12px 24px 12px 66px;
        width: inherit;
    }
</style>