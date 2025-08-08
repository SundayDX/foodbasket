<template>
  <div class="quality-create">
    <div class="page-header">
      <div class="header-content">
        <h2>新建质量检查</h2>
        <el-breadcrumb>
          <el-breadcrumb-item :to="{ path: '/quality/check' }">质量检查</el-breadcrumb-item>
          <el-breadcrumb-item>新建检查</el-breadcrumb-item>
        </el-breadcrumb>
      </div>
    </div>

    <div class="page-content">
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
        class="create-form"
      >
        <!-- 基本信息 -->
        <div class="form-card">
          <div class="card-header">
            <h3>基本信息</h3>
          </div>
          <div class="card-content">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="检查类型" prop="type">
                  <el-select v-model="form.type" placeholder="请选择检查类型">
                    <el-option label="入库检查" value="in" />
                    <el-option label="在库检查" value="stock" />
                    <el-option label="出库检查" value="out" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="检查标准" prop="standardId">
                  <el-select v-model="form.standardId" placeholder="请选择检查标准">
                    <el-option
                      v-for="item in standards"
                      :key="item.id"
                      :label="item.name"
                      :value="item.id"
                    />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
          </div>
        </div>

        <!-- 商品信息 -->
        <div class="form-card">
          <div class="card-header">
            <h3>商品信息</h3>
          </div>
          <div class="card-content">
            <el-form-item label="选择商品" prop="productId">
              <el-select
                v-model="form.productId"
                placeholder="请选择商品"
                remote
                filterable
                :remote-method="searchProducts"
                :loading="productLoading"
              >
                <el-option
                  v-for="item in products"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id"
                >
                  <div class="product-option">
                    <el-image
                      :src="item.image"
                      :preview-src-list="[item.image]"
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
                      <div class="product-name">{{ item.name }}</div>
                      <div class="product-code">{{ item.code }}</div>
                    </div>
                  </div>
                </el-option>
              </el-select>
            </el-form-item>

            <el-form-item label="批次号" prop="batchNumber">
              <el-input v-model="form.batchNumber" placeholder="请输入批次号" />
            </el-form-item>

            <el-form-item label="检查数量" prop="quantity">
              <el-input-number
                v-model="form.quantity"
                :min="1"
                :precision="0"
                :step="1"
                placeholder="请输入检查数量"
              />
            </el-form-item>
          </div>
        </div>

        <!-- 检查项目 -->
        <div class="form-card">
          <div class="card-header">
            <h3>检查项目</h3>
            <el-button type="primary" link @click="handleAddItem">
              <el-icon><Plus /></el-icon>
              添加项目
            </el-button>
          </div>
          <div class="card-content">
            <div
              v-for="(item, index) in form.items"
              :key="index"
              class="check-item"
            >
              <el-row :gutter="20">
                <el-col :span="8">
                  <el-form-item
                    :prop="'items.' + index + '.name'"
                    :rules="{ required: true, message: '请输入项目名称', trigger: 'blur' }"
                  >
                    <el-input v-model="item.name" placeholder="项目名称" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item
                    :prop="'items.' + index + '.standard'"
                    :rules="{ required: true, message: '请输入检查标准', trigger: 'blur' }"
                  >
                    <el-input v-model="item.standard" placeholder="检查标准" />
                  </el-form-item>
                </el-col>
                <el-col :span="4" class="item-actions">
                  <el-button type="danger" link @click="handleRemoveItem(index)">
                    <el-icon><Delete /></el-icon>
                    删除
                  </el-button>
                </el-col>
              </el-row>
            </div>
          </div>
        </div>

        <!-- 备注信息 -->
        <div class="form-card">
          <div class="card-header">
            <h3>备注信息</h3>
          </div>
          <div class="card-content">
            <el-form-item label="备注" prop="remark">
              <el-input
                v-model="form.remark"
                type="textarea"
                :rows="3"
                placeholder="请输入备注信息"
              />
            </el-form-item>
          </div>
        </div>

        <!-- 表单操作 -->
        <div class="form-actions">
          <el-button @click="handleCancel">取消</el-button>
          <el-button type="primary" @click="handleSubmit">提交</el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus, Delete, Picture } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'

const router = useRouter()
const formRef = ref<FormInstance>()

// 表单数据
const form = reactive({
  type: '',
  standardId: '',
  productId: '',
  batchNumber: '',
  quantity: 1,
  items: [
    { name: '', standard: '' }
  ],
  remark: ''
})

// 表单验证规则
const rules: FormRules = {
  type: [
    { required: true, message: '请选择检查类型', trigger: 'change' }
  ],
  standardId: [
    { required: true, message: '请选择检查标准', trigger: 'change' }
  ],
  productId: [
    { required: true, message: '请选择商品', trigger: 'change' }
  ],
  batchNumber: [
    { required: true, message: '请输入批次号', trigger: 'blur' }
  ],
  quantity: [
    { required: true, message: '请输入检查数量', trigger: 'blur' }
  ]
}

// 检查标准列表
const standards = ref([
  { id: 1, name: '蔬菜类检查标准' },
  { id: 2, name: '水果类检查标准' },
  { id: 3, name: '肉类检查标准' }
])

// 商品列表
const products = ref([
  {
    id: 1,
    name: '新鲜生菜',
    code: 'VEG001',
    image: ''
  },
  {
    id: 2,
    name: '红富士苹果',
    code: 'FRU001',
    image: ''
  }
])

// 商品搜索加载状态
const productLoading = ref(false)

// 搜索商品
const searchProducts = async (query: string) => {
  if (query) {
    productLoading.value = true
    try {
      // TODO: 调用API搜索商品
      // const res = await searchProductsApi(query)
      // products.value = res.data
    } catch (error) {
      console.error('搜索商品失败:', error)
    } finally {
      productLoading.value = false
    }
  }
}

// 添加检查项目
const handleAddItem = () => {
  form.items.push({ name: '', standard: '' })
}

// 删除检查项目
const handleRemoveItem = (index: number) => {
  form.items.splice(index, 1)
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
    // TODO: 调用API提交表单
    ElMessage.success('创建成功')
    router.push('/quality/check')
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}
</script>

<style lang="scss" scoped>
.quality-create {
  .page-header {
    background-color: #fff;
    padding: $spacing-base $spacing-large;
    margin-bottom: $spacing-base;
    border-radius: $border-radius-base;
    box-shadow: $box-shadow-light;

    .header-content {
      h2 {
        margin: 0 0 $spacing-small;
        font-size: 20px;
        font-weight: 600;
        color: $text-primary;
      }
    }
  }

  .page-content {
    background-color: #fff;
    padding: $spacing-large;
    border-radius: $border-radius-base;
    box-shadow: $box-shadow-light;

    .form-card {
      margin-bottom: $spacing-extra-large;
      
      .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: $spacing-large;
        padding-bottom: $spacing-small;
        border-bottom: 1px solid $border-color-light;

        h3 {
          margin: 0;
          font-size: 16px;
          font-weight: 600;
          color: $text-primary;
        }
      }

      .card-content {
        .check-item {
          padding: $spacing-base;
          margin-bottom: $spacing-base;
          border: 1px solid $border-color-light;
          border-radius: $border-radius-base;

          &:last-child {
            margin-bottom: 0;
          }

          .item-actions {
            display: flex;
            align-items: center;
            justify-content: flex-end;
          }
        }
      }
    }

    .form-actions {
      display: flex;
      justify-content: center;
      gap: $spacing-base;
      padding-top: $spacing-large;
      border-top: 1px solid $border-color-light;
    }
  }
}

.product-option {
  display: flex;
  align-items: center;
  gap: $spacing-base;

  .product-image {
    width: 40px;
    height: 40px;
    border-radius: $border-radius-small;
  }

  .product-info {
    .product-name {
      font-size: 14px;
      margin-bottom: 2px;
    }

    .product-code {
      font-size: 12px;
      color: $text-secondary;
    }
  }
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
