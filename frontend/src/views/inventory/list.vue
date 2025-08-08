<template>
  <div class="inventory-list">
    <!-- 库存概览卡片 -->
    <el-row :gutter="20" class="overview-cards">
      <el-col :span="6">
        <div class="overview-card warning">
          <div class="card-content">
            <div class="card-value">{{ statistics.lowStock }}</div>
            <div class="card-label">库存不足</div>
          </div>
          <div class="card-icon">
            <el-icon><WarningFilled /></el-icon>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="overview-card danger">
          <div class="card-content">
            <div class="card-value">{{ statistics.expired }}</div>
            <div class="card-label">即将过期</div>
          </div>
          <div class="card-icon">
            <el-icon><CircleCloseFilled /></el-icon>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="overview-card success">
          <div class="card-content">
            <div class="card-value">{{ statistics.normal }}</div>
            <div class="card-label">正常库存</div>
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
            <div class="card-label">商品种类</div>
          </div>
          <div class="card-icon">
            <el-icon><Goods /></el-icon>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 搜索和操作栏 -->
    <div class="action-bar card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="商品信息">
          <el-input
            v-model="searchForm.keyword"
            placeholder="商品名称/编码"
            clearable
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item label="商品类别">
          <el-cascader
            v-model="searchForm.category"
            :options="categoryOptions"
            :props="{ checkStrictly: true }"
            clearable
            placeholder="请选择商品类别"
          />
        </el-form-item>
        <el-form-item label="库存状态">
          <el-select v-model="searchForm.status" placeholder="请选择库存状态" clearable>
            <el-option label="库存不足" value="low" />
            <el-option label="库存充足" value="normal" />
            <el-option label="库存过高" value="high" />
          </el-select>
        </el-form-item>
        <el-form-item label="库存位置">
          <el-select v-model="searchForm.location" placeholder="请选择库存位置" clearable>
            <el-option
              v-for="item in locationOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
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
        <el-button type="primary" @click="handleStockIn">
          <el-icon><TopRight /></el-icon>
          入库
        </el-button>
        <el-button type="warning" @click="handleStockOut">
          <el-icon><BottomLeft /></el-icon>
          出库
        </el-button>
        <el-button type="info" @click="handleStockCheck">
          <el-icon><DocumentChecked /></el-icon>
          盘点
        </el-button>
        <el-button @click="handleExport">
          <el-icon><Download /></el-icon>
          导出
        </el-button>
      </div>
    </div>

    <!-- 库存列表 -->
    <div class="card">
      <el-table
        v-loading="loading"
        :data="inventoryList"
        border
        stripe
        style="width: 100%"
      >
        <el-table-column type="selection" width="55" align="center" />
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
        <el-table-column prop="product.category" label="类别" width="120" />
        <el-table-column label="库存信息" width="200">
          <template #default="{ row }">
            <div class="stock-info">
              <el-tag
                :type="getStockTagType(row.quantity, row.min_quantity, row.max_quantity)"
                effect="light"
              >
                {{ row.quantity }} {{ row.product.unit }}
              </el-tag>
              <div class="stock-limits">
                <span class="limit-item">
                  最小: {{ row.min_quantity }} {{ row.product.unit }}
                </span>
                <span class="limit-item">
                  最大: {{ row.max_quantity }} {{ row.product.unit }}
                </span>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="location" label="库存位置" width="120" />
        <el-table-column prop="batch_number" label="批次号" width="120" />
        <el-table-column label="最后操作" width="200">
          <template #default="{ row }">
            <div class="last-operation">
              <div>{{ row.last_operation }}</div>
              <div class="operation-time">{{ row.last_operation_time }}</div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button
              type="primary"
              link
              @click="handleStockInOut(row, 'in')"
            >
              入库
            </el-button>
            <el-button
              type="warning"
              link
              @click="handleStockInOut(row, 'out')"
            >
              出库
            </el-button>
            <el-button
              type="primary"
              link
              @click="handleViewHistory(row)"
            >
              记录
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

    <!-- 入库/出库对话框 -->
    <el-dialog
      v-model="stockDialog.visible"
      :title="stockDialog.type === 'in' ? '入库操作' : '出库操作'"
      width="500px"
      destroy-on-close
    >
      <el-form
        ref="stockFormRef"
        :model="stockForm"
        :rules="stockRules"
        label-width="100px"
      >
        <el-form-item label="商品名称">
          <div>{{ stockDialog.product?.name }}</div>
        </el-form-item>
        <el-form-item label="当前库存">
          <div>{{ stockDialog.currentStock }} {{ stockDialog.product?.unit }}</div>
        </el-form-item>
        <el-form-item 
          :label="stockDialog.type === 'in' ? '入库数量' : '出库数量'"
          prop="quantity"
        >
          <el-input-number
            v-model="stockForm.quantity"
            :min="1"
            :precision="2"
            :step="1"
            class="full-width"
          />
        </el-form-item>
        <el-form-item label="批次号" prop="batchNumber">
          <el-input
            v-model="stockForm.batchNumber"
            placeholder="请输入批次号"
          />
        </el-form-item>
        <el-form-item label="操作原因" prop="reason">
          <el-select
            v-model="stockForm.reason"
            placeholder="请选择操作原因"
            class="full-width"
          >
            <el-option
              v-for="item in reasonOptions[stockDialog.type]"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="备注" prop="notes">
          <el-input
            v-model="stockForm.notes"
            type="textarea"
            :rows="3"
            placeholder="请输入备注信息"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="stockDialog.visible = false">取消</el-button>
          <el-button type="primary" @click="handleStockSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 库存记录抽屉 -->
    <el-drawer
      v-model="historyDrawer.visible"
      title="库存操作记录"
      size="800px"
      destroy-on-close
    >
      <div v-loading="historyDrawer.loading">
        <div class="history-header">
          <div class="product-info">
            <div class="product-name">{{ historyDrawer.product?.name }}</div>
            <div class="product-code">{{ historyDrawer.product?.code }}</div>
          </div>
        </div>
        <el-timeline>
          <el-timeline-item
            v-for="(item, index) in historyDrawer.records"
            :key="index"
            :type="getTimelineItemType(item.type)"
            :timestamp="item.time"
            placement="top"
          >
            <div class="history-item">
              <div class="operation-type">
                {{ item.type === 'in' ? '入库' : '出库' }}
                <span class="quantity">
                  {{ item.type === 'in' ? '+' : '-' }}{{ item.quantity }}
                  {{ historyDrawer.product?.unit }}
                </span>
              </div>
              <div class="operation-info">
                <span>批次号：{{ item.batchNumber }}</span>
                <span>操作人：{{ item.operator }}</span>
              </div>
              <div class="operation-reason">
                原因：{{ item.reason }}
              </div>
              <div class="operation-notes" v-if="item.notes">
                备注：{{ item.notes }}
              </div>
            </div>
          </el-timeline-item>
        </el-timeline>
      </div>
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
import {
  Search, Refresh, TopRight, BottomLeft, DocumentChecked,
  Download, Picture, WarningFilled, CircleCloseFilled,
  CircleCheckFilled, Goods
} from '@element-plus/icons-vue'

// 统计数据
const statistics = reactive({
  lowStock: 5,
  expired: 2,
  normal: 158,
  total: 165
})

// 搜索表单
const searchForm = reactive({
  keyword: '',
  category: null,
  status: '',
  location: ''
})

// 分页参数
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 加载状态
const loading = ref(false)

// 库存列表数据
const inventoryList = ref([
  {
    id: 1,
    product: {
      name: '新鲜生菜',
      code: 'VEG001',
      category: '蔬菜',
      unit: 'kg',
      image: ''
    },
    quantity: 100,
    min_quantity: 50,
    max_quantity: 200,
    location: 'A-01-01',
    batch_number: 'B20240101001',
    last_operation: '入库',
    last_operation_time: '2024-01-01 12:00:00'
  }
])

// 选项数据
const categoryOptions = [
  {
    value: 'VEG',
    label: '蔬菜',
    children: [
      { value: 'VEG-LEAF', label: '叶菜类' },
      { value: 'VEG-ROOT', label: '根茎类' }
    ]
  }
]

const locationOptions = [
  { value: 'A-01-01', label: 'A区01货架01层' },
  { value: 'A-01-02', label: 'A区01货架02层' }
]

const reasonOptions = {
  in: [
    { value: 'purchase', label: '采购入库' },
    { value: 'return', label: '退货入库' },
    { value: 'adjustment', label: '库存调整' }
  ],
  out: [
    { value: 'sale', label: '销售出库' },
    { value: 'damage', label: '损耗出库' },
    { value: 'adjustment', label: '库存调整' }
  ]
}

// 入库/出库对话框
const stockDialog = reactive({
  visible: false,
  type: 'in',
  product: null,
  currentStock: 0
})

const stockFormRef = ref<FormInstance>()
const stockForm = reactive({
  quantity: 1,
  batchNumber: '',
  reason: '',
  notes: ''
})

const stockRules: FormRules = {
  quantity: [
    { required: true, message: '请输入数量', trigger: 'blur' }
  ],
  batchNumber: [
    { required: true, message: '请输入批次号', trigger: 'blur' }
  ],
  reason: [
    { required: true, message: '请选择操作原因', trigger: 'change' }
  ]
}

// 历史记录抽屉
const historyDrawer = reactive({
  visible: false,
  loading: false,
  product: null,
  records: [
    {
      type: 'in',
      quantity: 100,
      batchNumber: 'B20240101001',
      operator: '张三',
      reason: '采购入库',
      notes: '正常采购入库',
      time: '2024-01-01 12:00:00'
    }
  ]
})

// 获取库存列表
const getInventoryList = async () => {
  loading.value = true
  try {
    // TODO: 调用API获取库存列表
    // const res = await getInventory({ ...searchForm, page: page.value, pageSize: pageSize.value })
    // inventoryList.value = res.data.items
    // total.value = res.data.total
  } catch (error) {
    console.error('获取库存列表失败:', error)
    ElMessage.error('获取库存列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  page.value = 1
  getInventoryList()
}

// 重置搜索
const resetSearch = () => {
  Object.keys(searchForm).forEach(key => {
    searchForm[key] = ''
  })
  handleSearch()
}

// 分页处理
const handleSizeChange = (val: number) => {
  pageSize.value = val
  getInventoryList()
}

const handleCurrentChange = (val: number) => {
  page.value = val
  getInventoryList()
}

// 入库操作
const handleStockIn = () => {
  ElMessage.warning('请在具体商品上进行入库操作')
}

// 出库操作
const handleStockOut = () => {
  ElMessage.warning('请在具体商品上进行出库操作')
}

// 盘点操作
const handleStockCheck = () => {
  // TODO: 实现盘点功能
  ElMessage.info('盘点功能开发中')
}

// 导出数据
const handleExport = () => {
  // TODO: 实现导出功能
  ElMessage.info('导出功能开发中')
}

// 单个商品入库/出库
const handleStockInOut = (row: any, type: 'in' | 'out') => {
  stockDialog.type = type
  stockDialog.product = row.product
  stockDialog.currentStock = row.quantity
  stockDialog.visible = true
  
  // 重置表单
  stockForm.quantity = 1
  stockForm.batchNumber = ''
  stockForm.reason = ''
  stockForm.notes = ''
}

// 提交入库/出库
const handleStockSubmit = async () => {
  if (!stockFormRef.value) return
  
  try {
    await stockFormRef.value.validate()
    // TODO: 调用API提交入库/出库
    ElMessage.success(stockDialog.type === 'in' ? '入库成功' : '出库成功')
    stockDialog.visible = false
    getInventoryList()
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败，请检查表单')
  }
}

// 查看历史记录
const handleViewHistory = (row: any) => {
  historyDrawer.product = row.product
  historyDrawer.visible = true
  historyDrawer.loading = true
  
  // TODO: 调用API获取历史记录
  setTimeout(() => {
    historyDrawer.loading = false
  }, 1000)
}

// 获取库存标签类型
const getStockTagType = (quantity: number, min: number, max: number) => {
  if (quantity <= min) return 'danger'
  if (quantity >= max) return 'warning'
  return 'success'
}

// 获取时间线项目类型
const getTimelineItemType = (type: string) => {
  return type === 'in' ? 'success' : 'warning'
}

onMounted(() => {
  getInventoryList()
})
</script>

<style lang="scss" scoped>
.inventory-list {
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

      &.danger {
        background: linear-gradient(135deg, #ef5350 0%, #e53935 100%);
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

  .stock-info {
    .el-tag {
      margin-bottom: 8px;
    }

    .stock-limits {
      font-size: 12px;
      color: $text-secondary;

      .limit-item {
        display: block;
      }
    }
  }

  .last-operation {
    .operation-time {
      font-size: 12px;
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

.history-header {
  padding: 0 $spacing-base $spacing-base;
  border-bottom: 1px solid $border-color-light;
  margin-bottom: $spacing-base;

  .product-info {
    .product-name {
      font-size: 16px;
      font-weight: 500;
      margin-bottom: 4px;
    }

    .product-code {
      font-size: 12px;
      color: $text-secondary;
    }
  }
}

.history-item {
  .operation-type {
    font-weight: 500;
    margin-bottom: 8px;

    .quantity {
      margin-left: 8px;
      color: $text-regular;
    }
  }

  .operation-info {
    font-size: 13px;
    color: $text-regular;
    margin-bottom: 4px;

    span {
      margin-right: 16px;
    }
  }

  .operation-reason {
    font-size: 13px;
    color: $text-regular;
    margin-bottom: 4px;
  }

  .operation-notes {
    font-size: 13px;
    color: $text-secondary;
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