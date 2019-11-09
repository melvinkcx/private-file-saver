<template>
    <vs-table :data="files" stripe hover-flat @selected="onClick" @dblSelection="onDoubleClick" v-model="selected"
              no-data-text="No files">
        <template slot="thead">
            <vs-th>Files</vs-th>
            <vs-th>Status</vs-th>
        </template>
        <template slot-scope="{data}">
            <vs-tr :data="['..', 'DIRECTORY']" v-if="!isRootDirectory && !isLoading">
                <vs-td>
                    <span>
                        <vs-icon icon="fa-arrow-up" icon-pack="fa" style="padding-right: 6px"></vs-icon>
                        ..
                    </span>
                </vs-td>
            </vs-tr>
            <vs-tr :data="f" :key="`${f[0]}_${f[1]}`" v-for="f in data">
                <vs-td>
                    <span v-if="f[1] === 'DIRECTORY'">
                        <vs-icon icon="fa-folder" icon-pack="fa" style="padding-right: 6px"></vs-icon>
                        {{ f[0] }}/
                    </span>
                    <span v-else-if="f[1] === 'FILE'">
                        <vs-icon icon="fa-file" icon-pack="fa" style="padding-right: 6px"></vs-icon>
                        {{ f[0] }}
                    </span>
                    <span v-else> {{ f[0] }}</span>
                </vs-td>
                <vs-td>{{ f[2] }}</vs-td>
            </vs-tr>
        </template>
    </vs-table>
</template>

<script>
    export default {
        name: "FileList",
        data: () => ({
            selected: [],
        }),
        computed: {
            isLoading() {
                return this.$store.getters.isLoading;
            },
            files() {
                return this.$store.state.currentDirFiles;
            },
            currentDir() {
                return this.$store.state.currentDir;
            },
            isRootDirectory() {
                return this.$store.getters.isRootDirectory;
            }
        },
        methods: {
            onClick() {
                console.log(`File ${this.selected} is clicked`);
            },
            async onDoubleClick() {
                const [fileOrFolder, fileType] = this.selected;
                let fileOrFolderPath;

                if (fileOrFolder === "..") {
                    fileOrFolderPath = this.currentDir.split("/").slice(0, -1).join("/");
                } else {
                    fileOrFolderPath = `${this.currentDir}/${fileOrFolder}`;
                }

                if (fileType === 'DIRECTORY') {
                    await this.$store.dispatch('openDirectory', fileOrFolderPath);
                } else if (fileType === 'FILE') {
                    await this.$store.dispatch('openFile', fileOrFolderPath);
                }
            }
        }
    };
</script>

