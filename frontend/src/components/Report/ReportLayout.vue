<template>
  <div class="report-layout">
    <!-- 报表头部 -->
    <div class="report-header card">
      <div class="header-content">
        <div class="header-left">
          <h2>{{ title }}</h2>
          <el-tag v-if="subtitle" class="subtitle">{{ subtitle }}</el-tag>
        </div>
        <div class="header-actions">
          <slot name="actions">
            <el-button-group>
              <el-button
                v-for="view in views"
                :key="view.value"
                :type="currentView === view.value ? 'primary' : ''"
                @click="handleViewChange(view.value)"
              >
                {{ view.label }}
              </el-button>
            </el-button-group>
          </slot>
        </div>
      </div>
    </div>

    <!-- 筛选条件 -->
    <div class="report-filter card">
      <el-form
        ref="filterForm"
        :model="filterData"
        :inline="true"
        size="default"
      >
        <slot name="filters" />

        <el-form-item class="filter-actions">
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            查询
          </el-button>
          <el-button @click="handleReset">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
          <el-dropdown
            v-if="exportOptions && exportOptions.length"
            class="export-dropdown"
          >
            <el-button type="success">
              <el-icon><Download /></el-icon>
              导出
              <el-icon class="el-icon--right"><ArrowDown /></el-icon>
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item
                  v-for="option in exportOptions"
                  :key="option.value"
                  @click="handleExport(option.value)"
                >
                  <el-icon><component :is="option.icon" /></el-icon>
                  {{ option.label }}
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </el-form-item>
      </el-form>
    </div>

    <!-- 统计卡片 -->
    <div v-if="$slots.statistics" class="report-statistics">
      <el-row :gutter="20">
        <slot name="statistics" />
      </el-row>
    </div>

    <!-- 图表区域 -->
    <div v-if="$slots.charts" class="report-charts">
      <el-row :gutter="20">
        <slot name="charts" />
      </el-row>
    </div>

    <!-- 数据表格 -->
    <div class="report-table card">
      <slot name="table" />
    </div>

    <!-- 分页 -->
    <div v-if="showPagination" class="report-pagination">
      <el-pagination
        v-model:current-page="pagination.currentPage"
        v-model:page-size="pagination.pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import {
  Search,
  Refresh,
  Download,
  ArrowDown
} from '@element-plus/icons-vue'
import type { FormInstance } from 'element-plus'

interface Props {
  title: string
  subtitle?: string
  views?: Array<{
    label: string
    value: string
  }>
  exportOptions?: Array<{
    label: string
    value: string
    icon: string
  }>
  showPagination?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  subtitle: '',
  views: () => [],
  exportOptions: () => [],
  showPagination: true
})

const emit = defineEmits<{
  (e: 'view-change', view: string): void
  (e: 'search', data: any): void
  (e: 'reset'): void
  (e: 'export', type: string): void
  (e: 'page-change', page: number): void
  (e: 'size-change', size: number): void
}>()

// 视图切换
const currentView = ref(props.views[0]?.value || '')
const handleViewChange = (view: string) => {
  currentView.value = view
  emit('view-change', view)
}

// 筛选表单
const filterForm = ref<FormInstance>()
const filterData = reactive({})

// 查询
const handleSearch = async () => {
  if (!filterForm.value) return
  try {
    await filterForm.value.validate()
    emit('search', filterData)
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}

// 重置
const handleReset = () => {
  if (!filterForm.value) return
  filterForm.value.resetFields()
  emit('reset')
}

// 导出
const handleExport = (type: string) => {
  emit('export', type)
}

// 分页
const pagination = reactive({
  currentPage: 1,
  pageSize: 20,
  total: 0
})

const handleSizeChange = (size: number) => {
  pagination.pageSize = size
  emit('size-change', size)
}

const handleCurrentChange = (page: number) => {
  pagination.currentPage = page
  emit('page-change', page)
}

// 暴露方法给父组件
defineExpose({
  filterData,
  pagination,
  handleSearch,
  handleReset
})
</script>

<style lang="scss" scoped>
.report-layout {
  .report-header {
    margin-bottom: $spacing-base;

    .header-content {
      display: flex;
      justify-content: space-between;
      align-items: center;

      .header-left {
        display: flex;
        align-items: center;
        gap: $spacing-base;

        h2 {
          margin: 0;
          font-size: 20px;
          font-weight: 600;
        }

        .subtitle {
          font-weight: normal;
        }
      }
    }
  }

  .report-filter {
    margin-bottom: $spacing-base;

    .filter-actions {
      margin-left: auto;
      margin-right: 0;

      .export-dropdown {
        margin-left: $spacing-base;
      }
    }
  }

  .report-statistics {
    margin-bottom: $spacing-base;
  }

  .report-charts {
    margin-bottom: $spacing-base;
  }

  .report-table {
    margin-bottom: $spacing-base;
  }

  .report-pagination {
    display: flex;
    justify-content: flex-end;
    padding: $spacing-base 0;
  }
}
</style>