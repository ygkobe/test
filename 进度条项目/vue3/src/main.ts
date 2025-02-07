import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "./assets/tailwind.css";
import "@icon-park/vue-next/styles/index.css";
import "highlight.js/styles/dark.css";
import ElementPlus from 'element-plus';
import 'element-plus/theme-chalk/index.css';
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import zhCn from 'element-plus/es/locale/lang/zh-cn'; // 引入 Element Plus 中文包

import { createI18n } from 'vue-i18n';

// 配置 Vue I18n
const i18n = createI18n({
  locale: 'zh-cn',
  messages: {
    'zh-cn': {
      el: zhCn.el, // 使用 Element Plus 的中文包
    },
  },
});

const app = createApp(App);

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}

// 使用顺序很重要，确保 i18n 在 ElementPlus 之前被使用
app.use(i18n);

app.use(ElementPlus, {
  locale: zhCn, // 使用 Element Plus 的中文语言包
});

app.use(router).mount("#app");
