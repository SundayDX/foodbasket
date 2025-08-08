<template>
  <div class="product-list">
    <!-- 搜索和操作栏 -->
    <div class="action-bar card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="商品名称">
          <el-input
            v-model="searchForm.name"
            placeholder="请输入商品名称"
            clearable
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item label="商品编码">
          <el-input
            v-model="searchForm.code"
            placeholder="请输入商品编码"
            clearable
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item label="商品类别">
          <el-select
            v-model="searchForm.category"
            placeholder="请选择商品类别"
            clearable
          >
            <el-option
              v-for="item in categoryOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="供应商">
          <el-select
            v-model="searchForm.supplier"
            placeholder="请选择供应商"
            clearable
            filterable
          >
            <el-option
              v-for="item in supplierOptions"
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
        <el-button type="primary" @click="handleAdd">
          <el-icon><Plus /></el-icon>
          新增商品
        </el-button>
        <el-button type="success" @click="handleImport">
          <el-icon><Upload /></el-icon>
          批量导入
        </el-button>
        <el-button @click="handleExport">
          <el-icon><Download /></el-icon>
          导出数据
        </el-button>
      </div>
    </div>

    <!-- 商品列表表格 -->
    <div class="card">
      <el-table
        v-loading="loading"
        :data="productList"
        border
        stripe
        style="width: 100%"
      >
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column label="商品图片" width="100" align="center">
          <template #default="{ row }">
            <el-image
              :src="row.image"
              :preview-src-list="[row.image]"
              fit="cover"
              class="product-image"
            >
              <template #error>
                <div class="image-placeholder">
                  <el-icon><Picture /></el-icon>
                </div>
              </template>
            </el-image>
          </template>
        </el-table-column>
        <el-table-column prop="code" label="商品编码" width="120" />
        <el-table-column prop="name" label="商品名称" min-width="150" show-overflow-tooltip />
        <el-table-column prop="category" label="类别" width="120" />
        <el-table-column prop="supplier" label="供应商" width="150" show-overflow-tooltip />
        <el-table-column prop="unit" label="单位" width="80" align="center" />
        <el-table-column label="价格信息" width="200">
          <template #default="{ row }">
            <div class="price-info">
              <div class="price-item">
                <span class="label">采购价：</span>
                <span class="value">￥{{ row.purchase_price }}</span>
              </div>
              <div class="price-item">
                <span class="label">销售价：</span>
                <span class="value">￥{{ row.selling_price }}</span>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="库存" width="100" align="center">
          <template #default="{ row }">
            <el-tag
              :type="getStockTagType(row.inventory?.quantity)"
              size="small"
            >
              {{ row.inventory?.quantity || 0 }} {{ row.unit }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button
              type="primary"
              link
              @click="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              type="primary"
              link
              @click="handleView(row)"
            >
              查看
            </el-button>
            <el-popconfirm
              title="确定要删除该商品吗？"
              @confirm="handleDelete(row)"
            >
              <template #reference>
                <el-button
                  type="danger"
                  link
                >
                  删除
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

    <!-- 新增/编辑商品对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '新增商品' : '编辑商品'"
      width="700px"
      destroy-on-close
    >
      <el-form
        ref="productFormRef"
        :model="productForm"
        :rules="productRules"
        label-width="100px"
        class="product-form"
      >
        <el-form-item label="商品名称" prop="name">
          <el-input v-model="productForm.name" placeholder="请输入商品名称" />
        </el-form-item>
        <el-form-item label="商品编码" prop="code">
          <el-input v-model="productForm.code" placeholder="请输入商品编码" />
        </el-form-item>
        <el-form-item label="商品类别" prop="category">
          <el-select
            v-model="productForm.category"
            placeholder="请选择商品类别"
            class="full-width"
          >
            <el-option
              v-for="item in categoryOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="供应商" prop="supplier">
          <el-select
            v-model="productForm.supplier"
            placeholder="请选择供应商"
            filterable
            class="full-width"
          >
            <el-option
              v-for="item in supplierOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="单位" prop="unit">
          <el-input v-model="productForm.unit" placeholder="请输入单位" />
        </el-form-item>
        <el-form-item label="采购价" prop="purchase_price">
          <el-input-number
            v-model="productForm.purchase_price"
            :precision="2"
            :step="0.1"
            :min="0"
            class="full-width"
          />
        </el-form-item>
        <el-form-item label="销售价" prop="selling_price">
          <el-input-number
            v-model="productForm.selling_price"
            :precision="2"
            :step="0.1"
            :min="0"
            class="full-width"
          />
        </el-form-item>
        <el-form-item label="商品图片" prop="image">
          <el-upload
            class="product-upload"
            action="/api/upload"
            :show-file-list="false"
            :on-success="handleUploadSuccess"
            :before-upload="beforeUpload"
          >
            <img v-if="productForm.image" :src="productForm.image" class="upload-image">
            <el-icon v-else class="upload-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item label="商品描述" prop="description">
          <el-input
            v-model="productForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入商品描述"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Refresh, Plus, Upload, Download, Picture } from '@element-plus/icons-vue'

// 搜索表单
const searchForm = reactive({
  name: '',
  code: '',
  category: '',
  supplier: ''
})

// 分页参数
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 加载状态
const loading = ref(false)

// 商品列表数据
const productList = ref([])

// 类别和供应商选项（实际应该从API获取）
const categoryOptions = [
  { value: '蔬菜', label: '蔬菜' },
  { value: '水果', label: '水果' },
  { value: '肉类', label: '肉类' },
  { value: '海鲜', label: '海鲜' }
]

const supplierOptions = [
  { value: '供应商A', label: '供应商A' },
  { value: '供应商B', label: '供应商B' },
  { value: '供应商C', label: '供应商C' }
]

// 对话框相关
const dialogVisible = ref(false)
const dialogType = ref<'add' | 'edit'>('add')
const productFormRef = ref<FormInstance>()

// 商品表单
const productForm = reactive({
  name: '',
  code: '',
  category: '',
  supplier: '',
  unit: '',
  purchase_price: 0,
  selling_price: 0,
  image: '',
  description: ''
})

// 表单验证规则
const productRules: FormRules = {
  name: [
    { required: true, message: '请输入商品名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入商品编码', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择商品类别', trigger: 'change' }
  ],
  supplier: [
    { required: true, message: '请选择供应商', trigger: 'change' }
  ],
  unit: [
    { required: true, message: '请输入单位', trigger: 'blur' }
  ],
  purchase_price: [
    { required: true, message: '请输入采购价', trigger: 'blur' }
  ],
  selling_price: [
    { required: true, message: '请输入销售价', trigger: 'blur' }
  ]
}

// 获取商品列表
const getProductList = async () => {
  loading.value = true
  try {
    // TODO: 调用API获取商品列表
    // const res = await getProducts({ ...searchForm, page: page.value, pageSize: pageSize.value })
    // productList.value = res.data.items
    // total.value = res.data.total
  } catch (error) {
    console.error('获取商品列表失败:', error)
    ElMessage.error('获取商品列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  page.value = 1
  getProductList()
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
  getProductList()
}

const handleCurrentChange = (val: number) => {
  page.value = val
  getProductList()
}

// 新增商品
const handleAdd = () => {
  dialogType.value = 'add'
  Object.keys(productForm).forEach(key => {
    productForm[key] = ''
  })
  productForm.purchase_price = 0
  productForm.selling_price = 0
  dialogVisible.value = true
}

// 编辑商品
const handleEdit = (row: any) => {
  dialogType.value = 'edit'
  Object.keys(productForm).forEach(key => {
    productForm[key] = row[key]
  })
  dialogVisible.value = true
}

// 查看商品
const handleView = (row: any) => {
  // TODO: 实现商品详情查看
}

// 删除商品
const handleDelete = async (row: any) => {
  try {
    // TODO: 调用API删除商品
    // await deleteProduct(row.id)
    ElMessage.success('删除成功')
    getProductList()
  } catch (error) {
    console.error('删除商品失败:', error)
    ElMessage.error('删除商品失败')
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!productFormRef.value) return
  
  try {
    await productFormRef.value.validate()
    // TODO: 调用API保存商品
    // if (dialogType.value === 'add') {
    //   await createProduct(productForm)
    // } else {
    //   await updateProduct(productForm)
    // }
    ElMessage.success(dialogType.value === 'add' ? '添加成功' : '更新成功')
    dialogVisible.value = false
    getProductList()
  } catch (error) {
    console.error('保存商品失败:', error)
    ElMessage.error('保存失败，请检查表单')
  }
}

// 文件上传
const handleUploadSuccess = (response: any) => {
  productForm.image = response.url
  ElMessage.success('上传成功')
}

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

// 获取库存标签类型
const getStockTagType = (quantity: number) => {
  if (!quantity || quantity === 0) return 'danger'
  if (quantity < 10) return 'warning'
  return 'success'
}

// 批量导入
const handleImport = () => {
  // TODO: 实现批量导入功能
}

// 导出数据
const handleExport = () => {
  // TODO: 实现数据导出功能
}

onMounted(() => {
  getProductList()
})
</script>

<style lang="scss" scoped>
.product-list {
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
}

.product-image {
  width: 60px;
  height: 60px;
  border-radius: $border-radius-small;
}

.image-placeholder {
  width: 60px;
  height: 60px;
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

.price-info {
  .price-item {
    display: flex;
    justify-content: space-between;
    margin-bottom: 4px;
    
    &:last-child {
      margin-bottom: 0;
    }
    
    .label {
      color: $text-secondary;
    }
    
    .value {
      color: $text-primary;
      font-weight: 500;
    }
  }
}

.pagination-container {
  margin-top: $spacing-large;
  display: flex;
  justify-content: flex-end;
}

.product-form {
  .full-width {
    width: 100%;
  }
  
  .product-upload {
    :deep(.el-upload) {
      width: 120px;
      height: 120px;
      border: 1px dashed $border-color-base;
      border-radius: $border-radius-base;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      
      &:hover {
        border-color: $primary-color;
      }
    }
    
    .upload-image {
      width: 118px;
      height: 118px;
      object-fit: cover;
    }
    
    .upload-icon {
      font-size: 28px;
      color: $text-secondary;
    }
  }
}
</style>