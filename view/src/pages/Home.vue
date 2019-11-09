<template>
    <div>
        <!-- First row: General info-->
        <vs-row id="row-info">
            <vs-col vs-type="flex" vs-justify="center" vs-align="center" vs-w="2">
                <vs-icon v-show="status === 'SYNCED'" round size="large" color="success" icon="check_circle"></vs-icon>
                <vs-icon v-show="status === 'SYNCING'" round size="large" color="warning" icon="cloud_upload"></vs-icon>
                <vs-icon v-show="status === 'NO_NETWORK'" round size="large" color="danger" icon="wifi_off"></vs-icon>
                <vs-icon v-show="status === 'LOADING' || status === 'PENDING_SETUP'" round size="large" color="warning"
                         icon="fa-spinner"
                         icon-pack="fa"></vs-icon>
                <vs-icon v-show="status === 'SCANNING'" round size="large" color="primary" icon="fa-search"
                         icon-pack="fa"></vs-icon>
            </vs-col>
            <vs-col vs-w="10">
                <p class="info-header" v-show="status === 'SYNCED'">All files are synced! </p>
                <p class="info-header" v-show="status === 'SYNCING'">Synchronizing files </p>
                <p class="info-header" v-show="status === 'NO_NETWORK'">Offline, please check your network
                    connection.</p>
                <p class="info-header" v-show="status === 'LOADING'">Loading </p>
                <p class="info-header" v-show="status === 'PENDING_SETUP'"> Pending setup </p>
                <p class="info-header" v-show="status === 'SCANNING'">Scanning files </p>
                <p><b>Bucket name: </b> {{ bucketName }}</p>
            </vs-col>
        </vs-row>
        <vs-row id="row-file-list" vs-type="flex" vs-justify="center" vs-align="flex-start">
            <vs-col vs-w="12">
                <FileList></FileList>
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
            status() {
                return this.$store.state.status;
            },
            configs() {
                return this.$store.state.configs;
            },
            bucketName() {
                return this.configs["DEFAULT_BUCKET_NAME"] || "...";
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