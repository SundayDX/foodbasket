<template>
  <div class="quality-check">
    <!-- 质量检查概览 -->
    <el-row :gutter="20" class="overview-cards">
      <el-col :span="6">
        <div class="overview-card primary">
          <div class="card-content">
            <div class="card-value">{{ statistics.pending }}</div>
            <div class="card-label">待检查</div>
          </div>
          <div class="card-icon">
            <el-icon><Timer /></el-icon>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="overview-card success">
          <div class="card-content">
            <div class="card-value">{{ statistics.qualified }}</div>
            <div class="card-label">合格</div>
          </div>
          <div class="card-icon">
            <el-icon><CircleCheckFilled /></el-icon>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="overview-card danger">
          <div class="card-content">
            <div class="card-value">{{ statistics.unqualified }}</div>
            <div class="card-label">不合格</div>
          </div>
          <div class="card-icon">
            <el-icon><CircleCloseFilled /></el-icon>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="overview-card warning">
          <div class="card-content">
            <div class="card-value">{{ statistics.qualifiedRate }}%</div>
            <div class="card-label">合格率</div>
          </div>
          <div class="card-icon">
            <el-icon><DataLine /></el-icon>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 搜索和操作栏 -->
    <div class="action-bar card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="检查单号">
          <el-input
            v-model="searchForm.checkNumber"
            placeholder="请输入检查单号"
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
        <el-form-item label="检查类型">
          <el-select v-model="searchForm.type" placeholder="请选择检查类型" clearable>
            <el-option label="入库检查" value="in" />
            <el-option label="在库检查" value="stock" />
            <el-option label="出库检查" value="out" />
          </el-select>
        </el-form-item>
        <el-form-item label="检查结果">
          <el-select v-model="searchForm.result" placeholder="请选择检查结果" clearable>
            <el-option label="待检查" value="pending" />
            <el-option label="合格" value="qualified" />
            <el-option label="不合格" value="unqualified" />
          </el-select>
        </el-form-item>
        <el-form-item label="检查时间">
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
          新建检查
        </el-button>
        <el-button type="success" @click="handleBatchCheck">
          <el-icon><Check /></el-icon>
          批量检查
        </el-button>
        <el-button @click="handleExport">
          <el-icon><Download /></el-icon>
          导出数据
        </el-button>
      </div>
    </div>

    <!-- 检查任务列表 -->
    <div class="card">
      <el-table
        v-loading="loading"
        :data="checkList"
        border
        stripe
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column prop="checkNumber" label="检查单号" width="180" />
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
                <div class="product-batch">批次号：{{ row.batchNumber }}</div>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="检查类型" width="120">
          <template #default="{ row }">
            <el-tag :type="getCheckTypeTag(row.type)">
              {{ getCheckTypeText(row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="检查项目" width="200">
          <template #default="{ row }">
            <div class="check-items">
              <el-tag
                v-for="item in row.checkItems"
                :key="item"
                size="small"
                class="check-item"
              >
                {{ item }}
              </el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="检查结果" width="120">
          <template #default="{ row }">
            <el-tag :type="getResultTagType(row.result)">
              {{ getResultText(row.result) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="检查信息" width="180">
          <template #default="{ row }">
            <div class="check-info">
              <div>{{ row.inspector }}</div>
              <div class="check-time">{{ row.checkTime }}</div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button
              v-if="row.result === 'pending'"
              type="primary"
              link
              @click="handleCheck(row)"
            >
              检查
            </el-button>
            <el-button
              type="primary"
              link
              @click="handleView(row)"
            >
              查看
            </el-button>
            <el-button
              v-if="row.result === 'pending'"
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

    <!-- 检查对话框 -->
    <el-dialog
      v-model="checkDialog.visible"
      :title="'质量检查 - ' + checkDialog.checkNumber"
      width="800px"
      destroy-on-close
    >
      <el-form
        ref="checkFormRef"
        :model="checkForm"
        :rules="checkRules"
        label-width="120px"
      >
        <div class="check-form-header">
          <div class="product-info">
            <el-image
              :src="checkDialog.product?.image"
              :preview-src-list="[checkDialog.product?.image]"
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
              <div class="product-name">{{ checkDialog.product?.name }}</div>
              <div class="product-code">{{ checkDialog.product?.code }}</div>
              <div class="product-batch">批次号：{{ checkDialog.batchNumber }}</div>
            </div>
          </div>
        </div>

        <!-- 检查项目 -->
        <div
          v-for="(item, index) in checkForm.items"
          :key="index"
          class="check-item-form"
        >
          <div class="item-header">
            <h4>{{ item.name }}</h4>
            <el-tag :type="getItemResultType(item.result)" size="small">
              {{ getItemResultText(item.result) }}
            </el-tag>
          </div>
          <el-form-item
            :prop="'items.' + index + '.result'"
            :rules="{ required: true, message: '请选择检查结果', trigger: 'change' }"
          >
            <el-radio-group v-model="item.result">
              <el-radio label="qualified">合格</el-radio>
              <el-radio label="unqualified">不合格</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item
            :prop="'items.' + index + '.remark'"
            v-if="item.result === 'unqualified'"
          >
            <el-input
              v-model="item.remark"
              type="textarea"
              :rows="2"
              placeholder="请输入不合格原因"
            />
          </el-form-item>
        </div>

        <!-- 检查照片 -->
        <el-form-item label="检查照片" prop="images">
          <el-upload
            class="check-upload"
            action="/api/upload"
            list-type="picture-card"
            :on-preview="handlePictureCardPreview"
            :on-remove="handleRemove"
            :on-success="handleUploadSuccess"
            :before-upload="beforeUpload"
          >
            <el-icon><Plus /></el-icon>
          </el-upload>
          <el-dialog v-model="dialogVisible">
            <img w-full :src="dialogImageUrl" alt="Preview Image" />
          </el-dialog>
        </el-form-item>

        <!-- 检查结论 -->
        <el-form-item label="检查结论" prop="conclusion">
          <el-input
            v-model="checkForm.conclusion"
            type="textarea"
            :rows="3"
            placeholder="请输入检查结论"
          />
        </el-form-item>

        <!-- 处理建议 -->
        <el-form-item label="处理建议" prop="suggestion">
          <el-input
            v-model="checkForm.suggestion"
            type="textarea"
            :rows="2"
            placeholder="请输入处理建议"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="checkDialog.visible = false">取消</el-button>
          <el-button type="primary" @click="handleCheckSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Search, Refresh, Plus, Download, Picture, Timer,
  CircleCheckFilled, CircleCloseFilled, DataLine, Check
} from '@element-plus/icons-vue'

const router = useRouter()

// 统计数据
const statistics = reactive({
  pending: 10,
  qualified: 85,
  unqualified: 5,
  qualifiedRate: 94.4
})

// 搜索表单
const searchForm = reactive({
  checkNumber: '',
  keyword: '',
  type: '',
  result: '',
  timeRange: []
})

// 分页参数
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 加载状态
const loading = ref(false)

// 选中的检查任务
const selectedChecks = ref([])

// 检查任务列表数据
const checkList = ref([
  {
    id: 1,
    checkNumber: 'Q20240101001',
    product: {
      name: '新鲜生菜',
      code: 'VEG001',
      image: ''
    },
    batchNumber: 'B20240101001',
    type: 'in',
    checkItems: ['外观', '新鲜度', '包装'],
    result: 'pending',
    inspector: '',
    checkTime: ''
  }
])

// 检查对话框
const checkDialog = reactive({
  visible: false,
  checkNumber: '',
  product: null,
  batchNumber: ''
})

const checkFormRef = ref<FormInstance>()
const checkForm = reactive({
  items: [
    { name: '外观', result: '', remark: '' },
    { name: '新鲜度', result: '', remark: '' },
    { name: '包装', result: '', remark: '' }
  ],
  images: [],
  conclusion: '',
  suggestion: ''
})

const checkRules: FormRules = {
  conclusion: [
    { required: true, message: '请输入检查结论', trigger: 'blur' }
  ]
}

// 图片预览
const dialogImageUrl = ref('')
const dialogVisible = ref(false)

// 获取检查任务列表
const getCheckList = async () => {
  loading.value = true
  try {
    // TODO: 调用API获取检查任务列表
    // const res = await getChecks({ ...searchForm, page: page.value, pageSize: pageSize.value })
    // checkList.value = res.data.items
    // total.value = res.data.total
  } catch (error) {
    console.error('获取检查任务列表失败:', error)
    ElMessage.error('获取检查任务列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  page.value = 1
  getCheckList()
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
  getCheckList()
}

const handleCurrentChange = (val: number) => {
  page.value = val
  getCheckList()
}

// 新建检查
const handleCreate = () => {
  router.push('/quality/create')
}

// 批量检查
const handleBatchCheck = () => {
  if (selectedChecks.value.length === 0) {
    ElMessage.warning('请选择需要检查的任务')
    return
  }
  // TODO: 实现批量检查
  ElMessage.info('批量检查功能开发中')
}

// 导出数据
const handleExport = () => {
  // TODO: 实现导出功能
  ElMessage.info('导出功能开发中')
}

// 表格选择
const handleSelectionChange = (val: any[]) => {
  selectedChecks.value = val
}

// 检查
const handleCheck = (row: any) => {
  checkDialog.checkNumber = row.checkNumber
  checkDialog.product = row.product
  checkDialog.batchNumber = row.batchNumber
  checkDialog.visible = true
}

// 提交检查
const handleCheckSubmit = async () => {
  if (!checkFormRef.value) return
  
  try {
    await checkFormRef.value.validate()
    // TODO: 调用API提交检查结果
    ElMessage.success('检查完成')
    checkDialog.visible = false
    getCheckList()
  } catch (error) {
    console.error('提交失败:', error)
    ElMessage.error('提交失败，请检查表单')
  }
}

// 查看详情
const handleView = (row: any) => {
  router.push(`/quality/detail/${row.id}`)
}

// 删除检查任务
const handleDelete = (row: any) => {
  ElMessageBox.confirm(
    '确定要删除该检查任务吗？',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      // TODO: 调用API删除检查任务
      ElMessage.success('删除成功')
      getCheckList()
    } catch (error) {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

// 图片上传成功
const handleUploadSuccess = (response: any) => {
  checkForm.images.push(response.url)
}

// 移除图片
const handleRemove = (file: any) => {
  const index = checkForm.images.indexOf(file.url)
  if (index !== -1) {
    checkForm.images.splice(index, 1)
  }
}

// 预览图片
const handlePictureCardPreview = (file: any) => {
  dialogImageUrl.value = file.url
  dialogVisible.value = true
}

// 上传前检查
const beforeUpload = (file: File) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB!')
    return false
  }
  return true
}

// 获取检查类型标签
const getCheckTypeTag = (type: string) => {
  switch (type) {
    case 'in':
      return 'success'
    case 'stock':
      return 'warning'
    case 'out':
      return 'info'
    default:
      return 'info'
  }
}

// 获取检查类型文本
const getCheckTypeText = (type: string) => {
  switch (type) {
    case 'in':
      return '入库检查'
    case 'stock':
      return '在库检查'
    case 'out':
      return '出库检查'
    default:
      return '未知'
  }
}

// 获取结果标签类型
const getResultTagType = (result: string) => {
  switch (result) {
    case 'pending':
      return 'info'
    case 'qualified':
      return 'success'
    case 'unqualified':
      return 'danger'
    default:
      return 'info'
  }
}

// 获取结果文本
const getResultText = (result: string) => {
  switch (result) {
    case 'pending':
      return '待检查'
    case 'qualified':
      return '合格'
    case 'unqualified':
      return '不合格'
    default:
      return '未知'
  }
}

// 获取检查项结果类型
const getItemResultType = (result: string) => {
  switch (result) {
    case 'qualified':
      return 'success'
    case 'unqualified':
      return 'danger'
    default:
      return 'info'
  }
}

// 获取检查项结果文本
const getItemResultText = (result: string) => {
  switch (result) {
    case 'qualified':
      return '合格'
    case 'unqualified':
      return '不合格'
    default:
      return '未检查'
  }
}

onMounted(() => {
  getCheckList()
})
</script>

<style lang="scss" scoped>
.quality-check {
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

      &.success {
        background: linear-gradient(135deg, #66bb6a 0%, #43a047 100%);
      }

      &.danger {
        background: linear-gradient(135deg, #ef5350 0%, #e53935 100%);
      }

      &.warning {
        background: linear-gradient(135deg, #ffa726 0%, #fb8c00 100%);
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
        margin-bottom: 2px;
      }

      .product-batch {
        font-size: 12px;
        color: $text-regular;
      }
    }
  }

  .check-items {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;

    .check-item {
      margin: 0;
    }
  }

  .check-info {
    font-size: 13px;

    .check-time {
      color: $text-secondary;
      margin-top: 4px;
    }
  }

  .pagination-container {
    margin-top: $spacing-large;
    display: flex;
    justify-content: flex-end;
  }

  .check-form-header {
    margin-bottom: $spacing-large;
    padding-bottom: $spacing-base;
    border-bottom: 1px solid $border-color-light;

    .product-info {
      .product-image {
        width: 80px;
        height: 80px;
        border-radius: $border-radius-base;
      }

      .product-detail {
        .product-name {
          font-size: 16px;
        }
      }
    }
  }

  .check-item-form {
    margin-bottom: $spacing-large;
    padding: $spacing-base;
    border: 1px solid $border-color-light;
    border-radius: $border-radius-base;

    .item-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: $spacing-base;

      h4 {
        margin: 0;
        font-size: 14px;
        font-weight: 500;
      }
    }

    :deep(.el-form-item) {
      margin-bottom: $spacing-base;

      &:last-child {
        margin-bottom: 0;
      }
    }
  }

  .check-upload {
    :deep(.el-upload--picture-card) {
      width: 100px;
      height: 100px;
      line-height: 100px;
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