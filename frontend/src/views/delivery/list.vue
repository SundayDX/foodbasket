<template>
  <div class="delivery-list">
    <!-- 配送概览卡片 -->
    <el-row :gutter="20" class="overview-cards">
      <el-col :span="6">
        <div class="overview-card primary">
          <div class="card-content">
            <div class="card-value">{{ statistics.pending }}</div>
            <div class="card-label">待发货</div>
          </div>
          <div class="card-icon">
            <el-icon><Box /></el-icon>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="overview-card warning">
          <div class="card-content">
            <div class="card-value">{{ statistics.delivering }}</div>
            <div class="card-label">配送中</div>
          </div>
          <div class="card-icon">
            <el-icon><Van /></el-icon>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="overview-card success">
          <div class="card-content">
            <div class="card-value">{{ statistics.completed }}</div>
            <div class="card-label">已完成</div>
          </div>
          <div class="card-icon">
            <el-icon><CircleCheckFilled /></el-icon>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="overview-card info">
          <div class="card-content">
            <div class="card-value">{{ statistics.total }}</div>
            <div class="card-label">总配送单</div>
          </div>
          <div class="card-icon">
            <el-icon><Document /></el-icon>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 搜索和操作栏 -->
    <div class="action-bar card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="配送单号">
          <el-input
            v-model="searchForm.deliveryNumber"
            placeholder="请输入配送单号"
            clearable
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item label="配送状态">
          <el-select v-model="searchForm.status" placeholder="请选择配送状态" clearable>
            <el-option label="待发货" value="pending" />
            <el-option label="配送中" value="delivering" />
            <el-option label="已完成" value="completed" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
        </el-form-item>
        <el-form-item label="司机">
          <el-select
            v-model="searchForm.driverId"
            placeholder="请选择司机"
            clearable
            filterable
          >
            <el-option
              v-for="item in driverOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="配送时间">
          <el-date-picker
            v-model="searchForm.timeRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="resetSearch">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </el-form-item>
      </el-form>

      <div class="button-group">
        <el-button type="primary" @click="handleCreate">
          <el-icon><Plus /></el-icon>
          新建配送单
        </el-button>
        <el-button type="success" @click="handleBatchDispatch">
          <el-icon><Van /></el-icon>
          批量发货
        </el-button>
        <el-button @click="handleExport">
          <el-icon><Download /></el-icon>
          导出数据
        </el-button>
      </div>
    </div>

    <!-- 配送单列表 -->
    <div class="card">
      <el-table
        v-loading="loading"
        :data="deliveryList"
        border
        stripe
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column prop="deliveryNumber" label="配送单号" width="180" />
        <el-table-column label="配送状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusTagType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="配送信息" min-width="300">
          <template #default="{ row }">
            <div class="delivery-info">
              <div class="info-item">
                <span class="label">司机：</span>
                <span class="value">{{ row.driver.name }}</span>
                <span class="phone">{{ row.driver.phone }}</span>
              </div>
              <div class="info-item">
                <span class="label">车牌：</span>
                <span class="value">{{ row.vehicleNumber }}</span>
              </div>
              <div class="info-item">
                <span class="label">配送点：</span>
                <span class="value">{{ row.deliveryPoints.length }} 个</span>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="配送进度" width="200">
          <template #default="{ row }">
            <div class="delivery-progress">
              <el-progress
                :percentage="getDeliveryProgress(row)"
                :status="getProgressStatus(row.status)"
              />
              <div class="progress-text">
                已完成 {{ row.completedPoints }} / {{ row.deliveryPoints.length }} 个配送点
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="时间信息" width="180">
          <template #default="{ row }">
            <div class="time-info">
              <div class="time-item">
                <el-icon><Timer /></el-icon>
                <span>{{ row.startTime || '未开始' }}</span>
              </div>
              <div class="time-item" v-if="row.endTime">
                <el-icon><CircleCheckFilled /></el-icon>
                <span>{{ row.endTime }}</span>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="配送统计" width="180">
          <template #default="{ row }">
            <div class="delivery-stats">
              <div class="stats-item">
                <span class="label">总里程：</span>
                <span class="value">{{ row.totalDistance || 0 }} km</span>
              </div>
              <div class="stats-item">
                <span class="label">油耗：</span>
                <span class="value">{{ row.fuelConsumption || 0 }} L</span>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button
              v-if="row.status === 'pending'"
              type="success"
              link
              @click="handleDispatch(row)"
            >
              发货
            </el-button>
            <el-button
              type="primary"
              link
              @click="handleView(row)"
            >
              查看
            </el-button>
            <el-button
              v-if="row.status === 'pending'"
              type="primary"
              link
              @click="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-popconfirm
              v-if="row.status === 'pending'"
              title="确定要取消该配送单吗？"
              @confirm="handleCancel(row)"
            >
              <template #reference>
                <el-button
                  type="danger"
                  link
                >
                  取消
                </el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>

    <!-- 发货对话框 -->
    <el-dialog
      v-model="dispatchDialog.visible"
      title="发货确认"
      width="500px"
      destroy-on-close
    >
      <el-form
        ref="dispatchFormRef"
        :model="dispatchForm"
        :rules="dispatchRules"
        label-width="100px"
      >
        <el-form-item label="配送单号">
          <div>{{ dispatchDialog.deliveryNumber }}</div>
        </el-form-item>
        <el-form-item label="司机" prop="driverId">
          <el-select
            v-model="dispatchForm.driverId"
            placeholder="请选择司机"
            class="full-width"
          >
            <el-option
              v-for="item in driverOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="车牌号" prop="vehicleNumber">
          <el-input
            v-model="dispatchForm.vehicleNumber"
            placeholder="请输入车牌号"
          />
        </el-form-item>
        <el-form-item label="发货时间" prop="startTime">
          <el-date-picker
            v-model="dispatchForm.startTime"
            type="datetime"
            placeholder="请选择发货时间"
            class="full-width"
          />
        </el-form-item>
        <el-form-item label="备注" prop="notes">
          <el-input
            v-model="dispatchForm.notes"
            type="textarea"
            :rows="3"
            placeholder="请输入备注信息"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dispatchDialog.visible = false">取消</el-button>
          <el-button type="primary" @click="handleDispatchSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
import {
  Search, Refresh, Plus, Download, Box, Van,
  CircleCheckFilled, Document, Timer
} from '@element-plus/icons-vue'

const router = useRouter()

// 统计数据
const statistics = reactive({
  pending: 10,
  delivering: 5,
  completed: 85,
  total: 100
})

// 搜索表单
const searchForm = reactive({
  deliveryNumber: '',
  status: '',
  driverId: '',
  timeRange: []
})

// 分页参数
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 加载状态
const loading = ref(false)

// 选中的配送单
const selectedDeliveries = ref([])

// 配送单列表数据
const deliveryList = ref([
  {
    id: 1,
    deliveryNumber: 'D20240101001',
    status: 'delivering',
    driver: {
      name: '张三',
      phone: '13800138000'
    },
    vehicleNumber: '京A12345',
    deliveryPoints: [
      { id: 1, status: 'completed' },
      { id: 2, status: 'pending' }
    ],
    completedPoints: 1,
    startTime: '2024-01-01 09:00:00',
    endTime: null,
    totalDistance: 50,
    fuelConsumption: 5
  }
])

// 司机选项
const driverOptions = [
  { value: 1, label: '张三' },
  { value: 2, label: '李四' }
]

// 发货对话框
const dispatchDialog = reactive({
  visible: false,
  deliveryNumber: ''
})

const dispatchFormRef = ref<FormInstance>()
const dispatchForm = reactive({
  driverId: '',
  vehicleNumber: '',
  startTime: '',
  notes: ''
})

const dispatchRules: FormRules = {
  driverId: [
    { required: true, message: '请选择司机', trigger: 'change' }
  ],
  vehicleNumber: [
    { required: true, message: '请输入车牌号', trigger: 'blur' }
  ],
  startTime: [
    { required: true, message: '请选择发货时间', trigger: 'change' }
  ]
}

// 获取配送单列表
const getDeliveryList = async () => {
  loading.value = true
  try {
    // TODO: 调用API获取配送单列表
    // const res = await getDeliveries({ ...searchForm, page: page.value, pageSize: pageSize.value })
    // deliveryList.value = res.data.items
    // total.value = res.data.total
  } catch (error) {
    console.error('获取配送单列表失败:', error)
    ElMessage.error('获取配送单列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  page.value = 1
  getDeliveryList()
}

// 重置搜索
const resetSearch = () => {
  Object.keys(searchForm).forEach(key => {
    searchForm[key] = key === 'timeRange' ? [] : ''
  })
  handleSearch()
}

// 分页处理
const handleSizeChange = (val: number) => {
  pageSize.value = val
  getDeliveryList()
}

const handleCurrentChange = (val: number) => {
  page.value = val
  getDeliveryList()
}

// 新建配送单
const handleCreate = () => {
  router.push('/delivery/create')
}

// 批量发货
const handleBatchDispatch = () => {
  if (selectedDeliveries.value.length === 0) {
    ElMessage.warning('请选择需要发货的配送单')
    return
  }
  // TODO: 实现批量发货
  ElMessage.info('批量发货功能开发中')
}

// 导出数据
const handleExport = () => {
  // TODO: 实现导出功能
  ElMessage.info('导出功能开发中')
}

// 表格选择
const handleSelectionChange = (val: any[]) => {
  selectedDeliveries.value = val
}

// 发货
const handleDispatch = (row: any) => {
  dispatchDialog.deliveryNumber = row.deliveryNumber
  dispatchDialog.visible = true
}

// 提交发货
const handleDispatchSubmit = async () => {
  if (!dispatchFormRef.value) return
  
  try {
    await dispatchFormRef.value.validate()
    // TODO: 调用API提交发货
    ElMessage.success('发货成功')
    dispatchDialog.visible = false
    getDeliveryList()
  } catch (error) {
    console.error('发货失败:', error)
    ElMessage.error('发货失败，请检查表单')
  }
}

// 查看详情
const handleView = (row: any) => {
  router.push(`/delivery/detail/${row.id}`)
}

// 编辑配送单
const handleEdit = (row: any) => {
  router.push(`/delivery/create?id=${row.id}`)
}

// 取消配送单
const handleCancel = async (row: any) => {
  try {
    // TODO: 调用API取消配送单
    ElMessage.success('取消成功')
    getDeliveryList()
  } catch (error) {
    console.error('取消配送单失败:', error)
    ElMessage.error('取消失败')
  }
}

// 获取状态标签类型
const getStatusTagType = (status: string) => {
  switch (status) {
    case 'pending':
      return 'info'
    case 'delivering':
      return 'warning'
    case 'completed':
      return 'success'
    case 'cancelled':
      return 'danger'
    default:
      return 'info'
  }
}

// 获取状态文本
const getStatusText = (status: string) => {
  switch (status) {
    case 'pending':
      return '待发货'
    case 'delivering':
      return '配送中'
    case 'completed':
      return '已完成'
    case 'cancelled':
      return '已取消'
    default:
      return '未知'
  }
}

// 获取配送进度
const getDeliveryProgress = (row: any) => {
  if (!row.deliveryPoints?.length) return 0
  return Math.round((row.completedPoints / row.deliveryPoints.length) * 100)
}

// 获取进度状态
const getProgressStatus = (status: string) => {
  switch (status) {
    case 'completed':
      return 'success'
    case 'cancelled':
      return 'exception'
    default:
      return ''
  }
}

onMounted(() => {
  getDeliveryList()
})
</script>

<style lang="scss" scoped>
.delivery-list {
  .overview-cards {
    margin-bottom: $spacing-base;

    .overview-card {
      padding: $spacing-base;
      border-radius: $border-radius-base;
      display: flex;
      align-items: center;
      justify-content: space-between;
      color: #fff;

      &.primary {
        background: linear-gradient(135deg, #1890ff 0%, #096dd9 100%);
      }

      &.warning {
        background: linear-gradient(135deg, #ffa726 0%, #fb8c00 100%);
      }

      &.success {
        background: linear-gradient(135deg, #66bb6a 0%, #43a047 100%);
      }

      &.info {
        background: linear-gradient(135deg, #26c6da 0%, #00acc1 100%);
      }

      .card-content {
        .card-value {
          font-size: 24px;
          font-weight: 600;
          margin-bottom: 4px;
        }

        .card-label {
          font-size: 14px;
          opacity: 0.9;
        }
      }

      .card-icon {
        font-size: 36px;
        opacity: 0.8;
      }
    }
  }

  .action-bar {
    margin-bottom: $spacing-base;
    
    .search-form {
      margin-bottom: $spacing-base;
    }
    
    .button-group {
      display: flex;
      gap: $spacing-base;
    }
  }

  .delivery-info {
    .info-item {
      margin-bottom: 4px;

      &:last-child {
        margin-bottom: 0;
      }

      .label {
        color: $text-secondary;
      }

      .value {
        margin-right: $spacing-base;
      }

      .phone {
        color: $text-secondary;
      }
    }
  }

  .delivery-progress {
    .progress-text {
      font-size: 12px;
      color: $text-secondary;
      margin-top: 4px;
    }
  }

  .time-info {
    .time-item {
      display: flex;
      align-items: center;
      gap: $spacing-small;
      margin-bottom: 4px;

      &:last-child {
        margin-bottom: 0;
      }

      .el-icon {
        font-size: 16px;
        color: $text-secondary;
      }
    }
  }

  .delivery-stats {
    .stats-item {
      margin-bottom: 4px;

      &:last-child {
        margin-bottom: 0;
      }

      .label {
        color: $text-secondary;
      }

      .value {
        font-weight: 500;
      }
    }
  }

  .pagination-container {
    margin-top: $spacing-large;
    display: flex;
    justify-content: flex-end;
  }
}

.full-width {
  width: 100%;
}
</style>