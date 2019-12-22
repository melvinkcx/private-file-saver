<template>
    <div id="app">
        <Sidebar @on-page-changed="goToPage" parent="#app"/>
        <MainPanel>
            <Home v-if="currentPage === 'HOME'"/>
            <About v-else-if="currentPage === 'ABOUT'"/>
            <Settings v-else-if="currentPage === 'SETTINGS'"/>
            <LogMessageBar :message="currentState"/>
        </MainPanel>
        <!-- Dialogs -->
        <InitializationPopup v-if="setupDialogVisibility"
                             :visible="setupDialogVisibility"
                             @close="setupDialogVisibility = false"
                             @initialized="initializationCompleted"/>
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
    import LogMessageBar from "./components/LogMessageBar";

    export default {
        name: 'app',
        components: {
            LogMessageBar,
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
            currentState() {
                return this.$store.state.currentState;
            }
        },
        async mounted() {
            await this.$store.dispatch('initialize');
        },
        methods: {
            goToPage(page) {
                this.$store.dispatch('goToPage', page);
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
