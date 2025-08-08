<template>
  <report-layout title="报损报表">
    <template #filters>
      <el-form-item label="商品分类">
        <el-select v-model="filterForm.category" clearable placeholder="选择商品分类">
          <el-option
            v-for="item in categories"
            :key="item.id"
            :label="item.name"
            :value="item.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="报损原因">
        <el-select v-model="filterForm.reason" clearable placeholder="选择报损原因">
          <el-option
            v-for="item in reasons"
            :key="item.id"
            :label="item.name"
            :value="item.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="时间范围">
        <el-date-picker
          v-model="filterForm.dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>
    </template>

    <template #statistics>
      <el-col :span="6">
        <statistic-card
          title="报损总金额"
          :value="statistics.totalAmount"
          unit="元"
          :trend="statistics.amountRatio"
        />
      </el-col>
      <el-col :span="6">
        <statistic-card
          title="报损率"
          :value="statistics.damageRate"
          unit="%"
          :trend="statistics.rateRatio"
        />
      </el-col>
      <el-col :span="6">
        <statistic-card
          title="报损批次"
          :value="statistics.batchCount"
          unit="批"
          :trend="statistics.batchRatio"
        />
      </el-col>
      <el-col :span="6">
        <statistic-card
          title="平均处理时长"
          :value="statistics.avgProcessTime"
          unit="小时"
          :trend="statistics.timeRatio"
        />
      </el-col>
    </template>

    <template #charts>
      <el-row :gutter="20">
        <el-col :span="12">
          <chart-card
            title="报损趋势分析"
            :options="trendChartOptions"
            :loading="loading.trend"
            @range-change="handleTrendTimeChange"
          />
        </el-col>
        <el-col :span="12">
          <chart-card
            title="报损原因分布"
            :options="reasonChartOptions"
            :loading="loading.reason"
            @range-change="handleReasonTimeChange"
          />
        </el-col>
      </el-row>
      <el-row :gutter="20" class="mt-4">
        <el-col :span="24">
          <chart-card
            title="商品报损率排名"
            :options="productChartOptions"
            :loading="loading.product"
            @range-change="handleProductTimeChange"
          />
        </el-col>
      </el-row>
    </template>

    <template #table>
      <el-table
        v-loading="loading.table"
        :data="tableData"
        border
        style="width: 100%"
      >
        <el-table-column prop="date" label="报损日期" width="120" />
        <el-table-column prop="category" label="商品分类" />
        <el-table-column prop="product" label="商品名称" />
        <el-table-column prop="quantity" label="报损数量">
          <template #default="{ row }">
            {{ row.quantity }}{{ row.unit }}
          </template>
        </el-table-column>
        <el-table-column prop="amount" label="报损金额">
          <template #default="{ row }">
            ¥{{ row.amount }}
          </template>
        </el-table-column>
        <el-table-column prop="rate" label="报损率">
          <template #default="{ row }">
            <el-progress
              :percentage="row.rate"
              :status="getDamageRateStatus(row.rate)"
            />
          </template>
        </el-table-column>
        <el-table-column prop="reason" label="报损原因">
          <template #default="{ row }">
            <el-tag :type="getReasonTagType(row.reason)">
              {{ row.reason }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="处理状态">
          <template #default="{ row }">
            <el-tag :type="getStatusTagType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>

      <div class="flex justify-end mt-4">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </template>
  </report-layout>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import type { EChartsOption } from 'echarts'
import ReportLayout from '@/components/Report/ReportLayout.vue'
import StatisticCard from '@/components/Report/StatisticCard.vue'
import ChartCard from '@/components/Report/ChartCard.vue'

// 图表选项
const trendChartOptions = ref<EChartsOption>({
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'cross'
    }
  },
  legend: {
    data: ['报损金额', '报损率']
  },
  xAxis: {
    type: 'category',
    data: ['1月', '2月', '3月', '4月', '5月', '6月']
  },
  yAxis: [
    {
      type: 'value',
      name: '金额(元)'
    },
    {
      type: 'value',
      name: '报损率(%)',
      max: 10,
      position: 'right'
    }
  ],
  series: [
    {
      name: '报损金额',
      type: 'bar',
      data: [15000, 14000, 16000, 13000, 12000, 11000]
    },
    {
      name: '报损率',
      type: 'line',
      yAxisIndex: 1,
      data: [3.5, 3.2, 3.8, 3.0, 2.8, 2.5]
    }
  ]
})

const reasonChartOptions = ref<EChartsOption>({
  tooltip: {
    trigger: 'item'
  },
  legend: {
    orient: 'vertical',
    left: 'left'
  },
  series: [
    {
      name: '报损原因',
      type: 'pie',
      radius: '50%',
      data: [
        { value: 40, name: '过期' },
        { value: 25, name: '破损' },
        { value: 20, name: '品质问题' },
        { value: 15, name: '运输损坏' }
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
})

const productChartOptions = ref<EChartsOption>({
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow'
    }
  },
  legend: {
    data: ['报损率', '报损金额']
  },
  xAxis: {
    type: 'value',
    name: '报损率(%)',
    max: 10
  },
  yAxis: {
    type: 'category',
    data: ['西红柿', '苹果', '香蕉', '白菜', '猪肉'].reverse()
  },
  series: [
    {
      name: '报损率',
      type: 'bar',
      data: [5, 4, 3.5, 3, 2.5].reverse()
    },
    {
      name: '报损金额',
      type: 'bar',
      data: [2500, 3000, 2000, 1500, 4000].reverse()
    }
  ]
})

// 加载状态
const loading = ref({
  trend: false,
  reason: false,
  product: false,
  table: false
})

// 筛选表单
const filterForm = ref({
  category: '',
  reason: '',
  dateRange: [] as string[]
})

// 商品分类数据
const categories = ref([
  { id: 1, name: '蔬菜' },
  { id: 2, name: '水果' },
  { id: 3, name: '肉类' }
])

// 报损原因数据
const reasons = ref([
  { id: 1, name: '过期' },
  { id: 2, name: '破损' },
  { id: 3, name: '品质问题' },
  { id: 4, name: '运输损坏' }
])

// 统计数据
const statistics = ref({
  totalAmount: 15800,
  amountTrend: 'down',
  amountRatio: 12,
  damageRate: 2.5,
  rateTrend: 'down',
  rateRatio: 8,
  batchCount: 25,
  batchTrend: 'down',
  batchRatio: 15,
  avgProcessTime: 4.5,
  timeTrend: 'down',
  timeRatio: 10
})

// 表格数据
const tableData = ref([
  {
    date: '2024-01-20',
    category: '蔬菜',
    product: '西红柿',
    quantity: 50,
    unit: 'kg',
    amount: 250,
    rate: 5,
    reason: '过期',
    status: 'processed'
  },
  {
    date: '2024-01-20',
    category: '水果',
    product: '苹果',
    quantity: 30,
    unit: 'kg',
    amount: 300,
    rate: 3,
    reason: '破损',
    status: 'processing'
  }
])

// 分页配置
const pagination = ref({
  page: 1,
  pageSize: 10,
  total: 0
})

// 搜索处理
const handleSearch = () => {
  // TODO: 实现搜索逻辑
  console.log('Search with:', filterForm.value)
}

// 重置处理
const handleReset = () => {
  filterForm.value = {
    category: '',
    reason: '',
    dateRange: []
  }
}

// 分页处理
const handleSizeChange = (size: number) => {
  pagination.value.pageSize = size
  // TODO: 重新加载数据
}

const handlePageChange = (page: number) => {
  pagination.value.page = page
  // TODO: 重新加载数据
}

// 时间范围变化处理
const handleTrendTimeChange = (range: string) => {
  loading.value.trend = true
  // TODO: 根据时间范围更新趋势图表数据
  setTimeout(() => {
    loading.value.trend = false
  }, 1000)
}

const handleReasonTimeChange = (range: string) => {
  loading.value.reason = true
  // TODO: 根据时间范围更新原因分布图表数据
  setTimeout(() => {
    loading.value.reason = false
  }, 1000)
}

const handleProductTimeChange = (range: string) => {
  loading.value.product = true
  // TODO: 根据时间范围更新商品报损率图表数据
  setTimeout(() => {
    loading.value.product = false
  }, 1000)
}

// 报损率状态处理
const getDamageRateStatus = (rate: number): '' | 'success' | 'warning' | 'exception' => {
  if (rate <= 2) return 'success'
  if (rate <= 5) return 'warning'
  return 'exception'
}

// 原因标签类型处理
const getReasonTagType = (reason: string): '' | 'success' | 'warning' | 'danger' => {
  const types: Record<string, '' | 'success' | 'warning' | 'danger'> = {
    '过期': 'danger',
    '破损': 'warning',
    '品质问题': 'warning',
    '运输损坏': ''
  }
  return types[reason] || ''
}

// 状态标签类型处理
const getStatusTagType = (status: string): '' | 'success' | 'warning' | 'info' => {
  const types: Record<string, '' | 'success' | 'warning' | 'info'> = {
    processed: 'success',
    processing: 'warning',
    pending: 'info'
  }
  return types[status] || ''
}

// 状态文本处理
const getStatusText = (status: string): string => {
  const texts: Record<string, string> = {
    processed: '已处理',
    processing: '处理中',
    pending: '待处理'
  }
  return texts[status] || '未知'
}

// 生命周期钩子
onMounted(() => {
  // 图表由 ChartCard 组件自动处理
})
</script>

<style scoped>
.mt-4 {
  margin-top: 1rem;
}
.flex {
  display: flex;
}
.justify-end {
  justify-content: flex-end;
}
</style>
