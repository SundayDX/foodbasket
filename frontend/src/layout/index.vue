<template>
  <div class="app-wrapper">
    <!-- 侧边栏 -->
    <div 
      class="sidebar-container" 
      :class="{ 'is-collapsed': isCollapsed }"
    >
      <div class="logo-container flex-center">
        <img v-if="!isCollapsed" src="@/assets/logo.svg" alt="Logo" class="logo">
        <img v-else src="@/assets/logo-small.svg" alt="Logo" class="logo-small">
      </div>
      <el-scrollbar>
        <el-menu
          :default-active="activeMenu"
          :collapse="isCollapsed"
          :unique-opened="true"
          :collapse-transition="false"
          class="sidebar-menu"
          background-color="#304156"
          text-color="#bfcbd9"
          active-text-color="#409EFF"
        >
          <sidebar-item 
            v-for="route in routes"
            :key="route.path"
            :item="route"
            :base-path="route.path"
          />
        </el-menu>
      </el-scrollbar>
    </div>

    <!-- 主要内容区 -->
    <div class="main-container">
      <!-- 顶部导航栏 -->
      <div class="navbar">
        <div class="left-area">
          <el-icon 
            class="fold-btn"
            @click="toggleSidebar"
          >
            <component :is="isCollapsed ? 'Expand' : 'Fold'" />
          </el-icon>
          <breadcrumb class="breadcrumb-container" />
        </div>
        
        <div class="right-area">
          <el-tooltip
            content="全屏"
            placement="bottom"
          >
            <el-icon 
              class="action-icon"
              @click="toggleFullScreen"
            >
              <component :is="isFullscreen ? 'FullscreenExit' : 'FullScreen'" />
            </el-icon>
          </el-tooltip>

          <el-dropdown trigger="click">
            <div class="avatar-container">
              <el-avatar 
                :size="32"
                :src="userStore.avatar || ''"
              />
              <span class="username">{{ userStore.name }}</span>
              <el-icon class="el-icon--right">
                <CaretBottom />
              </el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="handleProfile">
                  <el-icon><User /></el-icon>
                  个人信息
                </el-dropdown-item>
                <el-dropdown-item divided @click="handleLogout">
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>

      <!-- 主要内容 -->
      <div class="app-main">
        <router-view v-slot="{ Component }">
          <transition name="fade-transform" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useFullscreen } from '@vueuse/core'
import { useUserStore } from '@/stores/user'
import SidebarItem from './components/SidebarItem.vue'
import Breadcrumb from './components/Breadcrumb.vue'
import { constantRoutes } from '@/router'

const userStore = useUserStore()
const route = useRoute()
const { isFullscreen, toggle: toggleFullscreen } = useFullscreen()

const isCollapsed = ref(false)
const routes = constantRoutes

const activeMenu = computed(() => {
  const { meta, path } = route
  if (meta?.activeMenu) {
    return meta.activeMenu
  }
  return path
})

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value
}

const toggleFullScreen = () => {
  toggleFullscreen()
}

const handleProfile = () => {
  // TODO: 跳转到个人信息页面
}

const handleLogout = async () => {
  await userStore.logout()
  window.location.reload()
}
</script>

<style lang="scss" scoped>
.app-wrapper {
  height: 100%;
  display: flex;
}

.sidebar-container {
  width: $sidebar-width;
  height: 100%;
  background-color: #304156;
  transition: width 0.3s;
  overflow: hidden;

  &.is-collapsed {
    width: $sidebar-collapsed-width;
  }

  .logo-container {
    height: $header-height;
    padding: $spacing-base;
    background-color: #2b2f3a;

    .logo-text {
      color: #fff;
      font-size: 20px;
      margin: 0;
      transition: all 0.3s;
    }

    .logo-text-small {
      color: #fff;
      font-size: 16px;
      margin: 0;
      transition: all 0.3s;
    }
  }

  .sidebar-menu {
    border: none;
  }
}

.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background-color: $background-color-base;
}

.navbar {
  height: $header-height;
  padding: 0 $spacing-base;
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  display: flex;
  align-items: center;
  justify-content: space-between;

  .left-area {
    display: flex;
    align-items: center;

    .fold-btn {
      padding: 0 $spacing-base;
      cursor: pointer;
      font-size: 20px;
      color: $text-regular;
      transition: all 0.3s;

      &:hover {
        color: $primary-color;
      }
    }
  }

  .right-area {
    display: flex;
    align-items: center;

    .action-icon {
      padding: 0 $spacing-base;
      cursor: pointer;
      font-size: 18px;
      color: $text-regular;
      transition: all 0.3s;

      &:hover {
        color: $primary-color;
      }
    }

    .avatar-container {
      display: flex;
      align-items: center;
      padding: 0 $spacing-base;
      cursor: pointer;

      .username {
        margin: 0 $spacing-small;
        color: $text-regular;
      }
    }
  }
}

.app-main {
  flex: 1;
  padding: $spacing-base;
  overflow-y: auto;
}

// 路由过渡动画
.fade-transform-enter-active,
.fade-transform-leave-active {
  transition: all 0.3s;
}

.fade-transform-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>