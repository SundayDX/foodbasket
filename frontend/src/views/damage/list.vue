<template>
  <div class="damage-list">
    <!-- 报损统计卡片 -->
    <el-row :gutter="20" class="overview-cards">
      <el-col :span="6">
        <div class="overview-card warning">
          <div class="card-content">
            <div class="card-value">{{ statistics.pending }}</div>
            <div class="card-label">待审核</div>
          </div>
          <div class="card-icon">
            <el-icon><Timer /></el-icon>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="overview-card success">
          <div class="card-content">
            <div class="card-value">{{ statistics.approved }}</div>
            <div class="card-label">已审核</div>
          </div>
          <div class="card-icon">
            <el-icon><CircleCheckFilled /></el-icon>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="overview-card danger">
          <div class="card-content">
            <div class="card-value">{{ statistics.rejected }}</div>
            <div class="card-label">已拒绝</div>
          </div>
          <div class="card-icon">
            <el-icon><CircleCloseFilled /></el-icon>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="overview-card primary">
          <div class="card-content">
            <div class="card-value">￥{{ statistics.totalAmount }}</div>
            <div class="card-label">报损总额</div>
          </div>
          <div class="card-icon">
            <el-icon><Money /></el-icon>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 搜索和操作栏 -->
    <div class="action-bar card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="报损单号">
          <el-input
            v-model="searchForm.damageNumber"
            placeholder="请输入报损单号"
            clearable
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item label="商品信息">
          <el-input
            v-model="searchForm.keyword"
            placeholder="商品名称/编码"
            clearable
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item label="报损类型">
          <el-select v-model="searchForm.type" placeholder="请选择报损类型" clearable>
            <el-option label="自然损耗" value="natural" />
            <el-option label="运输损坏" value="transport" />
            <el-option label="质量问题" value="quality" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="审核状态">
          <el-select v-model="searchForm.status" placeholder="请选择审核状态" clearable>
            <el-option label="待审核" value="pending" />
            <el-option label="已审核" value="approved" />
            <el-option label="已拒绝" value="rejected" />
          </el-select>
        </el-form-item>
        <el-form-item label="报损时间">
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
          新建报损
        </el-button>
        <el-button type="success" @click="handleBatchApprove">
          <el-icon><CircleCheck /></el-icon>
          批量审核
        </el-button>
        <el-button @click="handleExport">
          <el-icon><Download /></el-icon>
          导出数据
        </el-button>
      </div>
    </div>

    <!-- 报损单列表 -->
    <div class="card">
      <el-table
        v-loading="loading"
        :data="damageList"
        border
        stripe
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column prop="damageNumber" label="报损单号" width="180" />
        <el-table-column label="商品信息" min-width="300">
          <template #default="{ row }">
            <div class="product-info">
              <el-image
                :src="row.product.image"
                :preview-src-list="[row.product.image]"
                fit="cover"
                class="product-image"
              >
                <template #error>
                  <div class="image-placeholder">
                    <el-icon><Picture /></el-icon>
                  </div>
                </template>
              </el-image>
              <div class="product-detail">
                <div class="product-name">{{ row.product.name }}</div>
                <div class="product-code">{{ row.product.code }}</div>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="报损信息" width="200">
          <template #default="{ row }">
            <div class="damage-info">
              <div class="info-item">
                <span class="label">数量：</span>
                <span class="value">{{ row.quantity }} {{ row.product.unit }}</span>
              </div>
              <div class="info-item">
                <span class="label">金额：</span>
                <span class="value amount">￥{{ row.amount }}</span>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="type" label="报损类型" width="120">
          <template #default="{ row }">
            <el-tag :type="getDamageTypeTag(row.type)">
              {{ getDamageTypeText(row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="batchNumber" label="批次号" width="120" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTagType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="申请信息" width="180">
          <template #default="{ row }">
            <div class="apply-info">
              <div>{{ row.reporter }}</div>
              <div class="apply-time">{{ row.reportTime }}</div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="审核信息" width="180">
          <template #default="{ row }">
            <div class="approve-info" v-if="row.status !== 'pending'">
              <div>{{ row.approver }}</div>
              <div class="approve-time">{{ row.approveTime }}</div>
            </div>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button
              v-if="row.status === 'pending'"
              type="success"
              link
              @click="handleApprove(row)"
            >
              审核
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
              type="danger"
              link
              @click="handleDelete(row)"
            >
              删除
            </el-button>
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

    <!-- 审核对话框 -->
    <el-dialog
      v-model="approveDialog.visible"
      title="报损审核"
      width="500px"
      destroy-on-close
    >
      <el-form
        ref="approveFormRef"
        :model="approveForm"
        :rules="approveRules"
        label-width="100px"
      >
        <el-form-item label="审核结果" prop="result">
          <el-radio-group v-model="approveForm.result">
            <el-radio label="approved">通过</el-radio>
            <el-radio label="rejected">拒绝</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="处理方式" prop="handlingMethod" v-if="approveForm.result === 'approved'">
          <el-select
            v-model="approveForm.handlingMethod"
            placeholder="请选择处理方式"
            class="full-width"
          >
            <el-option label="销毁" value="destroy" />
            <el-option label="降价销售" value="discount" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="审核意见" prop="comment">
          <el-input
            v-model="approveForm.comment"
            type="textarea"
            :rows="3"
            placeholder="请输入审核意见"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="approveDialog.visible = false">取消</el-button>
          <el-button type="primary" @click="handleApproveSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Search, Refresh, Plus, Download, Picture, Timer,
  CircleCheckFilled, CircleCloseFilled, Money, CircleCheck
} from '@element-plus/icons-vue'

const router = useRouter()

// 统计数据
const statistics = reactive({
  pending: 10,
  approved: 85,
  rejected: 5,
  totalAmount: '12,345.67'
})

// 搜索表单
const searchForm = reactive({
  damageNumber: '',
  keyword: '',
  type: '',
  status: '',
  timeRange: []
})

// 分页参数
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 加载状态
const loading = ref(false)

// 选中的报损单
const selectedDamages = ref([])

// 报损单列表数据
const damageList = ref([
  {
    id: 1,
    damageNumber: 'D20240101001',
    product: {
      name: '新鲜生菜',
      code: 'VEG001',
      unit: 'kg',
      image: ''
    },
    quantity: 10,
    amount: 50.00,
    type: 'natural',
    batchNumber: 'B20240101001',
    status: 'pending',
    reporter: '张三',
    reportTime: '2024-01-01 09:00:00',
    approver: '',
    approveTime: ''
  }
])

// 审核对话框
const approveDialog = reactive({
  visible: false,
  currentDamage: null
})

const approveFormRef = ref<FormInstance>()
const approveForm = reactive({
  result: 'approved',
  handlingMethod: '',
  comment: ''
})

const approveRules: FormRules = {
  result: [
    { required: true, message: '请选择审核结果', trigger: 'change' }
  ],
  handlingMethod: [
    { required: true, message: '请选择处理方式', trigger: 'change' }
  ],
  comment: [
    { required: true, message: '请输入审核意见', trigger: 'blur' }
  ]
}

// 获取报损单列表
const getDamageList = async () => {
  loading.value = true
  try {
    // TODO: 调用API获取报损单列表
    // const res = await getDamages({ ...searchForm, page: page.value, pageSize: pageSize.value })
    // damageList.value = res.data.items
    // total.value = res.data.total
  } catch (error) {
    console.error('获取报损单列表失败:', error)
    ElMessage.error('获取报损单列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  page.value = 1
  getDamageList()
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
  getDamageList()
}

const handleCurrentChange = (val: number) => {
  page.value = val
  getDamageList()
}

// 新建报损
const handleCreate = () => {
  router.push('/damage/create')
}

// 批量审核
const handleBatchApprove = () => {
  if (selectedDamages.value.length === 0) {
    ElMessage.warning('请选择需要审核的报损单')
    return
  }
  // TODO: 实现批量审核
  ElMessage.info('批量审核功能开发中')
}

// 导出数据
const handleExport = () => {
  // TODO: 实现导出功能
  ElMessage.info('导出功能开发中')
}

// 表格选择
const handleSelectionChange = (val: any[]) => {
  selectedDamages.value = val
}

// 审核
const handleApprove = (row: any) => {
  approveDialog.currentDamage = row
  approveDialog.visible = true
}

// 提交审核
const handleApproveSubmit = async () => {
  if (!approveFormRef.value) return
  
  try {
    await approveFormRef.value.validate()
    // TODO: 调用API提交审核
    ElMessage.success('审核成功')
    approveDialog.visible = false
    getDamageList()
  } catch (error) {
    console.error('审核失败:', error)
    ElMessage.error('审核失败')
  }
}

// 查看详情
const handleView = (row: any) => {
  router.push(`/damage/detail/${row.id}`)
}

// 删除报损单
const handleDelete = (row: any) => {
  ElMessageBox.confirm(
    '确定要删除该报损单吗？',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      // TODO: 调用API删除报损单
      ElMessage.success('删除成功')
      getDamageList()
    } catch (error) {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

// 获取报损类型标签
const getDamageTypeTag = (type: string) => {
  switch (type) {
    case 'natural':
      return 'info'
    case 'transport':
      return 'warning'
    case 'quality':
      return 'danger'
    default:
      return 'info'
  }
}

// 获取报损类型文本
const getDamageTypeText = (type: string) => {
  switch (type) {
    case 'natural':
      return '自然损耗'
    case 'transport':
      return '运输损坏'
    case 'quality':
      return '质量问题'
    case 'other':
      return '其他'
    default:
      return '未知'
  }
}

// 获取状态标签类型
const getStatusTagType = (status: string) => {
  switch (status) {
    case 'pending':
      return 'info'
    case 'approved':
      return 'success'
    case 'rejected':
      return 'danger'
    default:
      return 'info'
  }
}

// 获取状态文本
const getStatusText = (status: string) => {
  switch (status) {
    case 'pending':
      return '待审核'
    case 'approved':
      return '已审核'
    case 'rejected':
      return '已拒绝'
    default:
      return '未知'
  }
}

onMounted(() => {
  getDamageList()
})
</script>

<style lang="scss" scoped>
.damage-list {
  .overview-cards {
    margin-bottom: $spacing-base;

    .overview-card {
      padding: $spacing-base;
      border-radius: $border-radius-base;
      display: flex;
      align-items: center;
      justify-content: space-between;
      color: #fff;

      &.warning {
        background: linear-gradient(135deg, #ffa726 0%, #fb8c00 100%);
      }

      &.success {
        background: linear-gradient(135deg, #66bb6a 0%, #43a047 100%);
      }

      &.danger {
        background: linear-gradient(135deg, #ef5350 0%, #e53935 100%);
      }

      &.primary {
        background: linear-gradient(135deg, #1890ff 0%, #096dd9 100%);
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

  .product-info {
    display: flex;
    align-items: center;
    gap: $spacing-base;

    .product-image {
      width: 50px;
      height: 50px;
      border-radius: $border-radius-small;
    }

    .product-detail {
      .product-name {
        font-weight: 500;
        margin-bottom: 4px;
      }

      .product-code {
        font-size: 12px;
        color: $text-secondary;
      }
    }
  }

  .damage-info {
    .info-item {
      margin-bottom: 4px;

      &:last-child {
        margin-bottom: 0;
      }

      .label {
        color: $text-secondary;
      }

      .value {
        &.amount {
          color: $danger-color;
          font-weight: 500;
        }
      }
    }
  }

  .apply-info,
  .approve-info {
    font-size: 13px;

    .apply-time,
    .approve-time {
      color: $text-secondary;
      margin-top: 4px;
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

.image-placeholder {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: $background-color-light;
  border: 1px dashed $border-color-base;
  border-radius: $border-radius-small;
  
  .el-icon {
    font-size: 20px;
    color: $text-secondary;
  }
}
</style>