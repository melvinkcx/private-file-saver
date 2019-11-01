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
}