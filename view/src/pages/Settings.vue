<template>
    <div>
        <vs-row vs-type="flex" vs-justify="center">
            <vs-col vs-w="12" vs-type="flex" vs-justify="center">
                <h2>Settings</h2>
            </vs-col>
            <vs-col vs-w="8">
                <vs-input label="AWS Access Key ID" :value="awsAccessKeyId" disabled/>
                <vs-input label="AWS Secret Access Key" :value="awsSecretAccessKey" disabled/>
                <vs-input label="Selected region" :value="regionName" disabled/>
                <vs-input label="Selected bucket" :value="bucketName" disabled/>
                <vs-input label="Target path:" :value="targetPath" disabled/>
            </vs-col>
        </vs-row>
        <!-- Download Bucket -->
        <vs-row vs-type="flex" vs-justify="center">
            <vs-col vs-w="8">
                <vs-divider>Download Bucket</vs-divider>
                <p>
                    Download the entire bucket from AWS S3.
                    This is useful when migrating to a new device.
                </p>
            </vs-col>
            <vs-col vs-w="8">
                <vs-button color="primary" type="filled" @click="downloadPopup = true">Download Bucket</vs-button>
                <vs-prompt title="Download bucket?" :active.sync="downloadPopup" type="confirm" color="primary"
                           @accept="handleDownloadBucket" @reject="() => {this.downloadPopup = false}"
                           accept-text="Download" cancel-text="Cancel"
                >
                    Download the entire bucket from AWS S3?
                </vs-prompt>
            </vs-col>
        </vs-row>
        <!-- Danger Zone: Reset Application -->
        <vs-row vs-type="flex" vs-justify="center">
            <vs-col vs-w="8">
                <vs-divider>Danger Zone</vs-divider>
            </vs-col>
            <vs-col vs-w="8">
                <vs-button color="danger" type="filled" @click="resetPopup = true">Reset Application</vs-button>
                <vs-prompt title="Reset Application?" :active.sync="resetPopup" type="confirm" color="danger"
                           @accept="handleResetApplication" @reject="() => {this.resetPopup = false}"
                           accept-text="Yes" cancel-text="Cancel"
                >
                    All settings will be removed, you will need to reinitialize Private File Saver.
                </vs-prompt>
            </vs-col>
        </vs-row>
    </div>
</template>

<script>
    export default {
        name: "Settings",
        data: () => ({
            resetPopup: false,
            downloadPopup: false,
        }),
        mounted() {
            if (this.isInitialized) {
                this.$store.dispatch('listConfigs');
                this.$store.dispatch('fetchRegionList');
                this.$store.dispatch('fetchBucketList');
            }
        },
        methods: {
            handleResetApplication() {
                this.$store.dispatch('resetApplication');
            },
            handleDownloadBucket() {
                this.$store.dispatch('downloadBucket');
                setImmediate(function () {
                    this.$store.dispatch('goToPage', "HOME");
                }.bind(this));
            }
        },
        computed: {
            isInitialized() {
                return this.$store.state.isInitialized;
            },
            regionName: {
                get() {
                    return this.$store.getters.regionName;
                },
                // Setter is not implemented for now
            },
            bucketName: {
                get() {
                    return this.$store.getters.bucketName;
                },
                // Setter is not implemented for now
            },
            awsAccessKeyId() {
                return this.$store.getters.awsAccessKeyId;
            },
            awsSecretAccessKey() {
                return this.$store.getters.awsSecretAccessKey;
            },
            targetPath() {
                return this.$store.getters.targetPath;
            },
            regions() {
                return this.$store.state.regionList;
            },
            buckets() {
                return this.$store.state.bucketList;
            }
        }
    };
</script>

<style scoped>
    .vs-component {
        margin-bottom: 6px;
        margin-top: 6px;
        width: 100%;
    }
    .vs-divider {
        margin-top: 30px;
    }
</style>