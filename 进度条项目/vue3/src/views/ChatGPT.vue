<template>
    <div class="flex flex-col h-screen">

        <!-- Chat Messages -->
        <div class="flex-1 mx-2 mt-20 mb-2" ref="chatListDom">
            <div
                    class="group flex flex-col px-4 py-3 hover:bg-slate-100 rounded-lg"
                    v-for="item in messageList.filter(v => v.role !== 'system')"
                    :key="item.id"
                    :style="{
          margin: '15px',
          padding: '10px',
          width: 'auto', /* Ensure width is auto to allow natural flow */
          maxWidth: '100%' /* Optionally set maxWidth to control maximum width */
        }"
            >
                <!-- User Messages -->
                <div class="flex justify-end items-center mb-2" v-if="item.role === 'user'">
                    <!--          <Copy class="invisible group-hover:visible" :content="item.content" />-->

                    <el-tooltip content="复制" placement="top" effect="light" style="background-color: #1db393">
                        <button style="padding: 5px; margin:5px" @click="copyToClipboard(item.content)">
                            <el-icon>
                                <CopyDocument/>
                            </el-icon>
                        </button>
                    </el-tooltip>

                    <div class="flex items-center">
                        <div class="font-bold" style="font-size: 14px; color: #0f9cfd; padding-right: 2px">User
                        </div>
                        <img
                                class="h-8 w-8 ml-2 rounded-full"
                                src="@/assets/img_2.png"
                                alt="User Icon"
                                :style="{ margin: '5px' }"
                        />
                    </div>
                </div>

                <!-- Assistant Messages -->
                <div class="flex justify-start items-center mb-2" v-else>
                    <img
                            class="h-8 w-8 mr-2 rounded-full"
                            src="@/assets/chatgpt.png"
                            alt="Assistant Icon"
                            :style="{ margin: '5px' }"
                    />
                    <div class="font-bold" style="font-size: 14px; color: #0f9cfd; padding-left: 2px"> ChatGPT</div>
                    <el-tooltip content="复制" placement="top" effect="light" style="background-color: #1db393">
                        <button style="padding: 5px; margin:5px" @click="copyToClipboard(item.content)">
                            <el-icon>
                                <CopyDocument/>
                            </el-icon>
                        </button>
                    </el-tooltip>
                </div>

                <!-- Message Content -->
                <div>
                    <div
                            :style="item.role === 'user'? 'font-size: 16px;float:right; padding-right: 10px;white-space: normal;word-wrap: break-word; ' : ' font-size: 16px;border-radius: 15px; padding-left: 10px;'"
                            v-if="item.content"
                            v-html="md.render(item.content)"
                    ></div>
                    <Loding v-else/>
                </div>

            </div>
        </div>

        <!-- Message Input -->

        <div class="sticky bottom-0 w-full p-6 pb-8 bg-gray-100">
    <div class="flex" style="display: flex; align-items: center;">
        <textarea
            class="input h-15"
            @keydown.enter.prevent="handleEnter"
            @keydown.enter.shift.prevent="handleShiftEnter"
            v-model="messageContent"
            style="height: 80px; border-radius: 30px 0 0 30px; flex-grow: 1; margin-right: 0; border-right: 0;"
        ></textarea>
        <button class="btn" :disabled="isTalking" @click="sendOrSave"
            style="background-color: #545c64; width: 150px; border-radius: 0 30px 30px 0; margin-left: 0;height: 80px;">
            <el-icon style="width: 20px;">
                <Promotion/>
            </el-icon>
        </button>
    </div>
</div>


    </div>
</template>

<script setup lang="ts">
import {ref, watch, nextTick, onMounted} from "vue";
import Loding from "@/components/Loding.vue";
import {md} from "@/libs/markdown";
import {ElMessage} from 'element-plus'

let isTalking = ref(false);
let messageContent = ref("");
const chatListDom = ref<HTMLDivElement | null>(null);
const decoder = new TextDecoder("utf-8");

interface ChatMessage {
    id: number;
    role: "user" | "assistant" | "system";
    content: string;
}

async function chat(messageList: ChatMessage[]) {
    try {
        const result = await fetch("http://127.0.0.1:8002/chat/sparkai/flow", {
            method: "post",
            mode: 'cors',
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                messages: messageList
            }),
        });
        return result;
    } catch (error) {
        throw error;
    }
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
        content: `你好，我是AI语言模型，支持字眼语言对话，可以查询违章地址
        比如： 数据提供方为：深圳市公安局交通警察支队罗湖大队 违章地址： 仙湖路仙湖植物园景区路段东行， 这个违章地址在哪个城市？
        `,
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

        messageList.value.push({id: messageList.value.length + 1, role: "user", content});
        scrollToBottom();
        clearMessageContent();

        messageList.value.push({id: messageList.value.length + 1, role: "assistant", content: ""});
        scrollToBottom();

        const {body, status} = await chat(messageList.value);
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
    scrollToBottom();
    if (!event.shiftKey) {
        sendOrSave();
    }
};

const handleShiftEnter = (event: KeyboardEvent) => {
    scrollToBottom();
    if (event.shiftKey) {
        messageContent.value += "\n";
    }
};

const copyToClipboard = async (content: string) => {
    try {
        await navigator.clipboard.writeText(content);
        ElMessage({
            message: '内容已成功复制到剪贴板',
            type: 'success',
        })
        console.log('内容已成功复制到剪贴板');
    } catch (err) {
        console.error('复制操作失败：', err);
    }
};

const readStream = async (
    reader: ReadableStreamDefaultReader<Uint8Array>,
    status: number
) => {
    let partialLine = "";
    scrollToBottom();
    while (true) {
        const {value, done} = await reader.read();
        if (done) break;

        const decodedText = decoder.decode(value, {stream: true});
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
    scrollToBottom();
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
.input {
    flex: 1; /* 让输入框占据剩余的全部宽度 */
}

.btn {
    margin-left: 0; /* 去除按钮的左边距 */
}
</style>
