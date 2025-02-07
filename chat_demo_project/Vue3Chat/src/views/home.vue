<template>
  <div class="flex flex-col h-screen">
    <div class="sticky top-0 z-50">
      <el-menu
        class="el-menu-demo"
        mode="horizontal"
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b"
        style="width: 100%;"
      >
        <el-menu-item index="1">Chatgpt</el-menu-item>
        <el-menu-item index="2" disabled>消息中心</el-menu-item>
        <el-menu-item index="3">
          <a href="https://www.ele.me" target="_blank">管理</a>
        </el-menu-item>
      </el-menu>
    </div>

    <div class="flex-1 mx-2 mt-20 mb-2" ref="chatListDom">
      <div
        class="group flex flex-col px-4 py-3 hover:bg-slate-100 rounded-lg"
        v-for="item in messageList.filter(v => v.role!='system')"
        :key="item.id"
        :style="{
          margin: '15px',
          padding: '10px'
        }"
      >
        <div class="flex justify-start items-center mb-2">
          <img
            v-if="item.role === 'user'"
            class="h-8 w-8 mr-2 rounded-full"
            src="@/assets/img_2.png"
            alt="User Icon"
            :style="{ margin: '5px' }"
          />
          <img
            v-if="item.role === 'assistant'"
            class="h-8 w-8 mr-2 rounded-full"
            src="@/assets/img.png"
            alt="Assistant Icon"
            :style="{ margin: '5px' }"
          />
          <div class="font-bold" style="font-size: 14px;color: #0f9cfd">{{ item.role === 'user'? '光之崽种 ' : " 文件传输助手 " }}</div>
          <Copy class="invisible group-hover:visible" :content="item.content" />
        </div>
        <div>
          <div
            class="prose text-sm  leading-relaxed"

            v-if="item.content"
            v-html="md.render(item.content)"
          ></div>
          <Loding v-else />
        </div>
      </div>
    </div>

    <div class="sticky bottom-0 w-full p-6 pb-8 bg-gray-100">
      <div class="flex">
        <textarea
          class="input h-15"
          @keydown.enter.prevent="handleEnter"
          @keydown.enter.shift.prevent="handleShiftEnter"
          v-model="messageContent"
        ></textarea>
        <button class="btn" :disabled="isTalking" @click="sendOrSave" style="width: 100px;background-color: #545c64; margin-left: 0;">
          <el-icon style="width: 20px;"><Promotion /></el-icon>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick, onMounted } from "vue";
import { chat } from "@/libs/gpt";
import Loding from "@/components/Loding.vue";
import Copy from "@/components/Copy.vue";
import { md } from "@/libs/markdown";

let isTalking = ref(false);
let messageContent = ref("");
const chatListDom = ref<HTMLDivElement | null>(null);
const decoder = new TextDecoder("utf-8");

// 定义 ChatMessage 类型
interface ChatMessage {
  id: number;
  role: "user" | "assistant" | "system";
  content: string;
}

const messageList = ref<ChatMessage[]>([
  {
    id: 1,
    role: "system",
    content: "你是 ChatGPT，OpenAI 训练的大型语言模型，尽可能简洁地回答。",
  },
  {
    id: 2,
    role: "assistant",
    content: `# 你好，我是AI语言模型，我只会说666 `,
  },
]);

onMounted(() => {
  sendOrSave();
});

const sendChatMessage = async (content: string = messageContent.value) => {
  try {
    isTalking.value = true;
    if (messageList.value.length === 2) {
      messageList.value.pop();
    }
    messageList.value.push({ id: messageList.value.length + 1, role: "user", content });
    clearMessageContent();
    messageList.value.push({ id: messageList.value.length + 1, role: "assistant", content: "" });

    const { body, status } = await chat(messageList.value);
    if (body) {
      const reader = body.getReader();
      await readStream(reader, status);
    }
    scrollToBottom();
  } catch (error: any) {
    appendLastMessageContent(error);
  } finally {
    isTalking.value = false;
  }
};

const handleEnter = (event: KeyboardEvent) => {
  if (!event.shiftKey) {
    sendOrSave();
  }
};

const handleShiftEnter = (event: KeyboardEvent) => {
  if (event.shiftKey) {
    messageContent.value += "\n";
  }
};

const readStream = async (
  reader: ReadableStreamDefaultReader<Uint8Array>,
  status: number
) => {
  let partialLine = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;

    const decodedText = decoder.decode(value, { stream: true });
    appendLastMessageContent(decodedText);
    scrollToBottom();
  }
};

const appendLastMessageContent = (content: string) => {
  const lastMessage = messageList.value[messageList.value.length - 1];
  if (lastMessage && lastMessage.role === "assistant") {
    lastMessage.content += content;
  }
};

const sendOrSave = () => {
  if (!messageContent.value.trim()) return;
  sendChatMessage();
};

const clearMessageContent = () => {
  messageContent.value = "";
};

const scrollToBottom = () => {
  window.scrollTo(0, document.body.scrollHeight);
};

watch(messageList, () => {
  scrollToBottom();
});
</script>

<style scoped>
  /* 新增以下样式 */
.input {
    flex: 1;  /* 让输入框占据剩余的全部宽度 */
  }
.btn {
    margin-left: 0;  /* 去除按钮的左边距 */
  }
</style>