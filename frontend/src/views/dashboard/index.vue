<template>
  <div class="dashboard">
    <!-- 概览数据卡片 -->
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card shadow="hover" class="overview-card">
          <div class="card-header">
            <span class="title">今日营业额</span>
            <el-icon class="icon"><Money /></el-icon>
          </div>
          <div class="card-content">
            <div class="value">¥{{ formatNumber(overview.todayRevenue) }}</div>
            <div class="trend" :class="{ 'up': overview.revenueTrend > 0, 'down': overview.revenueTrend < 0 }">
              <span>{{ Math.abs(overview.revenueTrend) }}%</span>
              <el-icon><component :is="overview.revenueTrend > 0 ? 'ArrowUp' : 'ArrowDown'" /></el-icon>
            </div>
          </div>
          <div class="card-footer">
            昨日：¥{{ formatNumber(overview.yesterdayRevenue) }}
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="overview-card">
          <div class="card-header">
            <span class="title">今日订单数</span>
            <el-icon class="icon"><Document /></el-icon>
          </div>
          <div class="card-content">
            <div class="value">{{ overview.todayOrders }}</div>
            <div class="trend" :class="{ 'up': overview.ordersTrend > 0, 'down': overview.ordersTrend < 0 }">
              <span>{{ Math.abs(overview.ordersTrend) }}%</span>
              <el-icon><component :is="overview.ordersTrend > 0 ? 'ArrowUp' : 'ArrowDown'" /></el-icon>
            </div>
          </div>
          <div class="card-footer">
            昨日：{{ overview.yesterdayOrders }}
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="overview-card">
          <div class="card-header">
            <span class="title">库存预警</span>
            <el-icon class="icon"><Warning /></el-icon>
          </div>
          <div class="card-content">
            <div class="value warning">{{ overview.warningCount }}</div>
            <div class="trend" :class="{ 'up': overview.warningTrend > 0, 'down': overview.warningTrend < 0 }">
              <span>{{ Math.abs(overview.warningTrend) }}%</span>
              <el-icon><component :is="overview.warningTrend > 0 ? 'ArrowUp' : 'ArrowDown'" /></el-icon>
            </div>
          </div>
          <div class="card-footer">
            <el-link type="warning" @click="handleViewWarnings">查看详情</el-link>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="overview-card">
          <div class="card-header">
            <span class="title">待处理事项</span>
            <el-icon class="icon"><Bell /></el-icon>
          </div>
          <div class="card-content">
            <div class="value">{{ overview.todoCount }}</div>
            <div class="trend" :class="{ 'up': overview.todoTrend > 0, 'down': overview.todoTrend < 0 }">
              <span>{{ Math.abs(overview.todoTrend) }}%</span>
              <el-icon><component :is="overview.todoTrend > 0 ? 'ArrowUp' : 'ArrowDown'" /></el-icon>
            </div>
          </div>
          <div class="card-footer">
            <el-link type="primary" @click="handleViewTodos">查看详情</el-link>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="mt-4">
      <el-col :span="16">
        <el-card shadow="hover">
          <template #header>
            <div class="chart-header">
              <span>营业趋势</span>
              <el-radio-group v-model="revenueChartType" size="small">
                <el-radio-button label="week">本周</el-radio-button>
                <el-radio-button label="month">本月</el-radio-button>
                <el-radio-button label="year">本年</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div ref="revenueChartRef" style="width: 100%; height: 350px" />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>
            <div class="chart-header">
              <span>商品分类占比</span>
            </div>
          </template>
          <div ref="categoryChartRef" style="width: 100%; height: 350px" />
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-4">
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div class="chart-header">
              <span>库存预警商品</span>
              <el-button type="primary" link @click="handleViewWarnings">
                查看全部
              </el-button>
            </div>
          </template>
          <el-table :data="warningProducts" style="width: 100%">
            <el-table-column prop="name" label="商品名称" />
            <el-table-column prop="category" label="分类" width="100" />
            <el-table-column prop="stock" label="当前库存" width="100" align="right" />
            <el-table-column prop="warning" label="预警类型" width="100">
              <template #default="{ row }">
                <el-tag :type="getWarningType(row.warning)">
                  {{ row.warning }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div class="chart-header">
              <span>待处理事项</span>
              <el-button type="primary" link @click="handleViewTodos">
                查看全部
              </el-button>
            </div>
          </template>
          <el-table :data="todoItems" style="width: 100%">
            <el-table-column prop="type" label="类型" width="100">
              <template #default="{ row }">
                <el-tag :type="getTodoType(row.type)">
                  {{ row.type }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="content" label="内容" />
            <el-table-column prop="time" label="时间" width="180" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <!-- 预警信息抽屉 -->
    <el-drawer
      v-model="warningDrawer.visible"
      title="库存预警详情"
      size="60%"
    >
      <el-table :data="warningDrawer.data" style="width: 100%">
        <el-table-column prop="name" label="商品名称" />
        <el-table-column prop="category" label="分类" width="100" />
        <el-table-column prop="stock" label="当前库存" width="100" align="right" />
        <el-table-column prop="warning" label="预警类型" width="100">
          <template #default="{ row }">
            <el-tag :type="getWarningType(row.warning)">
              {{ row.warning }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="suggestion" label="建议" />
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleWarningAction(row)">
              处理
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-drawer>

    <!-- 待办事项抽屉 -->
    <el-drawer
      v-model="todoDrawer.visible"
      title="待处理事项"
      size="60%"
    >
      <el-table :data="todoDrawer.data" style="width: 100%">
        <el-table-column prop="type" label="类型" width="100">
          <template #default="{ row }">
            <el-tag :type="getTodoType(row.type)">
              {{ row.type }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="content" label="内容" />
        <el-table-column prop="time" label="时间" width="180" />
        <el-table-column prop="priority" label="优先级" width="100">
          <template #default="{ row }">
            <el-tag :type="getPriorityType(row.priority)">
              {{ row.priority }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleTodoAction(row)">
              处理
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'
import type { EChartsOption } from 'echarts'
import {
  Money,
  Document,
  Warning,
  Bell,
  ArrowUp,
  ArrowDown
} from '@element-plus/icons-vue'

const router = useRouter()

// 图表引用
const revenueChartRef = ref<HTMLElement>()
const categoryChartRef = ref<HTMLElement>()

// 图表实例
let revenueChart: echarts.ECharts | null = null
let categoryChart: echarts.ECharts | null = null

// 概览数据
const overview = ref({
  todayRevenue: 158600,
  yesterdayRevenue: 145200,
  revenueTrend: 9.2,
  todayOrders: 256,
  yesterdayOrders: 238,
  ordersTrend: 7.5,
  warningCount: 12,
  warningTrend: -15,
  todoCount: 8,
  todoTrend: -25
})

// 营业趋势图表类型
const revenueChartType = ref('week')

// 预警商品列表
const warningProducts = ref([
  {
    name: '西红柿',
    category: '蔬菜',
    stock: 50,
    warning: '库存不足'
  },
  {
    name: '苹果',
    category: '水果',
    stock: 1000,
    warning: '库存过剩'
  },
  {
    name: '猪肉',
    category: '肉类',
    stock: 80,
    warning: '临期预警'
  }
])

// 待办事项列表
const todoItems = ref([
  {
    type: '质检',
    content: '新到货苹果批次质量检查',
    time: '2024-01-20 10:00'
  },
  {
    type: '配送',
    content: '城区3号线路配送延迟',
    time: '2024-01-20 09:30'
  },
  {
    type: '报损',
    content: '待处理报损申请 3 件',
    time: '2024-01-20 09:00'
  }
])

// 预警抽屉
const warningDrawer = ref({
  visible: false,
  data: [] as any[]
})

// 待办抽屉
const todoDrawer = ref({
  visible: false,
  data: [] as any[]
})

// 初始化图表
const initCharts = () => {
  // 营业趋势图表
  if (revenueChartRef.value) {
    revenueChart = echarts.init(revenueChartRef.value)
    const revenueOption: EChartsOption = {
      tooltip: {
        trigger: 'axis'
      },
      legend: {
        data: ['营业额', '订单数']
      },
      xAxis: {
        type: 'category',
        data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
      },
      yAxis: [
        {
          type: 'value',
          name: '金额(元)'
        },
        {
          type: 'value',
          name: '订单数',
          position: 'right'
        }
      ],
      series: [
        {
          name: '营业额',
          type: 'line',
          smooth: true,
          data: [150000, 145000, 160000, 155000, 165000, 180000, 170000]
        },
        {
          name: '订单数',
          type: 'bar',
          yAxisIndex: 1,
          data: [220, 210, 240, 230, 250, 270, 260]
        }
      ]
    }
    revenueChart.setOption(revenueOption)
  }

  // 商品分类占比图表
  if (categoryChartRef.value) {
    categoryChart = echarts.init(categoryChartRef.value)
    const categoryOption: EChartsOption = {
      tooltip: {
        trigger: 'item'
      },
      legend: {
        orient: 'vertical',
        left: 'left'
      },
      series: [
        {
          name: '商品分类',
          type: 'pie',
          radius: '50%',
          data: [
            { value: 35, name: '蔬菜' },
            { value: 30, name: '水果' },
            { value: 25, name: '肉类' },
            { value: 10, name: '其他' }
          ],
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
      ]
    }
    categoryChart.setOption(categoryOption)
  }
}

// 处理窗口大小变化
const handleResize = () => {
  revenueChart?.resize()
  categoryChart?.resize()
}

// 格式化数字
const formatNumber = (num: number) => {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

// 获取预警类型样式
const getWarningType = (type: string) => {
  const types: Record<string, string> = {
    '库存不足': 'danger',
    '库存过剩': 'warning',
    '临期预警': 'info'
  }
  return types[type] || ''
}

// 获取待办类型样式
const getTodoType = (type: string) => {
  const types: Record<string, string> = {
    '质检': 'success',
    '配送': 'warning',
    '报损': 'danger'
  }
  return types[type] || ''
}

// 获取优先级样式
const getPriorityType = (priority: string) => {
  const types: Record<string, string> = {
    '高': 'danger',
    '中': 'warning',
    '低': 'info'
  }
  return types[priority] || ''
}

// 查看预警详情
const handleViewWarnings = () => {
  warningDrawer.value.data = [
    {
      name: '西红柿',
      category: '蔬菜',
      stock: 50,
      warning: '库存不足',
      suggestion: '建议补货 200kg'
    },
    {
      name: '苹果',
      category: '水果',
      stock: 1000,
      warning: '库存过剩',
      suggestion: '建议促销处理'
    },
    {
      name: '猪肉',
      category: '肉类',
      stock: 80,
      warning: '临期预警',
      suggestion: '建议优先配送'
    }
  ]
  warningDrawer.value.visible = true
}

// 查看待办详情
const handleViewTodos = () => {
  todoDrawer.value.data = [
    {
      type: '质检',
      content: '新到货苹果批次质量检查',
      time: '2024-01-20 10:00',
      priority: '高'
    },
    {
      type: '配送',
      content: '城区3号线路配送延迟',
      time: '2024-01-20 09:30',
      priority: '中'
    },
    {
      type: '报损',
      content: '待处理报损申请 3 件',
      time: '2024-01-20 09:00',
      priority: '低'
    }
  ]
  todoDrawer.value.visible = true
}

// 处理预警操作
const handleWarningAction = (row: any) => {
  // TODO: 根据预警类型跳转到相应的处理页面
  console.log('Handle warning:', row)
}

// 处理待办操作
const handleTodoAction = (row: any) => {
  // TODO: 根据待办类型跳转到相应的处理页面
  console.log('Handle todo:', row)
}

// 监听营业趋势图表类型变化
watch(revenueChartType, (newType) => {
  if (!revenueChart) return

  const data = {
    week: {
      xAxis: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
      revenue: [150000, 145000, 160000, 155000, 165000, 180000, 170000],
      orders: [220, 210, 240, 230, 250, 270, 260]
    },
    month: {
      xAxis: Array.from({ length: 30 }, (_, i) => `${i + 1}日`),
      revenue: Array.from({ length: 30 }, () => Math.floor(Math.random() * 50000) + 140000),
      orders: Array.from({ length: 30 }, () => Math.floor(Math.random() * 100) + 200)
    },
    year: {
      xAxis: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
      revenue: Array.from({ length: 12 }, () => Math.floor(Math.random() * 1000000) + 4000000),
      orders: Array.from({ length: 12 }, () => Math.floor(Math.random() * 3000) + 6000)
    }
  }[newType]

  revenueChart.setOption({
    xAxis: {
      data: data.xAxis
    },
    series: [
      {
        name: '营业额',
        data: data.revenue
      },
      {
        name: '订单数',
        data: data.orders
      }
    ]
  })
})

// 生命周期钩子
onMounted(() => {
  initCharts()
  window.addEventListener('resize', handleResize)
})

// 组件卸载时清理
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  revenueChart?.dispose()
  categoryChart?.dispose()
})
</script>

<style scoped lang="scss">
.dashboard {
  padding: 20px;

  .overview-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;

      .title {
        font-size: 16px;
        color: #606266;
      }

      .icon {
        font-size: 24px;
        color: #409EFF;
      }
    }

    .card-content {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      margin-bottom: 10px;

      .value {
        font-size: 24px;
        font-weight: bold;
        color: #303133;

        &.warning {
          color: #E6A23C;
        }
      }

      .trend {
        display: flex;
        align-items: center;
        font-size: 14px;

        &.up {
          color: #67C23A;
        }

        &.down {
          color: #F56C6C;
        }

        .el-icon {
          margin-left: 4px;
        }
      }
    }

    .card-footer {
      font-size: 14px;
      color: #909399;
    }
  }

  .chart-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    span {
      font-size: 16px;
      font-weight: bold;
    }
  }

  .mt-4 {
    margin-top: 20px;
  }
}
</style>