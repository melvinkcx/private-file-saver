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
        status: 'LOADING',
        configs: {},
        /* Controls */
        dialogVisibility: {
            setupDialog: false,

        }
    },
    mutations: {
        /* App */
        setStatus(state, value) {
            state.status = value;
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
            // TODO
            store.commit('setIsInitialized', true);
            store.commit('setStatus', "SCANNING");
        }
    },
});