import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { ElMessage } from 'element-plus'
import Layout from '@/layout/index.vue'
import reportRoutes from './modules/report'
import qualityRoutes from './modules/quality'

export const constantRoutes: RouteRecordRaw[] = [
  {
    path: '/login',
    component: () => import('@/views/login/index.vue'),
    meta: { title: '登录', hidden: true }
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        component: () => import('@/views/dashboard/index.vue'),
        name: 'Dashboard',
        meta: { title: '首页', icon: 'House', affix: true }
      }
    ]
  },
  {
    path: '/product',
    component: Layout,
    redirect: '/product/list',
    meta: { title: '商品管理', icon: 'ShoppingCart' },
    children: [
      {
        path: 'list',
        component: () => import('@/views/product/list.vue'),
        name: 'ProductList',
        meta: { title: '商品列表' }
      },
      {
        path: 'category',
        component: () => import('@/views/product/category.vue'),
        name: 'ProductCategory',
        meta: { title: '商品分类' }
      }
    ]
  },
  {
    path: '/inventory',
    component: Layout,
    redirect: '/inventory/list',
    meta: { title: '库存管理', icon: 'Box' },
    children: [
      {
        path: 'list',
        component: () => import('@/views/inventory/list.vue'),
        name: 'InventoryList',
        meta: { title: '库存列表' }
      },
      {
        path: 'transaction',
        component: () => import('@/views/inventory/transaction.vue'),
        name: 'InventoryTransaction',
        meta: { title: '出入库记录' }
      }
    ]
  },
  {
    path: '/delivery',
    component: Layout,
    redirect: '/delivery/list',
    meta: { title: '配送管理', icon: 'Van' },
    children: [
      {
        path: 'list',
        component: () => import('@/views/delivery/list.vue'),
        name: 'DeliveryList',
        meta: { title: '配送单列表' }
      },
      {
        path: 'create',
        component: () => import('@/views/delivery/create.vue'),
        name: 'DeliveryCreate',
        meta: { title: '新建配送单' }
      },
      {
        path: 'detail/:id',
        component: () => import('@/views/delivery/detail.vue'),
        name: 'DeliveryDetail',
        meta: { title: '配送单详情', hidden: true }
      }
    ]
  },
  {
    path: '/damage',
    component: Layout,
    redirect: '/damage/list',
    meta: { title: '报损管理', icon: 'Warning' },
    children: [
      {
        path: 'list',
        component: () => import('@/views/damage/list.vue'),
        name: 'DamageList',
        meta: { title: '报损列表' }
      },
      {
        path: 'create',
        component: () => import('@/views/damage/create.vue'),
        name: 'DamageCreate',
        meta: { title: '报损申请' }
      }
    ]
  },
  qualityRoutes,
  reportRoutes
]

const router = createRouter({
  history: createWebHistory(),
  routes: constantRoutes,
  scrollBehavior: () => ({ top: 0 })
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  // 设置页面标题
  document.title = `${to.meta.title || ''} - Food Basket`

  // 放行登录页
  if (to.path === '/login') {
    if (localStorage.getItem('food_basket_token')) {
      next('/')
      return
    }
    next()
    return
  }

  // 检查是否有token
  const hasToken = localStorage.getItem('food_basket_token')
  if (!hasToken) {
    ElMessage.warning('请先登录')
    next(`/login?redirect=${to.path}`)
    return
  }

  next()
})

export default router