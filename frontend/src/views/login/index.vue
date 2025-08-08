<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <img src="@/assets/logo.png" alt="Logo" class="logo">
          <h2>生鲜流通数据系统</h2>
        </div>
      </template>
      
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
        autocomplete="on"
        label-position="top"
      >
        <el-form-item prop="username" label="用户名">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            type="text"
            tabindex="1"
            :prefix-icon="User"
            autocomplete="on"
          />
        </el-form-item>

        <el-form-item prop="password" label="密码">
          <el-input
            v-model="loginForm.password"
            placeholder="请输入密码"
            :type="passwordVisible ? 'text' : 'password'"
            tabindex="2"
            :prefix-icon="Lock"
            autocomplete="on"
            show-password
          />
        </el-form-item>

        <el-form-item>
          <el-button
            :loading="loading"
            type="primary"
            class="login-button"
            @click.prevent="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import type { FormInstance } from 'element-plus'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const loginFormRef = ref<FormInstance>()
const loading = ref(false)
const passwordVisible = ref(false)

const loginForm = reactive({
  username: '',
  password: ''
})

const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, message: '用户名长度不能小于3个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能小于6个字符', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    await loginFormRef.value.validate()
    loading.value = true
    
    const result = await userStore.login({
      username: loginForm.username,
      password: loginForm.password
    })

    if (result) {
      ElMessage.success('登录成功')
      router.push({ path: '/' })
    } else {
      ElMessage.error('登录失败，请检查用户名和密码')
    }
  } catch (error) {
    console.error('Login error:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  width: 420px;
  border-radius: $border-radius-large;
  box-shadow: $box-shadow-dark;
  background-color: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);

  .card-header {
    text-align: center;
    padding: $spacing-base 0;

    .logo {
      height: 48px;
      margin-bottom: $spacing-base;
    }

    h2 {
      margin: 0;
      color: $text-primary;
      font-size: 24px;
      font-weight: 600;
    }
  }
}

.login-form {
  padding: $spacing-large;

  .login-button {
    width: 100%;
    height: 44px;
    margin-top: $spacing-base;
  }
}

:deep(.el-input__wrapper) {
  height: 44px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: $text-regular;
}
</style>