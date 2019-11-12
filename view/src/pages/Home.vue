<template>
    <div>
        <!-- First row: General info-->
        <vs-row id="row-info">
            <vs-col vs-type="flex" vs-justify="center" vs-align="center" vs-w="2">
                <vs-icon round size="large" :color="status.color" :icon="status.icon"
                         :icon-pack="status.icon.startsWith('fa') ? 'fa' : 'material-icons'"></vs-icon>
            </vs-col>
            <vs-col vs-w="10">
                <p class="info-header">{{status.text}}</p>
                <p><b>Bucket name: </b> {{ bucketName }}</p>
                <p><small>{{ currentDir }}</small></p>
            </vs-col>
        </vs-row>
        <vs-row id="row-file-list" vs-type="flex" vs-justify="center" vs-align="flex-start">
            <vs-col vs-w="12">
                <FileList/>
            </vs-col>
        </vs-row>
    </div>
</template>

<script>
    import FileList from "../components/FileList";

    export default {
        name: "Home",
        components: {FileList},
        computed: {
            currentDir() {
                return this.$store.state.currentDir;
            },
            status() {
                return this.$store.state.status;
            },
            configs() {
                return this.$store.state.configs;
            },
            bucketName() {
                return this.configs["DEFAULT_BUCKET_NAME"] || "...";
            }
        },
    };
</script>

<style scoped>
    .info-header {
        font-size-adjust: 0.7;
    }

    #row-info {
        height: fit-content;
        padding-bottom: 24px;
    }

    #row-file-list {
        overflow-y: scroll;
        overflow-x: hidden;
        height: 80vh;
    }
</style>