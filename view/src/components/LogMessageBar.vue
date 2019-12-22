<template>
    <div class="log-message-bar">
        <i>{{ message }}</i>
    </div>
</template>

<script>
    export default {
        name: "LogMessageBar",
        props: ["message"]
    };
</script>

<style scoped>
    .log-message-bar {
        position: absolute;
        bottom: 0;
        padding: 14px 8px;
    }
</style>