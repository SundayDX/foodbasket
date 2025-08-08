import { RouteRecordRaw } from 'vue-router'
import Layout from '@/layout/index.vue'

const reportRoutes: RouteRecordRaw = {
  path: '/report',
  component: Layout,
  redirect: '/report/inventory',
  meta: { title: '数据报表', icon: 'DataLine' },
  children: [
    {
      path: 'inventory',
      component: () => import('@/views/report/inventory.vue'),
      name: 'InventoryReport',
      meta: { title: '库存报表' }
    },
    {
      path: 'delivery',
      component: () => import('@/views/report/delivery.vue'),
      name: 'DeliveryReport',
      meta: { title: '配送报表' }
    },
    {
      path: 'quality',
      component: () => import('@/views/report/quality.vue'),
      name: 'QualityReport',
      meta: { title: '质量报表' }
    },
    {
      path: 'damage',
      component: () => import('@/views/report/damage.vue'),
      name: 'DamageReport',
      meta: { title: '报损报表' }
    }
  ]
}

export default reportRoutes
