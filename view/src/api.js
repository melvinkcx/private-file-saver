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

    async isInitialized() {
        return window.pywebview.api.is_initialized();
    }

    async listConfigs() {
        return window.pywebview.api.list_configs();
    }

    async listConfigurables() {
        return window.pywebview.api.list_configurables();
    }

    async setConfigs(values) {
        return window.pywebview.api.set_configs(values);
    }

    // AWS
    async testAndSetCredentials(accessKeyID, secretAccessKey) {
        return window.pywebview.api.test_and_set_credentials(accessKeyID, secretAccessKey);
    }

    async listBuckets() {
        return window.pywebview.api.list_buckets()
    }

    async setDefaultBucket(bucketName) {
        return window.pywebview.api.set_default_bucket(bucketName)
    }

    async setTargetPath(targetPath) {
        return window.pywebview.api.set_target_path(targetPath)
    }


    // Syncer
    async scan(path) {
        return window.pywebview.api.scan(path);
    }

    async sync() {
        return window.pywebview.api.sync();
    }
}