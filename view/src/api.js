/**
 * FIXME
 *
 * Refactor this!
 */

export default class PythonApi {
    /**
     * PythonApi
     *
     * When calling python api, we need to explicitly states arguments in snake case
     */

    async ping() {
        // Check if pywebview is ready
        let notAvailable = true;
        let pong = false;
        do {
            try {
                pong = await window.pywebview.api.ping();
                if (!pong) {
                    throw new Error("APIs still not available");
                }
                notAvailable = false;
            } catch (err) {
                await new Promise((res) => setTimeout(res, 500));
            }
        } while (notAvailable);
        return pong;
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
        return window.pywebview.api.set_configs({values});
    }

    // AWS
    async listRegions() {
        return window.pywebview.api.list_regions();
    }

    async testAndSetCredentials(access_key_id, secret_access_key, region_name) {
        return window.pywebview.api.test_and_set_credentials({access_key_id, secret_access_key, region_name});
    }

    async listBuckets() {
        return window.pywebview.api.list_buckets();
    }

    async setDefaultBucket(bucket_name) {
        return window.pywebview.api.set_default_bucket({bucket_name});
    }

    async selectTargetPath() {
        return window.pywebview.api.select_target_path();
    }

    // Syncer
    async scan(path) {
        return window.pywebview.api.scan({path});
    }

    async sync() {
        return window.pywebview.api.sync();
    }
}