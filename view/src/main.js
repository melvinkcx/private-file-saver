import Vue from 'vue';
import App from './App.vue';
import Vuesax from 'vuesax';

import 'vuesax/dist/vuesax.css';
import 'material-icons/iconfont/material-icons.css';
import '@fortawesome/fontawesome-free/css/all.css';

Vue.config.productionTip = false;

Vue.use(Vuesax, {
  theme:{
    colors:{
      primary:'#FF9F00',
    }
  }
});


new Vue({
    render: h => h(App),
}).$mount('#app');
