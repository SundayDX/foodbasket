<template>
  <template v-if="!item.meta?.hidden">
    <!-- 有子菜单的情况 -->
    <el-sub-menu 
      v-if="hasChildren(item)"
      :index="resolvePath(item.path)"
    >
      <template #title>
        <el-icon v-if="item.meta?.icon">
          <component :is="item.meta.icon" />
        </el-icon>
        <span>{{ item.meta?.title }}</span>
      </template>
      <sidebar-item
        v-for="child in item.children"
        :key="child.path"
        :item="child"
        :base-path="resolvePath(item.path)"
      />
    </el-sub-menu>

    <!-- 没有子菜单的情况 -->
    <el-menu-item 
      v-else
      :index="resolvePath(item.path)"
      @click="navigateTo(resolvePath(item.path))"
    >
      <el-icon v-if="item.meta?.icon">
        <component :is="item.meta.icon" />
      </el-icon>
      <template #title>
        <span>{{ item.meta?.title }}</span>
      </template>
    </el-menu-item>
  </template>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import path from 'path-browserify'
import type { RouteRecordRaw } from 'vue-router'

const props = defineProps<{
  item: RouteRecordRaw
  basePath: string
}>()

const router = useRouter()

const hasChildren = (route: RouteRecordRaw) => {
  if (route.children) {
    return route.children.some(child => !child.meta?.hidden)
  }
  return false
}

const resolvePath = (routePath: string) => {
  if (path.isAbsolute(routePath)) {
    return routePath
  }
  return path.resolve(props.basePath, routePath)
}

const navigateTo = (path: string) => {
  router.push(path)
}
</script>

<style lang="scss" scoped>
.el-menu-item, :deep(.el-sub-menu__title) {
  .el-icon {
    margin-right: 12px;
    font-size: 16px;
  }
}
</style>