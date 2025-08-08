<template>
  <report-layout>
    <template #filter>
      <el-form :inline="true" :model="filterForm">
        <el-form-item label="供应商">
          <el-select v-model="filterForm.supplier" clearable placeholder="选择供应商">
            <el-option
              v-for="item in suppliers"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
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
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </template>

    <template #statistics>
      <el-row :gutter="20">
        <el-col :span="6">
          <statistic-card
            title="质检合格率"
            :value="statistics.passRate"
            unit="%"
            :trend="statistics.passRateTrend"
            :trend-ratio="statistics.passRateRatio"
          />
        </el-col>
        <el-col :span="6">
          <statistic-card
            title="平均质检得分"
            :value="statistics.avgScore"
            unit="分"
            :trend="statistics.scoreTrend"
            :trend-ratio="statistics.scoreRatio"
          />
        </el-col>
        <el-col :span="6">
          <statistic-card
            title="问题批次数"
            :value="statistics.issueCount"
            unit="批"
            :trend="statistics.issueTrend"
            :trend-ratio="statistics.issueRatio"
          />
        </el-col>
        <el-col :span="6">
          <statistic-card
            title="质检任务完成率"
            :value="statistics.completionRate"
            unit="%"
            :trend="statistics.completionTrend"
            :trend-ratio="statistics.completionRatio"
          />
        </el-col>
      </el-row>
    </template>

    <template #charts>
      <el-row :gutter="20">
        <el-col :span="12">
          <chart-card
            title="质检合格率趋势"
            :loading="loading.passRate"
            @timeChange="handlePassRateTimeChange"
          >
            <div ref="passRateChartRef" style="width: 100%; height: 300px" />
          </chart-card>
        </el-col>
        <el-col :span="12">
          <chart-card
            title="问题类型分布"
            :loading="loading.issueTypes"
            @timeChange="handleIssueTypesTimeChange"
          >
            <div ref="issueTypesChartRef" style="width: 100%; height: 300px" />
          </chart-card>
        </el-col>
      </el-row>
      <el-row :gutter="20" class="mt-4">
        <el-col :span="24">
          <chart-card
            title="供应商质量评分"
            :loading="loading.supplier"
            @timeChange="handleSupplierTimeChange"
          >
            <div ref="supplierChartRef" style="width: 100%; height: 300px" />
          </chart-card>
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
        <el-table-column prop="date" label="检查日期" width="120" />
        <el-table-column prop="supplier" label="供应商" />
        <el-table-column prop="category" label="商品分类" />
        <el-table-column prop="batchNo" label="批次号" width="120" />
        <el-table-column prop="passRate" label="合格率">
          <template #default="{ row }">
            <el-progress
              :percentage="row.passRate"
              :status="getPassRateStatus(row.passRate)"
            />
          </template>
        </el-table-column>
        <el-table-column prop="score" label="质检得分">
          <template #default="{ row }">
            {{ row.score }}分
          </template>
        </el-table-column>
        <el-table-column prop="issues" label="问题类型">
          <template #default="{ row }">
            <el-tag
              v-for="issue in row.issues"
              :key="issue"
              class="mr-1"
              :type="getIssueTagType(issue)"
            >
              {{ issue }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态">
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

// 图表引用
const passRateChartRef = ref<HTMLElement>()
const issueTypesChartRef = ref<HTMLElement>()
const supplierChartRef = ref<HTMLElement>()

// 图表实例
let passRateChart: echarts.ECharts | null = null
let issueTypesChart: echarts.ECharts | null = null
let supplierChart: echarts.ECharts | null = null

// 加载状态
const loading = ref({
  passRate: false,
  issueTypes: false,
  supplier: false,
  table: false
})

// 筛选表单
const filterForm = ref({
  supplier: '',
  category: '',
  dateRange: [] as string[]
})

// 供应商数据
const suppliers = ref([
  { id: 1, name: '供应商A' },
  { id: 2, name: '供应商B' },
  { id: 3, name: '供应商C' }
])

// 商品分类数据
const categories = ref([
  { id: 1, name: '蔬菜' },
  { id: 2, name: '水果' },
  { id: 3, name: '肉类' }
])

// 统计数据
const statistics = ref({
  passRate: 95.5,
  passRateTrend: 'up',
  passRateRatio: 2.5,
  avgScore: 92,
  scoreTrend: 'up',
  scoreRatio: 3,
  issueCount: 8,
  issueTrend: 'down',
  issueRatio: 15,
  completionRate: 98,
  completionTrend: 'up',
  completionRatio: 1
})

// 表格数据
const tableData = ref([
  {
    date: '2024-01-20',
    supplier: '供应商A',
    category: '蔬菜',
    batchNo: 'QC20240120001',
    passRate: 96,
    score: 94,
    issues: ['外观', '包装'],
    status: 'passed'
  },
  {
    date: '2024-01-20',
    supplier: '供应商B',
    category: '水果',
    batchNo: 'QC20240120002',
    passRate: 88,
    score: 85,
    issues: ['新鲜度', '规格'],
    status: 'warning'
  }
])

// 分页配置
const pagination = ref({
  page: 1,
  pageSize: 10,
  total: 0
})

// 初始化图表
const initCharts = () => {
  // 质检合格率趋势图表
  if (passRateChartRef.value) {
    passRateChart = echarts.init(passRateChartRef.value)
    const passRateOption: EChartsOption = {
      tooltip: {
        trigger: 'axis'
      },
      legend: {
        data: ['合格率', '平均得分']
      },
      xAxis: {
        type: 'category',
        data: ['1月', '2月', '3月', '4月', '5月', '6月']
      },
      yAxis: [
        {
          type: 'value',
          name: '百分比',
          max: 100
        },
        {
          type: 'value',
          name: '得分',
          max: 100
        }
      ],
      series: [
        {
          name: '合格率',
          type: 'line',
          data: [95, 93, 96, 94, 95, 97]
        },
        {
          name: '平均得分',
          type: 'line',
          yAxisIndex: 1,
          data: [92, 90, 93, 91, 94, 95]
        }
      ]
    }
    passRateChart.setOption(passRateOption)
  }

  // 问题类型分布图表
  if (issueTypesChartRef.value) {
    issueTypesChart = echarts.init(issueTypesChartRef.value)
    const issueTypesOption: EChartsOption = {
      tooltip: {
        trigger: 'item'
      },
      legend: {
        orient: 'vertical',
        left: 'left'
      },
      series: [
        {
          name: '问题类型',
          type: 'pie',
          radius: '50%',
          data: [
            { value: 30, name: '新鲜度' },
            { value: 25, name: '外观' },
            { value: 20, name: '规格' },
            { value: 15, name: '包装' },
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
    issueTypesChart.setOption(issueTypesOption)
  }

  // 供应商质量评分图表
  if (supplierChartRef.value) {
    supplierChart = echarts.init(supplierChartRef.value)
    const supplierOption: EChartsOption = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      legend: {
        data: ['合格率', '平均得分', '问题批次']
      },
      xAxis: {
        type: 'category',
        data: ['供应商A', '供应商B', '供应商C', '供应商D', '供应商E']
      },
      yAxis: [
        {
          type: 'value',
          name: '百分比/得分',
          max: 100
        },
        {
          type: 'value',
          name: '批次数',
          position: 'right'
        }
      ],
      series: [
        {
          name: '合格率',
          type: 'bar',
          data: [95, 88, 92, 90, 94]
        },
        {
          name: '平均得分',
          type: 'bar',
          data: [92, 85, 89, 87, 91]
        },
        {
          name: '问题批次',
          type: 'line',
          yAxisIndex: 1,
          data: [2, 5, 3, 4, 2]
        }
      ]
    }
    supplierChart.setOption(supplierOption)
  }
}

// 处理窗口大小变化
const handleResize = () => {
  passRateChart?.resize()
  issueTypesChart?.resize()
  supplierChart?.resize()
}

// 搜索处理
const handleSearch = () => {
  // TODO: 实现搜索逻辑
  console.log('Search with:', filterForm.value)
}

// 重置处理
const handleReset = () => {
  filterForm.value = {
    supplier: '',
    category: '',
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
const handlePassRateTimeChange = (range: string) => {
  loading.value.passRate = true
  // TODO: 根据时间范围更新合格率图表数据
  setTimeout(() => {
    loading.value.passRate = false
  }, 1000)
}

const handleIssueTypesTimeChange = (range: string) => {
  loading.value.issueTypes = true
  // TODO: 根据时间范围更新问题类型图表数据
  setTimeout(() => {
    loading.value.issueTypes = false
  }, 1000)
}

const handleSupplierTimeChange = (range: string) => {
  loading.value.supplier = true
  // TODO: 根据时间范围更新供应商图表数据
  setTimeout(() => {
    loading.value.supplier = false
  }, 1000)
}

// 合格率状态处理
const getPassRateStatus = (rate: number): '' | 'success' | 'warning' | 'exception' => {
  if (rate >= 95) return 'success'
  if (rate >= 90) return 'warning'
  return 'exception'
}

// 问题标签类型处理
const getIssueTagType = (issue: string): '' | 'success' | 'warning' | 'danger' => {
  const types: Record<string, '' | 'success' | 'warning' | 'danger'> = {
    '新鲜度': 'danger',
    '外观': 'warning',
    '规格': 'warning',
    '包装': '',
    '其他': ''
  }
  return types[issue] || ''
}

// 状态标签类型处理
const getStatusTagType = (status: string): '' | 'success' | 'warning' | 'danger' => {
  const types: Record<string, '' | 'success' | 'warning' | 'danger'> = {
    passed: 'success',
    warning: 'warning',
    failed: 'danger'
  }
  return types[status] || ''
}

// 状态文本处理
const getStatusText = (status: string): string => {
  const texts: Record<string, string> = {
    passed: '通过',
    warning: '警告',
    failed: '不合格'
  }
  return texts[status] || '未知'
}

// 生命周期钩子
onMounted(() => {
  initCharts()
  window.addEventListener('resize', handleResize)
})

// 组件卸载时清理
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  passRateChart?.dispose()
  issueTypesChart?.dispose()
  supplierChart?.dispose()
})
</script>

<style scoped>
.mt-4 {
  margin-top: 1rem;
}
.mr-1 {
  margin-right: 0.25rem;
}
.flex {
  display: flex;
}
.justify-end {
  justify-content: flex-end;
}
</style>
