export default class PythonApi {
    constructor() {
        // FIXME BUG: This doesn't distinguish if Vue is in PyWebView mode
        if (window.hasOwnProperty('pywebview')) {
            console.log("In PyWebView mode");
            this.pywebviewMode = true;
        } else {
            console.warn("PyWebView is not detected");
            this.pywebviewMode = false;
        }
    }

    async ping() {
        return window.pywebview.api.ping();
    }

    async list_configs() {
        return window.pywebview.api.list_configs();
    }

    async list_configurables() {
        return window.pywebview.api.list_configurables();
    }

    async set_configs(values) {
        return window.pywebview.api.set_configs(values);
    }

    async scan(path) {
        return window.pywebview.api.scan(path);
    }

    async sync() {
        return window.pywebview.api.sync();
    }
}