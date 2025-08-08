<template>
  <report-layout title="库存报表">
    <template #filters>
      <el-form-item label="商品分类">
        <el-select v-model="filterForm.categoryId" clearable placeholder="选择商品分类">
          <el-option
            v-for="item in categories"
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
           title="库存周转"
           :value="statistics.turnoverRate"
           unit="次"
           :trend="statistics.turnoverRatio"
         />
       </el-col>
       <el-col :span="6">
         <statistic-card
           title="平均库存天"
           :value="statistics.avgDays"
           unit="天"
           :trend="statistics.daysRatio"
         />
       </el-col>
       <el-col :span="6">
         <statistic-card
           title="库存预警商品"
           :value="statistics.warningCount"
           unit="个"
           :trend="statistics.warningRatio"
         />
       </el-col>
       <el-col :span="6">
         <statistic-card
           title="库存价值"
           :value="statistics.totalValue"
           unit="元"
           :trend="statistics.valueRatio"
         />
       </el-col>
     </template>

    <template #charts>
      <el-row :gutter="20">
        <el-col :span="12">
          <chart-card
            title="库存周转分析"
            :options="turnoverChartOptions"
            :loading="loading.turnover"
            @range-change="handleTurnoverTimeChange"
          />
        </el-col>
        <el-col :span="12">
          <chart-card
            title="库存预警分析"
            :options="warningChartOptions"
            :loading="loading.warning"
            @range-change="handleWarningTimeChange"
          />
        </el-col>
      </el-row>
      <el-row :gutter="20" class="mt-4">
        <el-col :span="24">
          <chart-card
            title="库存趋势分析"
            :options="trendChartOptions"
            :loading="loading.trend"
            @range-change="handleTrendTimeChange"
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
        <el-table-column prop="name" label="商品名称" />
        <el-table-column prop="category" label="商品分类" />
        <el-table-column prop="quantity" label="当前库存" />
        <el-table-column prop="turnoverRate" label="周转率">
          <template #default="{ row }">
            {{ row.turnoverRate }}次/年
          </template>
        </el-table-column>
        <el-table-column prop="avgDays" label="平均库存天数">
          <template #default="{ row }">
            {{ row.avgDays }}天
          </template>
        </el-table-column>
        <el-table-column prop="warningLevel" label="预警状态">
          <template #default="{ row }">
            <el-tag :type="getWarningTagType(row.warningLevel)">
              {{ getWarningText(row.warningLevel) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="value" label="库存价值">
          <template #default="{ row }">
            ¥{{ row.value }}
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
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import type { EChartsOption } from 'echarts'
import ReportLayout from '@/components/Report/ReportLayout.vue'
import StatisticCard from '@/components/Report/StatisticCard.vue'
import ChartCard from '@/components/Report/ChartCard.vue'

// 图表选项
const turnoverChartOptions = ref<EChartsOption>({
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['周转率', '平均库存天数']
  },
  xAxis: {
    type: 'category',
    data: ['1月', '2月', '3月', '4月', '5月', '6月']
  },
  yAxis: [
    {
      type: 'value',
      name: '周转率',
      position: 'left'
    },
    {
      type: 'value',
      name: '天数',
      position: 'right'
    }
  ],
  series: [
    {
      name: '周转率',
      type: 'line',
      data: [12, 13, 15, 14, 16, 15]
    },
    {
      name: '平均库存天数',
      type: 'line',
      yAxisIndex: 1,
      data: [30, 28, 25, 26, 24, 25]
    }
  ]
})

const warningChartOptions = ref<EChartsOption>({
  tooltip: {
    trigger: 'item'
  },
  legend: {
    orient: 'vertical',
    left: 'left'
  },
  series: [
    {
      name: '预警状态',
      type: 'pie',
      radius: '50%',
      data: [
        { value: 5, name: '库存不足' },
        { value: 3, name: '库存过剩' },
        { value: 15, name: '正常' }
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

const trendChartOptions = ref<EChartsOption>({
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['库存数量', '库存金额']
  },
  xAxis: {
    type: 'category',
    data: ['1月', '2月', '3月', '4月', '5月', '6月']
  },
  yAxis: [
    {
      type: 'value',
      name: '数量'
    },
    {
      type: 'value',
      name: '金额',
      position: 'right'
    }
  ],
  series: [
    {
      name: '库存数量',
      type: 'bar',
      data: [1500, 1600, 1800, 1700, 1900, 2000]
    },
    {
      name: '库存金额',
      type: 'line',
      yAxisIndex: 1,
      data: [120000, 130000, 150000, 140000, 160000, 170000]
    }
  ]
})

// 加载状态
const loading = ref({
  turnover: false,
  warning: false,
  trend: false,
  table: false
})

// 筛选表单
const filterForm = ref({
  categoryId: '',
  dateRange: [] as string[]
})

// 统计数据
const statistics = ref({
  turnoverRate: 1,
  turnoverTrend: 'up',
  turnoverRatio: 15,
  avgDays: 2,
  daysTrend: 'down',
  daysRatio: 10,
  warningCount: 5,
  warningTrend: 'up',
  warningRatio: 25,
  totalValue: 1,
  valueTrend: 'up',
  valueRatio: 8
})

// 分类数据
const categories = ref([
  { id: 1, name: '蔬菜' },
  { id: 2, name: '水果' },
  { id: 3, name: '肉类' }
])

// 表格数据
const tableData = ref([
  {
    name: '西红柿',
    category: '蔬菜',
    quantity: 1000,
    turnoverRate: 15.2,
    avgDays: 25,
    warningLevel: 'normal',
    value: 5000
  },
  {
    name: '苹果',
    category: '水果',
    quantity: 500,
    turnoverRate: 10.5,
    avgDays: 35,
    warningLevel: 'warning',
    value: 8000
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
    categoryId: '',
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
const handleTurnoverTimeChange = (range: string) => {
  loading.value.turnover = true
  // TODO: 根据时间范围更新周转率图表数据
  setTimeout(() => {
    loading.value.turnover = false
  }, 1000)
}

const handleWarningTimeChange = (range: string) => {
  loading.value.warning = true
  // TODO: 根据时间范围更新预警图表数据
  setTimeout(() => {
    loading.value.warning = false
  }, 1000)
}

const handleTrendTimeChange = (range: string) => {
  loading.value.trend = true
  // TODO: 根据时间范围更新趋势图表数据
  setTimeout(() => {
    loading.value.trend = false
  }, 1000)
}

// 预警状态处理
const getWarningTagType = (level: string) => {
  const types: Record<string, string> = {
    normal: 'success',
    warning: 'warning',
    danger: 'danger'
  }
  return types[level] || 'info'
}

const getWarningText = (level: string) => {
  const texts: Record<string, string> = {
    normal: '正常',
    warning: '预警',
    danger: '严重'
  }
  return texts[level] || '未知'
}

// 生命周期钩子
onMounted(() => {
  // 图表组件会自动初始化
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
