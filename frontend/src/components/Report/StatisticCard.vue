<template>
  <el-col :span="span">
    <div class="statistic-card" :class="type">
      <div class="card-content">
        <div class="card-title">
          {{ title }}
          <el-tooltip
            v-if="tooltip"
            :content="tooltip"
            placement="top"
            effect="dark"
          >
            <el-icon class="tooltip-icon"><QuestionFilled /></el-icon>
          </el-tooltip>
        </div>
        <div class="card-value">
          {{ value }}
          <span v-if="unit" class="unit">{{ unit }}</span>
        </div>
        <div v-if="showTrend" class="card-trend">
          <span
            class="trend-value"
            :class="{ 'up': trend > 0, 'down': trend < 0 }"
          >
            {{ trend > 0 ? '+' : '' }}{{ trend }}%
          </span>
          <span class="trend-label">{{ trendLabel }}</span>
        </div>
      </div>
      <div v-if="showChart" class="card-chart" ref="chartRef"></div>
    </div>
  </el-col>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { QuestionFilled } from '@element-plus/icons-vue'
import echarts from '@/utils/echarts'
import type { EChartsType } from 'echarts/core'

interface Props {
  title: string
  value: string | number
  unit?: string
  tooltip?: string
  type?: 'default' | 'primary' | 'success' | 'warning' | 'danger'
  trend?: number
  trendLabel?: string
  showTrend?: boolean
  showChart?: boolean
  chartData?: number[]
  span?: number
}

const props = withDefaults(defineProps<Props>(), {
  type: 'default',
  unit: '',
  tooltip: '',
  trend: 0,
  trendLabel: '较上期',
  showTrend: true,
  showChart: true,
  chartData: () => [],
  span: 6
})

// 图表相关
const chartRef = ref<HTMLElement>()
let chart: EChartsType | null = null

onMounted(async () => {
  if (props.showChart && props.chartData.length > 0) {
    await nextTick()
    initChart()
  }
})

const initChart = () => {
  if (!chartRef.value) return
  chart = echarts.init(chartRef.value)

  const option = {
    grid: {
      left: 0,
      right: 0,
      top: 0,
      bottom: 0
    },
    xAxis: {
      type: 'category',
      show: false
    },
    yAxis: {
      type: 'value',
      show: false
    },
    series: [
      {
        type: 'line',
        data: props.chartData,
        symbol: 'none',
        smooth: true,
        lineStyle: {
          width: 2,
          color: getChartColor()
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color: getChartColor(0.2)
            },
            {
              offset: 1,
              color: getChartColor(0)
            }
          ])
        }
      }
    ]
  }

  chart.setOption(option)
}

const getChartColor = (alpha = 1) => {
  const colors = {
    default: `rgba(64, 158, 255, ${alpha})`,
    primary: `rgba(64, 158, 255, ${alpha})`,
    success: `rgba(103, 194, 58, ${alpha})`,
    warning: `rgba(230, 162, 60, ${alpha})`,
    danger: `rgba(245, 108, 108, ${alpha})`
  }
  return colors[props.type]
}
</script>

<style lang="scss" scoped>
.statistic-card {
  background-color: #fff;
  border-radius: $border-radius-base;
  padding: $spacing-base;
  height: 120px;
  display: flex;
  position: relative;
  width: 100%;
  min-width: 200px;
  overflow: hidden;
  transition: all 0.3s;
  cursor: pointer;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  }

  &.primary {
    background: linear-gradient(135deg, $primary-color, lighten($primary-color, 15%));
    color: #fff;
  }

  &.success {
    background: linear-gradient(135deg, $success-color, lighten($success-color, 15%));
    color: #fff;
  }

  &.warning {
    background: linear-gradient(135deg, $warning-color, lighten($warning-color, 15%));
    color: #fff;
  }

  &.danger {
    background: linear-gradient(135deg, $danger-color, lighten($danger-color, 15%));
    color: #fff;
  }

  .card-content {
    flex: 1;
    z-index: 1;

    .card-title {
      font-size: 14px;
      margin-bottom: $spacing-small;
      display: flex;
      align-items: center;
      gap: 4px;
      opacity: 0.9;

      .tooltip-icon {
        cursor: help;
      }
    }

    .card-value {
      font-size: 24px;
      font-weight: bold;
      margin-bottom: $spacing-small;

      .unit {
        font-size: 14px;
        font-weight: normal;
        margin-left: 4px;
        opacity: 0.8;
      }
    }

    .card-trend {
      font-size: 12px;
      opacity: 0.9;

      .trend-value {
        &.up {
          color: #fff;
        }

        &.down {
          color: #fff;
        }
      }

      .trend-label {
        margin-left: 4px;
      }
    }
  }

  .card-chart {
    position: absolute;
    right: 0;
    bottom: 0;
    width: 100px;
    height: 40px;
    opacity: 0.2;
  }

  &:not(.primary):not(.success):not(.warning):not(.danger) {
    border: 1px solid $border-color-light;

    .card-trend {
      .trend-value {
        &.up {
          color: $success-color;
        }

        &.down {
          color: $danger-color;
        }
      }

      .trend-label {
        color: $text-secondary;
      }
    }
  }
}
</style>