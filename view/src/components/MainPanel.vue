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
        margin: auto;
        padding: 36px 12px 12px 66px;
        width: 660px;
    }
</style>