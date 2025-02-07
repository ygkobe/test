<template>
	<div class="waiting-animation">
		<div class="text">
			<span class="dot1">w</span>
			<span class="dot2">a</span>
			<span class="dot3">i</span>
			<span class="dot1">t</span>
			<span class="dot2">.</span>
			<span class="dot3">.</span>
			<span class="dot1">.</span>

		</div>
	</div>
</template>

<style scoped>
	.waiting-animation {
		/*margin: 0 auto; !* 居中 *!*/
		width: fit-content; /* 根据内容调整宽度 */
		/*text-align: center; !* 文字居中 *!*/
	}

	.text {
		font-size: 18px; /* 调整文字大小 */
		margin-bottom: 10px; /* 底部间距 */
	}

	.dot1, .dot2, .dot3 {
		animation: jump 1s infinite;
		animation-timing-function: ease-in-out;
		display: inline-block;
	}

	.dot2 {
		animation-delay: 0.2s;
	}

	.dot3 {
		animation-delay: 0.1s;
	}

	@keyframes jump {
		0%, 20%, 80%, 100% {
			transform: translateY(0);
		}
		40% {
			transform: translateY(-5px);
		}
		60% {
			transform: translateY(-3px);
		}
	}
</style>
<script setup lang="ts">
</script>