import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import Layout from '@/layout/index.vue'
import reportRoutes from './modules/report'

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
  {
    path: '/quality',
    component: Layout,
    redirect: '/quality/check',
    meta: { title: '质量管理', icon: 'CircleCheck' },
    children: [
      {
        path: 'check',
        component: () => import('@/views/quality/check.vue'),
        name: 'QualityCheck',
        meta: { title: '质量检查' }
      },
      {
        path: 'standard',
        component: () => import('@/views/quality/standard.vue'),
        name: 'QualityStandard',
        meta: { title: '质量标准' }
      },
      {
        path: 'detail/:id',
        component: () => import('@/views/quality/detail.vue'),
        name: 'QualityDetail',
        meta: { title: '检查详情', hidden: true, activeMenu: '/quality/check' }
      }
    ]
  },
  reportRoutes
]

const router = createRouter({
  history: createWebHistory(),
  routes: constantRoutes,
  scrollBehavior: () => ({ top: 0 })
})

export default router