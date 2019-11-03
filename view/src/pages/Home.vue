<template>
    <div>
        <!-- First row: General info-->
        <vs-row id="row-info">
            <vs-col vs-type="flex" vs-justify="center" vs-align="center" vs-w="2">
                <vs-icon v-show="status === 'SYNCED'" round size="large" color="success" icon="check_circle"></vs-icon>
                <vs-icon v-show="status === 'SYNCING'" round size="large" color="warning" icon="cloud_upload"></vs-icon>
                <vs-icon v-show="status === 'NO_NETWORK'" round size="large" color="danger" icon="wifi_off"></vs-icon>
                <vs-icon v-show="status === 'LOADING'" round size="large" color="warning" icon="fa-spinner"
                         icon-pack="fa"></vs-icon>
            </vs-col>
            <vs-col vs-w="10">
                <p class="info-header" v-show="status === 'SYNCED'">All files are synced! </p>
                <p class="info-header" v-show="status === 'SYNCING'">Synchronizing files... </p>
                <p class="info-header" v-show="status === 'NO_NETWORK'">Offline, please check your network
                    connection.</p>
                <p class="info-header" v-show="status === 'LOADING'">Loading... </p>
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
        props: {
            configs: Object
        },
        computed: {
            bucketName: function () {
                return this.configs["DEFAULT_BUCKET_NAME"] || "NOT SET";
            }
        },
        data: () => ({
            status: "LOADING", // SYNCED, SYNCING, NO_NETWORK
        }),
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