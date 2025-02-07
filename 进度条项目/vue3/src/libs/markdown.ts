import Markdown from "markdown-it";
import highlight from "highlight.js";

const mdOptions: Markdown.Options = {
  linkify: true,
  typographer: true,
  breaks: true,
  langPrefix: "language-",
  // 代码高亮
  highlight(str, lang) {
    if (lang && highlight.getLanguage(lang)) {
      try {
        return (
          '<pre class="hljs" style="background-color: rgba(0,0,0,0.93); border-radius: 10px; margin: 10px;padding: 15px"><code>' +  // 设置背景颜色样式
          highlight.highlight(lang, str, true).value +
          "</code></pre>"
        );
      } catch (__) {}
    }
    return "";
  },
};

export const md = new Markdown(mdOptions);


