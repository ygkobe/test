// import type { ChatMessage } from "@/types";
interface ChatMessage {
  role: "user" | "assistant" | "system";
  content: string;
}
export async function chat(messageList: ChatMessage[]) {
  try {
    // const result = await fetch("http://220.231.144.212:8002/chat/sparkai", {
    // const result = await fetch("http://127.0.0.1:8002/chat/openai", {
    const result = await fetch("http://220.231.144.212:8002/chat/sparkai/flow", {
    // const result = await fetch("http://127.0.0.1:8002/chat/sparkai/flow", {
      method: "post",
	  mode:'cors',
	  headers: {
                'Access-Control-Allow-Origin': '*',
				'Content-Type': 'application/json'
            },
      // signal: AbortSignal.timeout(8000),
      // 开启后到达设定时间会中断流式输出
      body: JSON.stringify({


        messages: messageList

      }),
    });
    return result;
  } catch (error) {
    throw error;

  }
}
