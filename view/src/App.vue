<template>
    <div id="app">
        <Sidebar @on-page-changed="goToPage" parent="#app"></Sidebar>
        <MainPanel>
            <Home v-show="currentPage === 'HOME'" :configs="configs"></Home>
            <About v-show="currentPage === 'ABOUT'"></About>
            <Settings v-show="currentPage === 'SETTINGS'" :configs="configs"></Settings>
        </MainPanel>
        <!-- Dialogs -->
        <WelcomePopup :title="dialogContents.welcomeDialog.title"
                      :visible="dialogControls.welcomeDialog"
                      @close="dialogControls.welcomeDialog = false"
                      :text="dialogContents.welcomeDialog.text"/>
        <InitializationPopup :configs="configs"
                             :visible="dialogControls.setupDialog"
                             @close="dialogControls.setupDialog = false"
                             @initialized="initialized = true"
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
    import WelcomePopup from "./components/WelcomePopup";

    export default {
        name: 'app',
        components: {
            WelcomePopup,
            InitializationPopup,
            Settings,
            About,
            Home,
            Sidebar,
            MainPanel
        },
        data: () => ({
            currentPage: 'HOME',
            defaultColor: 'dark',
            initialized: true,
            isReady: false, // If pywebview is ready
            dialogControls: {
                welcomeDialog: false,
                setupDialog: true
            },
            dialogContents: {
                welcomeDialog: {
                    title: "Private File Saver",
                    text: `Store your precious files in your private encrypted storage.`
                },
            },
            configs: {},
        }),
        async mounted() {
            // Wait for api to be ready
            await this.$api.ping();

            // Get data
            this.isReady = true;
            this.initialized = await this.$api.isInitialized();
            this.configs = await this.$api.listConfigs();

            if (!this.initialized) this.dialogControls.setupDialog = true;
        },
        methods: {
            async goToPage(page) {
                this.currentPage = page;
            },
            promptDialog(dialogName) {
                try {
                    this.dialogControls[dialogName] = true;
                } catch (err) {
                    console.error(`Dialog ${dialogName} not found.`);
                }
            },
            updateConfigs({configs}) {
                this.configs = configs;
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
