<template>
    <vs-prompt :title="title" :active.sync="active" buttons-hidden>
        <div id="step-1-credentials" v-show="currentStep === 1">
            <vs-input label="AWS Access Key ID" v-model="accessKeyId" style="width: unset"/>
            <vs-input label="AWS Secret Access Key" v-model="secretAccessKey" style="width: unset"/>
            <vs-button ref="submitStepOneButton" id="submit-step-one-loading" class="vs-con-loading__container"
                       @click="submitStepOne">
                Next
            </vs-button>
        </div>
        <div id="step-2-buckets" v-show="currentStep === 2">
            <vs-select label="Select Bucket" v-model="bucketName" width="100%">
                <vs-select-item :key="b" :value="b" :text="b" v-for="b in buckets"/>
            </vs-select>
            <vs-button ref="submitStepTwoButton" id="submit-step-two-loading" class="vs-con-loading__container"
                       @click="submitStepTwo">
                Last
            </vs-button>
        </div>
        <div id="step-3-target" v-show="currentStep === 3">
            <vs-input label="Select Folder to Sync" v-model="targetPath" style="width: unset"/>
            <vs-button ref="submitStepThreeButton" id="submit-step-three-loading" class="vs-con-loading__container"
                       @click="submitStepThree">
                Complete
            </vs-button>
        </div>

    </vs-prompt>
</template>

<script>
    export default {
        name: "InitializationPopup",
        props: {
            title: String,
            visible: Boolean,
            configs: Object,
        },
        data: () => ({
            currentStep: 1,
            buckets: []
        }),
        computed: {
            active: {
                get() {
                    return this.visible;
                },
                set(value) {
                    // this.$emit("close");
                    return value;

                }
            },
            accessKeyId: {
                get() {
                    return this.configs["AWS_ACCESS_KEY_ID"];
                },
                set(value) {
                    return value;
                }
            },
            secretAccessKey: {
                get() {
                    return this.configs["AWS_SECRET_ACCESS_KEY"];
                },
                set(value) {
                    return value;
                }
            },
            bucketName: {
                get() {
                    return this.configs["DEFAULT_BUCKET_NAME"];
                },
                set(value) {
                    return value;
                }
            },
            targetPath: {
                get() {
                    return this.configs["TARGET_PATH"];
                },
                set(value) {
                    return value;
                }
            },
        },
        methods: {
            submitStepOne() {
                // Set and validate access keys
                this.$vs.loading({
                    container: '#submit-step-one-loading',
                    type: 'corners',
                    scale: 0.45
                });
                // TODO FIXME submit and validate access key and policies
                setTimeout(() => {
                    this.currentStep += 1;
                    this.$vs.loading.close('#submit-step-one-loading');
                }, 1000);

            },
            submitStepTwo() {
                // Select bucket
                // TODO FIXME validate permission to write to bucket
                this.$vs.loading({
                    container: '#submit-step-two-loading',
                    type: 'corners',
                    scale: 0.45
                });
                setTimeout(() => {
                    this.currentStep += 1;
                    this.$vs.loading.close('#submit-step-two-loading');
                }, 1000);
            },
            submitStepThree() {
                // Validate
                // TODO FIXME validate permission on target path
                this.$vs.loading({
                    container: '#submit-step-three-loading',
                    type: 'corners',
                    scale: 0.45
                });
                setTimeout(() => {
                    this.currentStep += 1;
                    this.$vs.loading.close('#submit-step-three-loading');
                    this.$emit('close');
                }, 1000);
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