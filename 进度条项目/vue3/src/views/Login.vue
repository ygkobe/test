<template>
  <div class="login-container">
    <div class="login-background"></div>
    <div class="login-form">
      <el-card class="login-card" style="border-radius: 50px">
        <h1 class="login-title">
          <el-text class="mx-1" type="primary" size="large">违章处理</el-text>
        </h1>
        <el-form
          v-if="!isRegister"
          ref="loginForm"
          :rules="rules"
          :model="loginData"

        >
          <el-form-item prop="username" class="centered-form-item">
            <el-input
              size="large"
              v-model="loginData.username"
              placeholder="用户名"
              style="border-radius: 10px"
            >
              <template #prepend>
                <el-icon style="font-size: 24px;"><User /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item prop="password" class="centered-form-item">
            <el-input
              size="large"
              type="password"
              v-model="loginData.password"
              placeholder="密码"
              @keyup.enter.native="login"
            >
              <template #prepend>
                <el-icon style="font-size: 24px;"><Key /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item class="centered-form-item">
            <el-button style="width: 100%" type="primary" @click="login">
              登 录
            </el-button>
          </el-form-item>
          <el-form-item class="centered-form-item">
            <el-button style="width: 100%" type="text" @click="toggleForm">
              注册
            </el-button>
          </el-form-item>
        </el-form>

        <el-form
          v-else
          ref="registerForm"
          :rules="registerRules"
          :model="registerData"

        >
          <el-form-item prop="username" class="centered-form-item">
            <el-input
              size="large"
              v-model="registerData.username"
              placeholder="用户名"
            >
              <template #prepend>
                <el-icon style="font-size: 24px;"><User /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item prop="password" class="centered-form-item">
            <el-input
              size="large"
              type="password"
              v-model="registerData.password"
              placeholder="密码"
              @keyup.enter.native="register"
            >
              <template #prepend>
                <el-icon style="font-size: 24px;"><Key /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item prop="confirmPassword" class="centered-form-item">
            <el-input
              size="large"
              type="password"
              v-model="registerData.confirmPassword"
              placeholder="确认密码"
              @keyup.enter.native="register"
            >
              <template #prepend>
                <el-icon style="font-size: 24px;"><Key /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item class="centered-form-item">
            <el-button style="width: 100%" type="primary" @click="register">
              注 册
            </el-button>
          </el-form-item>
          <el-form-item class="centered-form-item">
            <el-button style="width: 100%" type="text" @click="toggleForm">
              已有账号？登录
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script lang="ts">
import { reactive, ref } from 'vue';
import { ElForm, ElFormItem, ElInput, ElButton, ElCard, ElMessage } from 'element-plus';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { User, Key } from '@element-plus/icons-vue';

export default {
  components: {
    ElForm,
    ElFormItem,
    ElInput,
    ElButton,
    ElCard,
    User,
    Key
  },
  setup() {
    const isRegister = ref(false);
    const loginData = reactive({
      username: '',
      password: ''
    });

    const registerData = reactive({
      username: '',
      password: '',
      confirmPassword: ''
    });

    const rules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' }
      ]
    };

    const registerRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' }
      ],
      confirmPassword: [
        { required: true, message: '请确认密码', trigger: 'blur' },
        { validator: (rule: any, value: string, callback: (error?: Error) => void) => {
          if (value !== registerData.password) {
            callback(new Error('两次输入的密码不一致'));
          } else {
            callback();
          }
        }, trigger: 'blur' }
      ]
    };

    const router = useRouter();

    const login = () => {
      axios.post('http://127.0.0.1:8002/user/login/', {
        username: loginData.username,
        password: loginData.password
      })
        .then(response => {
          const token = response.data.token;
          localStorage.setItem('token', token);
          localStorage.setItem('username', response.data.username);
          router.push('/home/violation');
        })
        .catch(error => {
          ElMessage({
            message: '用户名或密码错误',
            type: 'error'
          });
        });
    };

    const register = () => {
      axios.post('http://127.0.0.1:8002/user/register/', {
        username: registerData.username,
        password: registerData.password,
        confirmPassword: registerData.confirmPassword
      })
        .then(response => {
          ElMessage({
            message: '注册成功，请登录',
            type: 'success'
          });
          isRegister.value = false;
        })
        .catch(error => {
          ElMessage({
            message: '注册失败，请重试',
            type: 'error'
          });
        });
    };

    const toggleForm = () => {
      isRegister.value = !isRegister.value;
    };

    return {
      loginData,
      registerData,
      rules,
      registerRules,
      login,
      register,
      toggleForm,
      isRegister
    };
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  height: 100vh;
  justify-content: center;
  align-items: center;
  position: relative;
}

.login-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url("@/assets/2111.jpg");
  background-size: cover;
  z-index: 0;
}

.login-form {
  z-index: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-card {
  width: 550px;
  padding: 20px;
  background-color: #f5f7fa;
}

.login-title {
  font-size: 20px;
  margin-bottom: 20px;
  text-align: center;
}

.centered-form-item {
  display: flex;
  justify-content: center;
}

.el-form-item {
  text-align: center;
}

.el-button {
  margin-left: auto;
  margin-right: auto;
  display: block;
}

.n-gradient-text {
  font-size: 30px;
}
</style>
