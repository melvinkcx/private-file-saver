<template>
    <div id="app">
        <Sidebar @on-page-changed="goToPage" parent="#app"></Sidebar>
        <MainPanel>
            <Home v-show="currentPage === 'HOME'"></Home>
            <About v-show="currentPage === 'ABOUT'"></About>
            <Settings v-show="currentPage === 'SETTINGS'"></Settings>
        </MainPanel>
        <!-- Dialogs -->
        <vs-prompt
                :title="dialogContents.welcomeDialog.title"
                buttons-hidden
                :active.sync="dialogControls.welcomeDialog"
        >
            {{dialogContents.welcomeDialog.text}}
        </vs-prompt>
        <vs-prompt
                :active.sync="dialogControls.initializationDialog"
                buttons-hidden
        >
            Initialized..
        </vs-prompt>
        <!-- End of Dialogs -->
    </div>
</template>

<script>
    import Sidebar from "./components/Sidebar";
    import MainPanel from "./components/MainPanel";
    import Home from "./pages/Home";
    import About from "./pages/About";
    import Settings from "./pages/Settings";

    export default {
        name: 'app',
        components: {
            Settings,
            About,
            Home,
            Sidebar,
            MainPanel
        },
        data: () => ({
            currentPage: 'HOME',
            defaultColor: 'dark',
            dialogControls: {
                welcomeDialog: false,
                initializationDialog: false,
            },
            dialogContents: {
                welcomeDialog: {
                    title: "Private File Saver",
                    text: "Store your precious files in your private encrypted storage."
                }
            }
        }),
        created() {
            this.promptDialog('welcomeDialog');
        },
        methods: {
            goToPage(page) {
                this.currentPage = page;
            },
            promptDialog(dialogName) {
                try {
                    this.dialogControls[dialogName] = true;
                } catch (err) {
                    console.error(`Dialog ${dialogName} not found.`);
                }
            },
        }
    };
</script>

<style scoped>
    #app {
        width: 660px;
        height: 100vh;
        margin: 0;
        padding: 0;
    }
</style>
