<template>
  <report-layout title="配送报表">
    <template #filters>
      <el-form-item label="配送区域">
        <el-select v-model="filterForm.area" clearable placeholder="选择配送区域">
          <el-option
            v-for="item in areas"
            :key="item.id"
            :label="item.name"
            :value="item.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="配送员">
        <el-select v-model="filterForm.deliveryStaff" clearable placeholder="选择配送员">
          <el-option
            v-for="item in deliveryStaff"
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
          title="平均配送时长"
          :value="statistics.avgDeliveryTime"
          unit="分钟"
          :trend="statistics.timeRateRatio"
        />
      </el-col>
      <el-col :span="6">
        <statistic-card
          title="准时率"
          :value="statistics.onTimeRate"
          unit="%"
          :trend="statistics.onTimeRatio"
        />
      </el-col>
      <el-col :span="6">
        <statistic-card
          title="客户满意度"
          :value="statistics.satisfaction"
          unit="分"
          :trend="statistics.satisfactionRatio"
        />
      </el-col>
      <el-col :span="6">
        <statistic-card
          title="配送单量"
          :value="statistics.orderCount"
          unit="单"
          :trend="statistics.orderCountRatio"
        />
      </el-col>
    </template>

    <template #charts>
      <el-row :gutter="20">
        <el-col :span="12">
          <chart-card
            title="配送效率分析"
            :options="efficiencyChartOptions"
            :loading="loading.efficiency"
            @range-change="handleEfficiencyTimeChange"
          />
        </el-col>
        <el-col :span="12">
          <chart-card
            title="客户满意度分析"
            :options="satisfactionChartOptions"
            :loading="loading.satisfaction"
            @range-change="handleSatisfactionTimeChange"
          />
        </el-col>
      </el-row>
      <el-row :gutter="20" class="mt-4">
        <el-col :span="24">
          <chart-card
            title="路线优化分析"
            :options="routeChartOptions"
            :loading="loading.route"
            @range-change="handleRouteTimeChange"
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
        <el-table-column prop="date" label="日期" width="120" />
        <el-table-column prop="area" label="配送区域" />
        <el-table-column prop="staff" label="配送员" />
        <el-table-column prop="orderCount" label="配送单数" />
        <el-table-column prop="avgTime" label="平均配送时长">
          <template #default="{ row }">
            {{ row.avgTime }}分钟
          </template>
        </el-table-column>
        <el-table-column prop="onTimeRate" label="准时率">
          <template #default="{ row }">
            {{ row.onTimeRate }}%
          </template>
        </el-table-column>
        <el-table-column prop="satisfaction" label="满意度">
          <template #default="{ row }">
            <el-rate
              v-model="row.satisfaction"
              disabled
              show-score
              text-color="#ff9900"
            />
          </template>
        </el-table-column>
        <el-table-column prop="distance" label="配送距离">
          <template #default="{ row }">
            {{ row.distance }}km
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
const routeChartOptions = ref<EChartsOption>({
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['配送距离', '配送单数', '单均距离']
  },
  xAxis: {
    type: 'category',
    data: ['路线A', '路线B', '路线C', '路线D', '路线E']
  },
  yAxis: [
    {
      type: 'value',
      name: '距离(km)'
    },
    {
      type: 'value',
      name: '订单数',
      position: 'right'
    }
  ],
  series: [
    {
      name: '配送距离',
      type: 'bar',
      data: [120, 150, 80, 200, 160]
    },
    {
      name: '配送单数',
      type: 'bar',
      data: [20, 25, 15, 30, 22]
    },
    {
      name: '单均距离',
      type: 'line',
      data: [6, 6, 5.3, 6.7, 7.3]
    }
  ]
})

// 加载状态
const loading = ref({
  efficiency: false,
  satisfaction: false,
  route: false,
  table: false
})

// 筛选表单
const filterForm = ref({
  area: '',
  deliveryStaff: '',
  dateRange: [] as string[]
})

// 配送区域数据
const areas = ref([
  { id: 1, name: '城区' },
  { id: 2, name: '郊区' },
  { id: 3, name: '开发区' }
])

// 配送员数据
const deliveryStaff = ref([
  { id: 1, name: '张三' },
  { id: 2, name: '李四' },
  { id: 3, name: '王五' }
])

// 图表选项
const efficiencyChartOptions = ref<EChartsOption>({
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'cross'
    }
  },
  legend: {
    data: ['平均配送时长', '准时率']
  },
  xAxis: {
    type: 'category',
    data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
  },
  yAxis: [
    {
      type: 'value',
      name: '时长(分钟)',
      position: 'left'
    },
    {
      type: 'value',
      name: '准时率(%)',
      position: 'right',
      max: 100
    }
  ],
  series: [
    {
      name: '平均配送时长',
      type: 'bar',
      data: [45, 42, 46, 43, 40, 48, 50]
    },
    {
      name: '准时率',
      type: 'line',
      yAxisIndex: 1,
      data: [95, 96, 94, 95, 97, 93, 92]
    }
  ]
})

const satisfactionChartOptions = ref<EChartsOption>({
  tooltip: {
    trigger: 'item'
  },
  legend: {
    orient: 'vertical',
    left: 'left'
  },
  series: [
    {
      name: '满意度分布',
      type: 'pie',
      radius: '50%',
      data: [
        { value: 60, name: '非常满意' },
        { value: 25, name: '满意' },
        { value: 10, name: '一般' },
        { value: 5, name: '不满意' }
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

// 统计数据
const statistics = ref({
  avgDeliveryTime: 45,
  timeRateTrend: 'down',
  timeRateRatio: 10,
  onTimeRate: 95,
  onTimeTrend: 'up',
  onTimeRatio: 5,
  satisfaction: 4.8,
  satisfactionTrend: 'up',
  satisfactionRatio: 2,
  orderCount: 150,
  orderCountTrend: 'up',
  orderCountRatio: 15
})

// 表格数据
const tableData = ref([
  {
    date: '2024-01-20',
    area: '城区',
    staff: '张三',
    orderCount: 25,
    avgTime: 42,
    onTimeRate: 96,
    satisfaction: 4.8,
    distance: 85
  },
  {
    date: '2024-01-20',
    area: '郊区',
    staff: '李四',
    orderCount: 18,
    avgTime: 50,
    onTimeRate: 94,
    satisfaction: 4.6,
    distance: 120
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
    area: '',
    deliveryStaff: '',
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
const handleEfficiencyTimeChange = (range: string) => {
  loading.value.efficiency = true
  // TODO: 根据时间范围更新配送效率图表数据
  setTimeout(() => {
    loading.value.efficiency = false
  }, 1000)
}

const handleSatisfactionTimeChange = (range: string) => {
  loading.value.satisfaction = true
  // TODO: 根据时间范围更新满意度图表数据
  setTimeout(() => {
    loading.value.satisfaction = false
  }, 1000)
}

const handleRouteTimeChange = (range: string) => {
  loading.value.route = true
  // TODO: 根据时间范围更新路线分析图表数据
  setTimeout(() => {
    loading.value.route = false
  }, 1000)
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
