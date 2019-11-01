<template>
    <div id="app">
        <Sidebar @on-page-changed="goToPage" parent="#app"></Sidebar>
        <MainPanel>
            <Home v-show="currentPage === 'HOME'"></Home>
            <About v-show="currentPage === 'ABOUT'"></About>
            <Settings v-show="currentPage === 'SETTINGS'"></Settings>
        </MainPanel>
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
           currentPage: 'HOME'
        }),
        methods: {
            goToPage(page) {
                this.currentPage = page;
                console.log(`Go to ${page}`);
            }
        }
    };
</script>

<style>

</style>
