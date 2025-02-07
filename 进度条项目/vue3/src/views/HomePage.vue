<template>
  <div style="position: relative;">
    <el-menu
      class="el-menu-demo"
      mode="horizontal"
      background-color="#545c64"
      text-color="#fff"
      active-text-color="#ffd04b"
      style="width: 100%; top: 0; position: fixed; z-index: 1000; display: flex; justify-content: space-between;"
    >
      <!-- 左侧菜单项 -->
      <div style="display: flex;">
          <router-link to="/home/violation" style="text-decoration: none;">
          <el-menu-item index="1">违章处理 <el-icon><Grid /></el-icon> </el-menu-item>
        </router-link>
<!--        <router-link to="/home/chatgpt" style="text-decoration: none;">-->
<!--          <el-menu-item index="3">违章地点查询 <el-icon><Search /></el-icon> </el-menu-item>-->
<!--        </router-link>-->

          <el-menu-item index="2">

              <a href="https://www.baidu.com/" target="_blank"> 跳转到其他页面</a> <el-icon><Link /></el-icon>
          </el-menu-item>

<!--        <router-link to="/home/temp" style="text-decoration: none;">-->
<!--          <el-menu-item index="3">临时测试 <el-icon><Grid /></el-icon> </el-menu-item>-->
<!--        </router-link>-->

      </div>

      <!-- 右侧子菜单 -->
      <el-sub-menu index="4">
        <template #title> <span style="font-size: 18px; color: #ffffff"><el-icon><Avatar /></el-icon> {{ username }}</span> </template>
        <el-menu-item index="4-1" @click="logout" style="width: 100%">退出</el-menu-item>
      </el-sub-menu>
    </el-menu>
  </div>
  <div class="content-container">
    <router-view></router-view>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';

const router = useRouter(); // 在 setup 函数中调用 useRouter
const username = ref(localStorage.getItem('username') || '');

const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('username');
  router.push('/login'); // 使用保存在 setup 函数中的 router 对象

  ElMessage({
    message: '退出登录',
    type: 'success',
  });
};
</script>

<style scoped>
.el-menu-demo {
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
}

.content-container {
  margin: 5px;
  height: calc(100vh - 50px); /* 60px 是顶部菜单的高度 */
  overflow-y: auto;
  position: relative;
  top: 50px; /* 将内容容器向下移动 60px */
}
</style>
