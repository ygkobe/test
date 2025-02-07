import type { ChatMessage } from "@/types";

export async function chat(messageList: ChatMessage[]) {
  try {
    const result = await fetch("http://220.231.144.212:8002/chat/sparkai", {
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
