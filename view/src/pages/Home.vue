<template>
    <div>
        <!-- First row: General info-->
        <vs-row id="row-info">
            <vs-col vs-type="flex" vs-justify="center" vs-align="center" vs-w="2">
                <vs-icon round size="large" :color="status.color" :icon="status.icon"
                         :icon-pack="status.icon.startsWith('fa') ? 'fa' : 'material-icons'"></vs-icon>
            </vs-col>
            <vs-col vs-w="9">
                <p class="info-header">{{status.text}}</p>
                <p><b>Bucket name: </b> {{ bucketName }}</p>
                <p><small>{{ currentDir }}</small></p>
            </vs-col>
            <vs-col vs-w="1" vs-type="flex" vs-justify="flex-end" vs-align="flex-end">
                <vs-button v-if="showSyncButton" id="sync-button" class="vs-con-loading__container" color="primary" icon="sync" @click="sync"></vs-button>
                <vs-button v-if="showScanButton" id="scan-button" class="vs-con-loading__container" color="primary" icon="search" @click="getSyncStatus"></vs-button>
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
            },
            showScanButton() {
                return ["SYNCED", "NO_NETWORK", "SCANNING"].includes(this.$store.state.status.code);
            },
            showSyncButton() {
                return ["NOT_SYNCED", "SYNCING"].includes(this.$store.state.status.code);
            },
        },
        methods: {
            async sync() {
                this.$vs.loading({
                    container: '#sync-button',
                    type: 'corners',
                    scale: 0.25
                });
                await this.$store.dispatch("sync");
                this.$vs.loading.close('#sync-button > .con-vs-loading');
            },
            async getSyncStatus() {
                this.$vs.loading({
                    container: '#scan-button',
                    type: 'corners',
                    scale: 0.25
                });
                await this.$store.dispatch("getSyncStatus");
                this.$vs.loading.close('#scan-button > .con-vs-loading');
            }
        }
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