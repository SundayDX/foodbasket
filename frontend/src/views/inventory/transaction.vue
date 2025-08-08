<template>
  <div class="transaction-page">
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
        <el-form-item label="交易类型">
          <el-select v-model="searchForm.type" placeholder="请选择交易类型" clearable>
            <el-option label="入库" value="in" />
            <el-option label="出库" value="out" />
            <el-option label="调整" value="adjustment" />
          </el-select>
        </el-form-item>
        <el-form-item label="批次号">
          <el-input
            v-model="searchForm.batchNumber"
            placeholder="请输入批次号"
            clearable
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item label="操作时间">
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
        <el-button type="primary" @click="handleExport">
          <el-icon><Download /></el-icon>
          导出记录
        </el-button>
      </div>
    </div>

    <!-- 交易记录表格 -->
    <div class="card">
      <el-table
        v-loading="loading"
        :data="transactionList"
        border
        stripe
        style="width: 100%"
      >
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
        <el-table-column label="交易信息" width="200">
          <template #default="{ row }">
            <div class="transaction-info">
              <el-tag
                :type="getTransactionTagType(row.type)"
                effect="light"
              >
                {{ row.type === 'in' ? '入库' : row.type === 'out' ? '出库' : '调整' }}
              </el-tag>
              <div class="quantity" :class="row.type">
                {{ row.type === 'in' ? '+' : '-' }}{{ row.quantity }}
                {{ row.product.unit }}
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="batchNumber" label="批次号" width="120" />
        <el-table-column label="库存变化" width="200">
          <template #default="{ row }">
            <div class="stock-change">
              <div class="before">
                变更前：{{ row.beforeStock }} {{ row.product.unit }}
              </div>
              <div class="after">
                变更后：{{ row.afterStock }} {{ row.product.unit }}
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="reason" label="操作原因" width="120" />
        <el-table-column label="操作信息" width="200">
          <template #default="{ row }">
            <div class="operation-info">
              <div>操作人：{{ row.operator }}</div>
              <div class="operation-time">{{ row.operationTime }}</div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="notes" label="备注" min-width="150" show-overflow-tooltip />
        <el-table-column label="操作" width="100" fixed="right">
          <template #default="{ row }">
            <el-button
              type="primary"
              link
              @click="handleViewDetail(row)"
            >
              详情
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

    <!-- 详情抽屉 -->
    <el-drawer
      v-model="detailDrawer.visible"
      title="交易详情"
      size="600px"
      destroy-on-close
    >
      <div class="transaction-detail">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="商品名称">
            {{ detailDrawer.data?.product?.name }}
          </el-descriptions-item>
          <el-descriptions-item label="商品编码">
            {{ detailDrawer.data?.product?.code }}
          </el-descriptions-item>
          <el-descriptions-item label="交易类型">
            <el-tag :type="getTransactionTagType(detailDrawer.data?.type)">
              {{ detailDrawer.data?.type === 'in' ? '入库' : detailDrawer.data?.type === 'out' ? '出库' : '调整' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="交易数量">
            <span :class="['quantity', detailDrawer.data?.type]">
              {{ detailDrawer.data?.type === 'in' ? '+' : '-' }}{{ detailDrawer.data?.quantity }}
              {{ detailDrawer.data?.product?.unit }}
            </span>
          </el-descriptions-item>
          <el-descriptions-item label="批次号">
            {{ detailDrawer.data?.batchNumber }}
          </el-descriptions-item>
          <el-descriptions-item label="变更前库存">
            {{ detailDrawer.data?.beforeStock }} {{ detailDrawer.data?.product?.unit }}
          </el-descriptions-item>
          <el-descriptions-item label="变更后库存">
            {{ detailDrawer.data?.afterStock }} {{ detailDrawer.data?.product?.unit }}
          </el-descriptions-item>
          <el-descriptions-item label="操作原因">
            {{ detailDrawer.data?.reason }}
          </el-descriptions-item>
          <el-descriptions-item label="操作人">
            {{ detailDrawer.data?.operator }}
          </el-descriptions-item>
          <el-descriptions-item label="操作时间">
            {{ detailDrawer.data?.operationTime }}
          </el-descriptions-item>
          <el-descriptions-item label="备注">
            {{ detailDrawer.data?.notes || '无' }}
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Search, Refresh, Download, Picture } from '@element-plus/icons-vue'

// 搜索表单
const searchForm = reactive({
  keyword: '',
  type: '',
  batchNumber: '',
  timeRange: []
})

// 分页参数
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 加载状态
const loading = ref(false)

// 交易记录列表
const transactionList = ref([
  {
    id: 1,
    product: {
      name: '新鲜生菜',
      code: 'VEG001',
      unit: 'kg',
      image: ''
    },
    type: 'in',
    quantity: 100,
    batchNumber: 'B20240101001',
    beforeStock: 50,
    afterStock: 150,
    reason: '采购入库',
    operator: '张三',
    operationTime: '2024-01-01 12:00:00',
    notes: '正常采购入库'
  }
])

// 详情抽屉
const detailDrawer = reactive({
  visible: false,
  data: null
})

// 获取交易记录列表
const getTransactionList = async () => {
  loading.value = true
  try {
    // TODO: 调用API获取交易记录列表
    // const res = await getTransactions({ ...searchForm, page: page.value, pageSize: pageSize.value })
    // transactionList.value = res.data.items
    // total.value = res.data.total
  } catch (error) {
    console.error('获取交易记录列表失败:', error)
    ElMessage.error('获取交易记录列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  page.value = 1
  getTransactionList()
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
  getTransactionList()
}

const handleCurrentChange = (val: number) => {
  page.value = val
  getTransactionList()
}

// 导出记录
const handleExport = () => {
  // TODO: 实现导出功能
  ElMessage.info('导出功能开发中')
}

// 查看详情
const handleViewDetail = (row: any) => {
  detailDrawer.data = row
  detailDrawer.visible = true
}

// 获取交易标签类型
const getTransactionTagType = (type: string) => {
  switch (type) {
    case 'in':
      return 'success'
    case 'out':
      return 'warning'
    default:
      return 'info'
  }
}

onMounted(() => {
  getTransactionList()
})
</script>

<style lang="scss" scoped>
.transaction-page {
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

  .transaction-info {
    .quantity {
      margin-top: 8px;
      font-weight: 500;

      &.in {
        color: $success-color;
      }

      &.out {
        color: $warning-color;
      }

      &.adjustment {
        color: $info-color;
      }
    }
  }

  .stock-change {
    font-size: 13px;

    .before {
      color: $text-secondary;
      margin-bottom: 4px;
    }

    .after {
      color: $text-primary;
      font-weight: 500;
    }
  }

  .operation-info {
    font-size: 13px;

    .operation-time {
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

.transaction-detail {
  :deep(.el-descriptions__label) {
    width: 120px;
  }

  .quantity {
    font-weight: 500;

    &.in {
      color: $success-color;
    }

    &.out {
      color: $warning-color;
    }

    &.adjustment {
      color: $info-color;
    }
  }
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