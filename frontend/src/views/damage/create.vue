<template>
  <div class="damage-create">
    <div class="page-header card">
      <div class="header-content">
        <h2>{{ isEdit ? '编辑报损单' : '新建报损单' }}</h2>
        <div class="header-actions">
          <el-button @click="handleCancel">取消</el-button>
          <el-button type="primary" @click="handleSubmit">提交</el-button>
        </div>
      </div>
    </div>

    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
      class="damage-form"
    >
      <!-- 基本信息 -->
      <div class="form-section card">
        <h3 class="section-title">基本信息</h3>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="报损单号" prop="damageNumber">
              <el-input
                v-model="form.damageNumber"
                placeholder="系统自动生成"
                disabled
              />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="报损类型" prop="type">
              <el-select
                v-model="form.type"
                placeholder="请选择报损类型"
                class="full-width"
              >
                <el-option label="自然损耗" value="natural" />
                <el-option label="运输损坏" value="transport" />
                <el-option label="质量问题" value="quality" />
                <el-option label="其他" value="other" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="报损时间" prop="reportTime">
              <el-date-picker
                v-model="form.reportTime"
                type="datetime"
                placeholder="请选择报损时间"
                class="full-width"
              />
            </el-form-item>
          </el-col>
        </el-row>
      </div>

      <!-- 商品信息 -->
      <div class="form-section card">
        <h3 class="section-title">商品信息</h3>
        <el-form-item prop="productId">
          <el-select
            v-model="form.productId"
            placeholder="请选择商品"
            filterable
            remote
            :remote-method="handleProductSearch"
            :loading="productLoading"
            class="product-select"
            @change="handleProductChange"
          >
            <el-option
              v-for="item in productOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
              <div class="product-option">
                <el-image
                  :src="item.image"
                  fit="cover"
                  class="product-image"
                >
                  <template #error>
                    <div class="image-placeholder">
                      <el-icon><Picture /></el-icon>
                    </div>
                  </template>
                </el-image>
                <div class="product-info">
                  <div class="product-name">{{ item.label }}</div>
                  <div class="product-code">{{ item.code }}</div>
                  <div class="product-stock">
                    库存：{{ item.stock }} {{ item.unit }}
                  </div>
                </div>
              </div>
            </el-option>
          </el-select>
        </el-form-item>

        <div v-if="selectedProduct" class="selected-product">
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="批次号" prop="batchNumber">
                <el-select
                  v-model="form.batchNumber"
                  placeholder="请选择批次"
                  class="full-width"
                >
                  <el-option
                    v-for="item in batchOptions"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  >
                    <div class="batch-info">
                      <div class="batch-number">{{ item.label }}</div>
                      <div class="batch-stock">
                        库存：{{ item.stock }} {{ selectedProduct.unit }}
                      </div>
                    </div>
                  </el-option>
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="报损数量" prop="quantity">
                <el-input-number
                  v-model="form.quantity"
                  :min="0.01"
                  :max="maxQuantity"
                  :precision="2"
                  :step="1"
                  class="full-width"
                  @change="handleQuantityChange"
                >
                  <template #suffix>{{ selectedProduct.unit }}</template>
                </el-input-number>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="报损金额">
                <el-input
                  v-model="form.amount"
                  placeholder="系统自动计算"
                  disabled
                >
                  <template #prefix>￥</template>
                </el-input>
              </el-form-item>
            </el-col>
          </el-row>
        </div>
      </div>

      <!-- 报损原因 -->
      <div class="form-section card">
        <h3 class="section-title">报损原因</h3>
        <el-form-item prop="reason">
          <el-input
            v-model="form.reason"
            type="textarea"
            :rows="3"
            placeholder="请详细描述报损原因"
          />
        </el-form-item>
      </div>

      <!-- 现场照片 -->
      <div class="form-section card">
        <h3 class="section-title">现场照片</h3>
        <el-form-item prop="images">
          <el-upload
            class="damage-upload"
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
        <div class="upload-tip">
          提示：请上传清晰的商品损坏照片，支持JPG/PNG格式，单张不超过2MB
        </div>
      </div>

      <!-- 处理建议 -->
      <div class="form-section card">
        <h3 class="section-title">处理建议</h3>
        <el-form-item label="处理方式" prop="handlingMethod">
          <el-select
            v-model="form.handlingMethod"
            placeholder="请选择处理方式"
          >
            <el-option label="销毁" value="destroy" />
            <el-option label="降价销售" value="discount" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="补充说明" prop="notes">
          <el-input
            v-model="form.notes"
            type="textarea"
            :rows="2"
            placeholder="请输入补充说明"
          />
        </el-form-item>
      </div>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
import { Picture, Plus } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const formRef = ref<FormInstance>()

// 判断是否为编辑模式
const isEdit = computed(() => route.query.id !== undefined)

// 表单数据
const form = reactive({
  damageNumber: '',
  type: '',
  reportTime: '',
  productId: '',
  batchNumber: '',
  quantity: 0,
  amount: '',
  reason: '',
  images: [],
  handlingMethod: '',
  notes: ''
})

// 表单验证规则
const rules: FormRules = {
  type: [
    { required: true, message: '请选择报损类型', trigger: 'change' }
  ],
  reportTime: [
    { required: true, message: '请选择报损时间', trigger: 'change' }
  ],
  productId: [
    { required: true, message: '请选择商品', trigger: 'change' }
  ],
  batchNumber: [
    { required: true, message: '请选择批次号', trigger: 'change' }
  ],
  quantity: [
    { required: true, message: '请输入报损数量', trigger: 'blur' },
    { type: 'number', min: 0.01, message: '报损数量必须大于0', trigger: 'blur' }
  ],
  reason: [
    { required: true, message: '请输入报损原因', trigger: 'blur' }
  ],
  images: [
    { required: true, message: '请上传现场照片', trigger: 'change' }
  ],
  handlingMethod: [
    { required: true, message: '请选择处理方式', trigger: 'change' }
  ]
}

// 商品选择相关
const productLoading = ref(false)
const productOptions = ref([
  {
    value: 1,
    label: '新鲜生菜',
    code: 'VEG001',
    image: '',
    stock: 100,
    unit: 'kg',
    price: 5.00
  }
])
const selectedProduct = ref(null)

// 批次选项
const batchOptions = ref([
  {
    value: 'B20240101001',
    label: 'B20240101001',
    stock: 50
  }
])

// 最大可报损数量
const maxQuantity = computed(() => {
  if (!selectedProduct.value || !form.batchNumber) return 0
  const batch = batchOptions.value.find(item => item.value === form.batchNumber)
  return batch ? batch.stock : 0
})

// 图片预览
const dialogImageUrl = ref('')
const dialogVisible = ref(false)

// 搜索商品
const handleProductSearch = async (query: string) => {
  if (query) {
    productLoading.value = true
    try {
      // TODO: 调用API搜索商品
      // const res = await searchProducts(query)
      // productOptions.value = res.data
    } catch (error) {
      console.error('搜索商品失败:', error)
    } finally {
      productLoading.value = false
    }
  }
}

// 选择商品
const handleProductChange = async (value: number) => {
  const product = productOptions.value.find(item => item.value === value)
  if (product) {
    selectedProduct.value = product
    form.quantity = 0
    form.amount = ''
    // TODO: 获取商品批次
    // const res = await getProductBatches(value)
    // batchOptions.value = res.data
  }
}

// 数量变更
const handleQuantityChange = (value: number) => {
  if (selectedProduct.value) {
    form.amount = (value * selectedProduct.value.price).toFixed(2)
  }
}

// 图片上传成功
const handleUploadSuccess = (response: any) => {
  form.images.push(response.url)
}

// 移除图片
const handleRemove = (file: any) => {
  const index = form.images.indexOf(file.url)
  if (index !== -1) {
    form.images.splice(index, 1)
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

// 取消
const handleCancel = () => {
  router.back()
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    // TODO: 调用API保存报损单
    ElMessage.success(isEdit.value ? '更新成功' : '提交成功')
    router.push('/damage/list')
  } catch (error) {
    console.error('提交失败:', error)
    ElMessage.error('提交失败，请检查表单')
  }
}
</script>

<style lang="scss" scoped>
.damage-create {
  .page-header {
    margin-bottom: $spacing-base;

    .header-content {
      display: flex;
      justify-content: space-between;
      align-items: center;

      h2 {
        margin: 0;
        font-size: 20px;
        font-weight: 600;
      }

      .header-actions {
        display: flex;
        gap: $spacing-base;
      }
    }
  }

  .form-section {
    margin-bottom: $spacing-base;

    .section-title {
      margin: 0 0 $spacing-large;
      font-size: 16px;
      font-weight: 600;
    }
  }

  .product-select {
    width: 100%;
  }

  .product-option {
    display: flex;
    align-items: center;
    gap: $spacing-base;
    padding: $spacing-small 0;

    .product-image {
      width: 40px;
      height: 40px;
      border-radius: $border-radius-small;
    }

    .product-info {
      .product-name {
        font-weight: 500;
        margin-bottom: 2px;
      }

      .product-code {
        font-size: 12px;
        color: $text-secondary;
        margin-bottom: 2px;
      }

      .product-stock {
        font-size: 12px;
        color: $text-regular;
      }
    }
  }

  .batch-info {
    .batch-number {
      font-weight: 500;
      margin-bottom: 2px;
    }

    .batch-stock {
      font-size: 12px;
      color: $text-regular;
    }
  }

  .damage-upload {
    :deep(.el-upload--picture-card) {
      width: 120px;
      height: 120px;
      line-height: 120px;
    }
  }

  .upload-tip {
    font-size: 12px;
    color: $text-secondary;
    margin-top: $spacing-small;
  }
}

.full-width {
  width: 100%;
}

.image-placeholder {
  width: 40px;
  height: 40px;
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