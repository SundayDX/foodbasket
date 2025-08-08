import { RouteRecordRaw } from 'vue-router'

const qualityRoutes: RouteRecordRaw = {
  path: '/quality',
  name: 'Quality',
  component: () => import('@/layout/index.vue'),
  meta: {
    title: '质量管理',
    icon: 'Shield',
    order: 5
  },
  children: [
    {
      path: 'check',
      name: 'QualityCheck',
      component: () => import('@/views/quality/check.vue'),
      meta: {
        title: '质量检查',
        icon: 'Check',
        keepAlive: true
      }
    },
    {
      path: 'standard',
      name: 'QualityStandard',
      component: () => import('@/views/quality/standard.vue'),
      meta: {
        title: '检查标准',
        icon: 'Document',
        keepAlive: true
      }
    },
    {
      path: 'detail/:id',
      name: 'QualityDetail',
      component: () => import('@/views/quality/detail.vue'),
      meta: {
        title: '检查详情',
        icon: 'InfoFilled',
        hidden: true,
        activeMenu: '/quality/check'
      }
    }
  ]
}

export default qualityRoutes