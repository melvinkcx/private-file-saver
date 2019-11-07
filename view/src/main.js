import Vue from 'vue';
import App from './App.vue';
import Vuesax from 'vuesax';

import 'vuesax/dist/vuesax.css';
import 'material-icons/iconfont/material-icons.css';
import '@fortawesome/fontawesome-free/css/all.css';
import PythonApi from "./api";

Vue.config.productionTip = false;

Vue.use(Vuesax, {
    theme: {
        colors: {
            primary: '#FF9F00',
        }
    }
});

/**
 * FIXME, wait for new release, listen to `pywebviewready` window event to know if PyWebView is ready
 * https://github.com/r0x0r/pywebview/issues/378
 */
Vue.prototype.$api = new PythonApi();

new Vue({
    render: h => h(App),
}).$mount('#app');
