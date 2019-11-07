<template>
    <vs-prompt :title="title" :active.sync="active" buttons-hidden>
        <div id="step-1-credentials" v-show="currentStep === 1" class="vs-con-loading__container">
            <vs-input label="AWS Access Key ID" v-model="accessKeyId" style="width: unset"/>
            <vs-input label="AWS Secret Access Key" v-model="secretAccessKey" style="width: unset"/>
            <vs-select label="Select region" v-model="regionName" width="100%" v-show="regions.length">
                <vs-select-item :key="r" :value="r" :text="r" v-for="r in regions"/>
            </vs-select>
            <vs-button class="vs-con-loading__container" @click="submitStepOne" :disabled="disableStepOneButton">
                Next
            </vs-button>
        </div>
        <div id="step-2-buckets" v-show="currentStep === 2">
            <vs-select label="Select Bucket" v-model="bucketName" width="100%">
                <vs-select-item :key="b" :value="b" :text="b" v-for="b in buckets"/>
            </vs-select>
            <vs-button class="vs-con-loading__container" @click="submitStepTwo" :disabled="disableStepTwoButton">
                Last
            </vs-button>
        </div>
        <div id="step-3-target" v-show="currentStep === 3">
            <div>
                <!-- Ref: https://stackoverflow.com/questions/2809688/directory-chooser-in-html-page -->
                <vs-button @click="submitStepThree">Select Folder</vs-button>
            </div>
        </div>
    </vs-prompt>
</template>

<script>
    export default {
        name: "InitializationPopup",
        props: {
            visible: Boolean,
            configs: Object,
        },
        data: () => ({
            currentStep: 1,
            regions: [],
            buckets: [],
            regionName: "",
            secretAccessKey: "",
            accessKeyId: "",
            bucketName: "",
        }),
        async created() {
            await this.$api.ping();
            this.regions = await this.$api.listRegions();
        },
        computed: {
            title() {
                return `Complete Setup (${this.currentStep}/3)`;
            },
            active: {
                get() {
                    return this.visible;
                },
                set(value) {
                    this.$vs.notify({
                        title: "Setup Required",
                        text: "Initial setup is necessary",
                        color: "warning"
                    });
                    return value;
                }
            },
            disableStepOneButton() {
                return !this.secretAccessKey || !this.accessKeyId || !this.regionName || !this.regions.length;
            },
            disableStepTwoButton() {
                return !this.bucketName;
            },
        },
        methods: {
            async submitStepOne() {
                // Set and validate access keys
                this.$vs.loading({
                    container: '#step-1-credentials',
                    type: 'corners',
                    scale: 0.45
                });
                try {
                    const res = await this.$api.testAndSetCredentials(this.accessKeyId, this.secretAccessKey, this.regionName);
                    if (res.error || !res.ok) {
                        this.$vs.notify({
                            title: res.code,
                            text: res.message,
                            color: "danger"
                        });
                    } else {
                        this.$vs.notify({
                            title: "First step done",
                            text: `Default region is: ${this.regionName}`,
                            color: "success"
                        });
                        this.buckets = await this.$api.listBuckets();
                        this.currentStep += 1;
                    }
                } catch (err) {
                    this.$vs.notify({
                        title: "An error occurred",
                        text: err.message,
                        color: "danger"
                    });
                } finally {
                    this.$vs.loading.close('#step-1-credentials > .con-vs-loading');
                }
            },
            async submitStepTwo() {
                // Select bucket
                this.$vs.loading({
                    container: '#step-2-buckets',
                    type: 'corners',
                    scale: 0.45
                });
                try {
                    const configs = await this.$api.setDefaultBucket(this.bucketName);
                    this.$vs.notify({
                        title: "One more step to go",
                        text: `Selected "${this.bucketName}"`,
                        color: "success"
                    });
                    this.$emit("update-config", {configs});
                    this.currentStep += 1;
                } catch (err) {
                    this.$vs.notify({
                        title: "An error occurred",
                        text: err.message,
                        color: "danger"
                    });
                } finally {
                    this.$vs.loading.close('#step-2-buckets  > .con-vs-loading');
                }
            },
            async submitStepThree() {
                this.$vs.loading({
                    container: '#step-3-target',
                    type: 'corners',
                    scale: 0.45
                });
                try {
                    const configs = await this.$api.selectTargetPath();
                    if (configs) {
                        this.$vs.notify({
                            title: "All set!",
                            text: `Target path is: ${configs["TARGET_PATH"]}`,
                            color: "success"
                        });
                        this.$emit("update-config", {configs});
                        this.$emit("initialized");
                        this.$emit("close");
                    }

                } catch (err) {
                    this.$vs.notify({
                        title: "An error occurred",
                        text: err.message,
                        color: "danger"
                    });
                } finally {
                    this.$vs.loading.close('#step-3-target  > .con-vs-loading');
                }
            }
        }
    };
</script>

<style scoped>
    .vs-component {
        margin-bottom: 6px;
        margin-top: 6px;
    }
</style>