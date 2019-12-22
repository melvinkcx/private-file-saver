import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

const getDefaultState = () => ({
    /* App */
    currentPage: 'HOME',
    pollTaskId: null,
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
    /* Syncer */
    currentDir: "",
    currentDirFiles: [],
    synced: true,
    /* Controls */
    dialogVisibility: {
        setupDialog: false,
    },
    /* Current Log */
    currentLog: "Initializing...",
});

export default new Vuex.Store({
    state: getDefaultState(),
    getters: {
        isLoading(state) {
            return state.status === "LOADING" || state.status === "PENDING_SETUP";
        },
        awsAccessKeyId(state) {
            return state.configs["AWS_ACCESS_KEY_ID"];
        },
        awsSecretAccessKey(state) {
            return state.configs["AWS_SECRET_ACCESS_KEY"];
        },
        targetPath(state) {
            return state.configs["TARGET_PATH"];
        },
        regionName(state) {
            return state.configs["AWS_REGION"];
        },
        bucketName(state) {
            return state.configs["DEFAULT_BUCKET_NAME"];
        },
        isRootDirectory(state, getters) {
            return getters.targetPath === state.currentDir;
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
                case "NOT_SYNCED":
                    state.status = {
                        code: "NOT_SYNCED",
                        text: "Not all files are synced!",
                        icon: "fa-times-circle",
                        color: "danger",
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
        setPollTaskId(state, value) {
            state.pollTaskId = value;
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
        /* Syncer */
        setCurrentDir(state, value) {
            state.currentDir = value;
        },
        setCurrentDirFiles(state, value) {
            state.currentDirFiles = value;
        },
        setSynced(state, value) {
            state.synced = value;
        },
        /* Controls */
        setDialogVisibility(state, {dialog, value}) {
            state.dialogVisibility[dialog] = value;
        },
        /* Danger Zone */
        resetAppState(state) {
            Object.assign(state, getDefaultState());
        },
        /* Current State/ Log */
        setCurrentLog(state, value) {
            state.currentLog = value;
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
                await store.dispatch('listConfigs');
                await store.dispatch('scanDirectory');
                store.dispatch('getSyncStatus');    // This caused problem with scanDirectory

                // Set up interval task
                // 1. Smart polling
                const pollTask = async function () {
                    await store.dispatch("" +
                        "scanDirectory", store.state.currentDir);
                    const pollTaskId = setTimeout(pollTask, 5000);
                    store.commit("setPollTaskId", pollTaskId);
                };
                const pollTaskId = setTimeout(pollTask, 5000);
                store.commit("setPollTaskId", pollTaskId);

                // 2. Get current state
                setInterval(() => {
                    store.dispatch("getCurrentLog");
                }, 1000);
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
            store.dispatch('getSyncStatus');
        },
        async listConfigs(store) {
            const configs = await window.pywebview.api.list_configs();
            store.commit('setConfigs', configs);
        },
        /* Syncer */
        async scanDirectory(store, path) {
            if (!path) {
                path = store.getters.targetPath;
            }
            const currentDirFiles = await window.pywebview.api.scan({path});
            store.commit('setCurrentDir', path);
            store.commit('setCurrentDirFiles', currentDirFiles);
            if (currentDirFiles.filter((f) => f.length > 2 && ["NOT_UPLOADED", "NOT_SYNCED"].includes(f[2])).length > 0) {
                store.commit('setStatus', 'NOT_SYNCED');
            }
            return currentDirFiles;
        },
        async sync(store) {
            store.commit('setStatus', 'SYNCING');
            try {
                await window.pywebview.api.sync();
                store.commit('setStatus', 'SYNCED');
            } catch (err) {
                store.commit('setStatus', 'NOT_SYNCED');
            }
        },
        async openDirectory(store, path) {
            return store.dispatch('scanDirectory', path);
        },
        async openFile(store, file) {
            return window.pywebview.api.open_file({file});
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
            return store.getters.targetPath;
        },
        async getSyncStatus(store) {
            store.commit('setStatus', "SCANNING");
            const syncStatus = await window.pywebview.api.get_sync_status();
            store.commit("setSynced", syncStatus.synced);
            store.commit('setStatus', syncStatus.synced ? "SYNCED" : "NOT_SYNCED");
            return syncStatus;
        },
        async resetApplication(store) {
            clearTimeout(store.state.pollTask);
            await window.pywebview.api.reset_application();
            store.commit('resetAppState');
            store.commit('setStatus', 'PENDING_SETUP');
            store.commit('setIsInitialized', false);
        },
        async getCurrentLog(store) {
            const log = await window.pywebview.api.get_current_log();
            store.commit('setCurrentLog', log);
        }
    },
});