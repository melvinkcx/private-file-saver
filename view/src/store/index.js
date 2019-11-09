import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        /* App */
        currentPage: 'HOME',
        isReady: false,
        isInitialized: false,
        defaultColor: 'dark',
        status: {
            code: "LOADING",
            text: "Loading",
            icon: "fa-spinner",
            color: "warning",
        },
        configs: {},
        /* Initialization Popup*/
        regionList: [],
        bucketList: [],
        /* Controls */
        dialogVisibility: {
            setupDialog: false,
        }
    },
    mutations: {
        /* App */
        setStatus(state, code) {
            switch (code) {
                case "LOADING":
                    state.status = {
                        code: "LOADING",
                        text: "Loading",
                        icon: "fa-spinner",
                        color: "warning",
                    };
                    break;
                case "PENDING_SETUP":
                    state.status = {
                        code: "PENDING_SETUP",
                        text: "Pending setup",
                        icon: "fa-spinner",
                        color: "warning",
                    };
                    break;
                case "SYNCING":
                    state.status = {
                        code: "SYNCING",
                        text: "Synchronizing files",
                        icon: "cloud_upload",
                        color: "primary",
                    };
                    break;
                case "SYNCED":
                    state.status = {
                        code: "SYNCED",
                        text: "All files are synced!",
                        icon: "check_circle",
                        color: "success",
                    };
                    break;
                case "SCANNING":
                    state.status = {
                        code: "SCANNING",
                        text: "Scanning files",
                        icon: "fa-search",
                        color: "primary",
                    };
                    break;
                case "NO_NETWORK":
                    state.status = {
                        code: "NO_NETWORK",
                        text: "Offline, please check your network connection",
                        icon: "wifi_off",
                        color: "danger",
                    };
                    break;
            }
        },
        setIsReady(state, value) {
            state.isReady = value;
        },
        setIsInitialized(state, value) {
            state.isInitialized = value;
        },
        setConfigs(state, value) {
            state.configs = value;
        },
        setCurrentPage(state, value) {
            state.currentPage = value;
        },
        /* Initialization */
        setRegionList(state, value) {
            state.regionList = value;
        },
        setBucketList(state, value) {
            state.bucketList = value;
        },
        /* Controls */
        setDialogVisibility(state, {dialog, value}) {
            state.dialogVisibility[dialog] = value;
        }
    },
    actions: {
        async ping() {
            // Check if pywebview is ready
            let notAvailable = true;
            let pong = false;
            do {
                try {
                    pong = await window.pywebview.api.ping();
                    if (!pong) {
                        throw new Error("APIs still not available");
                    }
                    notAvailable = false;
                } catch (err) {
                    await new Promise((res) => setTimeout(res, 500));
                }
            } while (notAvailable);
            return pong;
        },
        async goToPage(store, page) {
            store.commit('setCurrentPage', page);
        },
        async initialize(store) {
            await store.dispatch('ping');

            store.commit('setIsReady', true);

            const isInitialized = await window.pywebview.api.is_initialized();
            store.commit('setIsInitialized', isInitialized);

            if (isInitialized) {
                const configs = await window.pywebview.api.list_configs();
                store.commit('setConfigs', configs);
            } else {
                store.commit('setDialogVisibility', {
                    dialog: 'setupDialog',
                    value: true,
                });
                store.commit('setStatus', "PENDING_SETUP");
            }
        },
        async completeInitialization(store) {
            store.commit('setIsInitialized', true);
            store.dispatch('scanDirectory');
        },
        /* Syncer */
        async scanDirectory(store, path) {
            await window.pywebview.api.scan({path});
        },
        async sync() {
            return window.pywebview.api.sync();
        },
        /* Initialization */
        async fetchRegionList(store) {
            await store.dispatch('ping');

            const regionList = await window.pywebview.api.list_regions();
            store.commit('setRegionList', regionList);
        },
        async fetchBucketList(store) {
            await store.dispatch('ping');

            const bucketList = await window.pywebview.api.list_buckets();
            store.commit('setBucketList', bucketList);
        },
        async testAndSetCredentials(store, {accessKeyId, secretAccessKey, regionName}) {
            await store.dispatch('ping');

            return window.pywebview.api.test_and_set_credentials({
                access_key_id: accessKeyId,
                secret_access_key: secretAccessKey,
                region_name: regionName
            });
        },
        async selectDefaultBucket(store, {bucketName}) {
            const configs = await window.pywebview.api.set_default_bucket({bucket_name: bucketName});
            store.commit('setConfigs', configs);
        },
        async selectTargetPath(store) {
            const configs = await window.pywebview.api.select_target_path();
            store.commit('setConfigs', configs);
            return configs["TARGET_PATH"];
        }
    },
});