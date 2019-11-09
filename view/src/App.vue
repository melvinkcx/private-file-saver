<template>
    <div id="app">
        <Sidebar @on-page-changed="goToPage" parent="#app"></Sidebar>
        <MainPanel>
            <Home v-show="currentPage === 'HOME'" :configs="configs" :status="status"></Home>
            <About v-show="currentPage === 'ABOUT'"></About>
            <Settings v-show="currentPage === 'SETTINGS'" :configs="configs"></Settings>
        </MainPanel>
        <!-- Dialogs -->
        <InitializationPopup v-if="setupDialogVisibility"
                             :configs="configs"
                             :visible="setupDialogVisibility"
                             @close="setupDialogVisibility = false"
                             @initialized="initializationCompleted"
                             @update-config="updateConfigs"/>
        <!-- End of Dialogs -->
    </div>
</template>

<script>
    import Sidebar from "./components/Sidebar";
    import MainPanel from "./components/MainPanel";
    import Home from "./pages/Home";
    import About from "./pages/About";
    import Settings from "./pages/Settings";
    import InitializationPopup from "./components/InitializationPopup";

    export default {
        name: 'app',
        components: {
            InitializationPopup,
            Settings,
            About,
            Home,
            Sidebar,
            MainPanel
        },
        computed: {
            currentPage() {
                return this.$store.state.currentPage;
            },
            defaultColor() {
                return this.$store.state.defaultColor;
            },
            isInitialized() {
                return this.$store.state.isInitialized;
            },
            setupDialogVisibility: {
                get() {
                    return this.$store.state.dialogVisibility.setupDialog;
                },
                set(value) {
                    return this.$store.commit('setDialogVisibility', {dialog: 'setupDialog', value});
                }
            },

            configs() {
                return this.$store.state.configs;
            },
            status() {
                return this.$store.state.status;
            },
        },
        async mounted() {
            await this.$store.dispatch('initialize');
        },
        methods: {
            updateConfigs({configs}) {
                this.$store.commit('setConfigs', configs);
            },
            initializationCompleted() {
                this.$store.dispatch('completeInitialization');
            }
        }
    };
</script>

<style scoped>
    #app {
        width: 100vw;
        height: 100vh;
        margin: 0;
        padding: 0;
    }
</style>
