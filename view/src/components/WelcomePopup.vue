<template>
    <vs-prompt :title="title" :active.sync="active" :text="text" buttons-hidden>
        {{text}}
    </vs-prompt>
</template>

<script>
    export default {
        name: "WelcomePopup",
        props: {
            title: String,
            visible: Boolean,
            text: String
        },
        computed: {
            active: {
                get() {
                    return this.visible;
                },
                set(value) {
                    this.$emit("close");
                    return value;

                }
            }
        }
    };
</script>

<style scoped>

</style>