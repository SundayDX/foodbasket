<template>
  <el-col :span="span">
    <div class="chart-card card">
      <div class="card-header">
        <div class="header-left">
          <h3>{{ title }}</h3>
          <el-tooltip
            v-if="tooltip"
            :content="tooltip"
            placement="top"
            effect="dark"
          >
            <el-icon class="tooltip-icon"><QuestionFilled /></el-icon>
          </el-tooltip>
        </div>
        <div class="header-right">
          <slot name="actions">
            <el-radio-group
              v-if="timeRanges.length"
              v-model="selectedRange"
              size="small"
              @change="handleRangeChange"
            >
              <el-radio-button
                v-for="range in timeRanges"
                :key="range.value"
                :label="range.value"
              >
                {{ range.label }}
              </el-radio-button>
            </el-radio-group>
          </slot>
        </div>
      </div>
      <div class="card-body">
        <div
          v-if="loading"
          class="chart-loading"
        >
          <el-icon class="loading-icon"><Loading /></el-icon>
          加载中...
        </div>
        <div
          v-else-if="error"
          class="chart-error"
        >
          <el-icon class="error-icon"><Warning /></el-icon>
          {{ error }}
        </div>
        <div
          v-else
          ref="chartRef"
          class="chart-container"
          :style="{ height: height + 'px', width: '100%' }"
        ></div>
      </div>
    </div>
  </el-col>
</template>

<script setup lang="ts">
import {
  ref,
  onMounted,
  onUnmounted,
  watch,
  nextTick
} from 'vue'
import {
  QuestionFilled,
  Loading,
  Warning
} from '@element-plus/icons-vue'
import echarts from '@/utils/echarts'
import type { EChartsType, EChartsOption } from 'echarts/core'

interface TimeRange {
  label: string
  value: string
}

interface Props {
  title: string
  tooltip?: string
  options: EChartsOption
  loading?: boolean
  error?: string
  height?: number
  span?: number
  timeRanges?: TimeRange[]
}

const props = withDefaults(defineProps<Props>(), {
  tooltip: '',
  loading: false,
  error: '',
  height: 300,
  span: 12,
  timeRanges: () => []
})

const emit = defineEmits<{
  (e: 'range-change', range: string): void
}>()

// 图表实例
const chartRef = ref<HTMLElement>()
let chart: EChartsType | null = null

// 时间范围选择
const selectedRange = ref(props.timeRanges[0]?.value || '')

// 初始化图表
onMounted(async () => {
  await nextTick()
  if (props.options) {
    initChart()
  }
  window.addEventListener('resize', handleResize)
})

// 销毁图表
onUnmounted(() => {
  if (chart) {
    chart.dispose()
    chart = null
  }
  window.removeEventListener('resize', handleResize)
})

// 监听选项变化
watch(
  () => props.options,
  (newOptions) => {
    if (chart && newOptions) {
      chart.setOption(newOptions, true)
    }
  },
  { deep: true }
)

// 初始化图表
const initChart = () => {
  if (!chartRef.value || !props.options) {
    console.log('ChartCard: 无法初始化图表', { chartRef: !!chartRef.value, options: !!props.options })
    return
  }
  console.log('ChartCard: 初始化图表', props.title, props.options)
  chart = echarts.init(chartRef.value)
  chart.setOption(props.options)
}

// 处理窗口大小变化
const handleResize = () => {
  chart?.resize()
}

// 处理时间范围变化
const handleRangeChange = (range: string) => {
  emit('range-change', range)
}

// 暴露方法给父组件
defineExpose({
  getChart: () => chart
})
</script>

<style lang="scss" scoped>
.chart-card {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: $spacing-base;

    .header-left {
      display: flex;
      align-items: center;
      gap: 4px;

      h3 {
        margin: 0;
        font-size: 16px;
        font-weight: 600;
      }

      .tooltip-icon {
        font-size: 14px;
        color: $text-secondary;
        cursor: help;
      }
    }
  }

  .card-body {
    position: relative;

    .chart-loading,
    .chart-error {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      color: $text-secondary;
      font-size: 14px;
      background-color: rgba(255, 255, 255, 0.9);
      z-index: 1;

      .loading-icon {
        font-size: 24px;
        margin-bottom: $spacing-small;
        animation: rotating 2s linear infinite;
      }

      .error-icon {
        font-size: 24px;
        margin-bottom: $spacing-small;
        color: $danger-color;
      }
    }
  }
}

@keyframes rotating {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>