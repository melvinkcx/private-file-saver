<template>
    <div>
        <vs-row vs-type="flex" vs-justify="center" vs-align="flex-start">
            <vs-col vs-w="8" vs-type="flex" vs-justify="center">
                <h2>Settings</h2>
            </vs-col>
            <vs-col vs-w="8">
                <vs-input label="AWS Access Key ID" :value="awsAccessKeyId" disabled/>
                <vs-input label="AWS Secret Access Key" :value="awsSecretAccessKey" disabled/>
                <vs-select label="Selected region" v-model="regionName" width="100%" disabled>
                    <vs-select-item :key="r" :value="r" :text="r" v-for="r in regions"/>
                </vs-select>
                <vs-select label="Selected bucket:" v-model="bucketName" width="100%" disabled>
                    <vs-select-item :key="b" :value="b" :text="b" v-for="b in buckets"/>
                </vs-select>
                <vs-input label="Target path:" :value="targetPath" disabled/>
            </vs-col>
        </vs-row>
    </div>
</template>

<script>
    export default {
        name: "Settings",
        mounted() {
            this.$store.dispatch('listConfigs');
            this.$store.dispatch('fetchRegionList');
            this.$store.dispatch('fetchBucketList');
        },
        computed: {
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
            awsAccessKeyId(){
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
</style>