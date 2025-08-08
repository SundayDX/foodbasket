<template>
  <div class="delivery-create">
    <div class="page-header card">
      <div class="header-content">
        <h2>{{ isEdit ? '编辑配送单' : '新建配送单' }}</h2>
        <div class="header-actions">
          <el-button @click="handleCancel">取消</el-button>
          <el-button type="primary" @click="handleSubmit">保存</el-button>
        </div>
      </div>
    </div>

    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
      class="delivery-form"
    >
      <!-- 基本信息 -->
      <div class="form-section card">
        <h3 class="section-title">基本信息</h3>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="配送单号" prop="deliveryNumber">
              <el-input
                v-model="form.deliveryNumber"
                placeholder="系统自动生成"
                disabled
              />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="预计发货时间" prop="plannedStartTime">
              <el-date-picker
                v-model="form.plannedStartTime"
                type="datetime"
                placeholder="请选择预计发货时间"
                class="full-width"
              />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="配送车辆" prop="vehicleNumber">
              <el-select
                v-model="form.vehicleNumber"
                placeholder="请选择配送车辆"
                class="full-width"
              >
                <el-option
                  v-for="item in vehicleOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="配送司机" prop="driverId">
              <el-select
                v-model="form.driverId"
                placeholder="请选择配送司机"
                class="full-width"
                @change="handleDriverChange"
              >
                <el-option
                  v-for="item in driverOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="联系电话">
              <el-input
                v-model="driverPhone"
                placeholder="司机联系电话"
                disabled
              />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="预计配送时长" prop="estimatedDuration">
              <el-input-number
                v-model="form.estimatedDuration"
                :min="1"
                :max="24"
                class="full-width"
              >
                <template #suffix>小时</template>
              </el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
      </div>

      <!-- 配送商品 -->
      <div class="form-section card">
        <div class="section-header">
          <h3 class="section-title">配送商品</h3>
          <el-button type="primary" @click="handleAddProduct">
            <el-icon><Plus /></el-icon>
            添加商品
          </el-button>
        </div>
        
        <el-table
          :data="form.products"
          border
          style="width: 100%"
        >
          <el-table-column label="商品信息" min-width="300">
            <template #default="{ row }">
              <el-form-item
                :prop="'products.' + $index + '.productId'"
                :rules="{ required: true, message: '请选择商品', trigger: 'change' }"
              >
                <el-select
                  v-model="row.productId"
                  placeholder="请选择商品"
                  filterable
                  class="full-width"
                  @change="(val) => handleProductChange(val, $index)"
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
                      </div>
                    </div>
                  </el-option>
                </el-select>
              </el-form-item>
            </template>
          </el-table-column>
          <el-table-column label="单价" width="150">
            <template #default="{ row }">
              <span>￥{{ row.unitPrice }}</span>
            </template>
          </el-table-column>
          <el-table-column label="数量" width="200">
            <template #default="{ row, $index }">
              <el-form-item
                :prop="'products.' + $index + '.quantity'"
                :rules="{ required: true, message: '请输入数量', trigger: 'blur' }"
              >
                <el-input-number
                  v-model="row.quantity"
                  :min="1"
                  :precision="2"
                  :step="1"
                  @change="handleQuantityChange($index)"
                />
              </el-form-item>
            </template>
          </el-table-column>
          <el-table-column label="总价" width="150">
            <template #default="{ row }">
              <span class="total-price">￥{{ row.totalPrice }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="100" fixed="right">
            <template #default="{ $index }">
              <el-button
                type="danger"
                link
                @click="handleRemoveProduct($index)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="products-summary">
          <span class="summary-item">
            商品种类：<strong>{{ form.products.length }}</strong>
          </span>
          <span class="summary-item">
            商品总数：<strong>{{ getTotalQuantity() }}</strong>
          </span>
          <span class="summary-item">
            总金额：<strong class="total-amount">￥{{ getTotalAmount() }}</strong>
          </span>
        </div>
      </div>

      <!-- 配送路线 -->
      <div class="form-section card">
        <div class="section-header">
          <h3 class="section-title">配送路线</h3>
          <el-button type="primary" @click="handleAddPoint">
            <el-icon><Plus /></el-icon>
            添加配送点
          </el-button>
        </div>

        <div class="route-container">
          <!-- 配送点列表 -->
          <div class="delivery-points">
            <el-table
              :data="form.deliveryPoints"
              border
              style="width: 100%"
              row-key="id"
              :max-height="500"
            >
              <el-table-column type="index" label="序号" width="60" />
              <el-table-column label="配送点信息" min-width="300">
                <template #default="{ row, $index }">
                  <el-form-item
                    :prop="'deliveryPoints.' + $index + '.address'"
                    :rules="{ required: true, message: '请输入配送地址', trigger: 'blur' }"
                  >
                    <div class="point-info">
                      <el-input
                        v-model="row.address"
                        placeholder="请输入配送地址"
                        @change="handleAddressChange($index)"
                      >
                        <template #append>
                          <el-button @click="handleSelectOnMap($index)">
                            <el-icon><Location /></el-icon>
                          </el-button>
                        </template>
                      </el-input>
                      <div class="contact-info">
                        <el-input
                          v-model="row.contactName"
                          placeholder="联系人"
                          class="contact-input"
                        />
                        <el-input
                          v-model="row.contactPhone"
                          placeholder="联系电话"
                          class="contact-input"
                        />
                      </div>
                    </div>
                  </el-form-item>
                </template>
              </el-table-column>
              <el-table-column label="预计到达时间" width="200">
                <template #default="{ row, $index }">
                  <el-form-item
                    :prop="'deliveryPoints.' + $index + '.plannedTime'"
                    :rules="{ required: true, message: '请选择预计到达时间', trigger: 'change' }"
                  >
                    <el-time-picker
                      v-model="row.plannedTime"
                      placeholder="请选择时间"
                      format="HH:mm"
                    />
                  </el-form-item>
                </template>
              </el-table-column>
              <el-table-column label="备注" min-width="150">
                <template #default="{ row }">
                  <el-input
                    v-model="row.notes"
                    placeholder="请输入备注信息"
                  />
                </template>
              </el-table-column>
              <el-table-column label="操作" width="150" fixed="right">
                <template #default="{ $index }">
                  <el-button
                    type="primary"
                    link
                    @click="handleMoveUp($index)"
                    :disabled="$index === 0"
                  >
                    上移
                  </el-button>
                  <el-button
                    type="primary"
                    link
                    @click="handleMoveDown($index)"
                    :disabled="$index === form.deliveryPoints.length - 1"
                  >
                    下移
                  </el-button>
                  <el-button
                    type="danger"
                    link
                    @click="handleRemovePoint($index)"
                  >
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>

          <!-- 地图容器 -->
          <div class="map-container">
            <div id="mapContainer" class="map"></div>
          </div>
        </div>
      </div>

      <!-- 备注信息 -->
      <div class="form-section card">
        <h3 class="section-title">备注信息</h3>
        <el-form-item prop="notes">
          <el-input
            v-model="form.notes"
            type="textarea"
            :rows="3"
            placeholder="请输入配送单备注信息"
          />
        </el-form-item>
      </div>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
import { Plus, Picture, Location } from '@element-plus/icons-vue'
import AMapLoader from '@amap/amap-jsapi-loader'

const route = useRoute()
const router = useRouter()
const formRef = ref<FormInstance>()

// 判断是否为编辑模式
const isEdit = computed(() => route.query.id !== undefined)

// 表单数据
const form = reactive({
  deliveryNumber: '',
  plannedStartTime: '',
  vehicleNumber: '',
  driverId: '',
  estimatedDuration: 1,
  products: [],
  deliveryPoints: [],
  notes: ''
})

// 表单验证规则
const rules: FormRules = {
  plannedStartTime: [
    { required: true, message: '请选择预计发货时间', trigger: 'change' }
  ],
  vehicleNumber: [
    { required: true, message: '请选择配送车辆', trigger: 'change' }
  ],
  driverId: [
    { required: true, message: '请选择配送司机', trigger: 'change' }
  ],
  estimatedDuration: [
    { required: true, message: '请输入预计配送时长', trigger: 'blur' }
  ]
}

// 选项数据
const vehicleOptions = [
  { value: '京A12345', label: '京A12345 (2.5吨货车)' },
  { value: '京B12345', label: '京B12345 (4.2吨货车)' }
]

const driverOptions = [
  { value: 1, label: '张三', phone: '13800138000' },
  { value: 2, label: '李四', phone: '13800138001' }
]

const productOptions = [
  {
    value: 1,
    label: '新鲜生菜',
    code: 'VEG001',
    image: '',
    price: 5.00,
    unit: 'kg'
  }
]

// 司机电话
const driverPhone = ref('')

// 地图实例
let map: any = null
let markers: any[] = []
let polyline: any = null

// 初始化地图
const initMap = async () => {
  try {
    const AMap = await AMapLoader.load({
      key: 'your-amap-key',
      version: '2.0'
    })
    
    map = new AMap.Map('mapContainer', {
      zoom: 11,
      center: [116.397428, 39.90923]
    })
  } catch (error) {
    console.error('地图加载失败:', error)
    ElMessage.error('地图加载失败')
  }
}

// 更新地图标记
const updateMapMarkers = () => {
  if (!map) return

  // 清除现有标记
  markers.forEach(marker => marker.remove())
  markers = []
  if (polyline) {
    polyline.remove()
  }

  // 添加新标记
  const points = form.deliveryPoints.map((point, index) => {
    const marker = new AMap.Marker({
      position: [point.longitude, point.latitude],
      label: {
        content: `${index + 1}`,
        direction: 'top'
      }
    })
    markers.push(marker)
    return [point.longitude, point.latitude]
  })

  // 添加路线
  if (points.length > 1) {
    polyline = new AMap.Polyline({
      path: points,
      strokeColor: '#409EFF',
      strokeWeight: 6
    })
    map.add(polyline)
  }

  map.add(markers)
  if (points.length > 0) {
    map.setFitView()
  }
}

// 处理司机选择
const handleDriverChange = (value: number) => {
  const driver = driverOptions.find(item => item.value === value)
  driverPhone.value = driver?.phone || ''
}

// 处理商品选择
const handleProductChange = (value: number, index: number) => {
  const product = productOptions.find(item => item.value === value)
  if (product) {
    form.products[index] = {
      ...form.products[index],
      productId: value,
      unitPrice: product.price,
      totalPrice: product.price * (form.products[index].quantity || 1)
    }
  }
}

// 处理数量变更
const handleQuantityChange = (index: number) => {
  const product = form.products[index]
  product.totalPrice = product.unitPrice * product.quantity
}

// 添加商品
const handleAddProduct = () => {
  form.products.push({
    productId: '',
    quantity: 1,
    unitPrice: 0,
    totalPrice: 0
  })
}

// 移除商品
const handleRemoveProduct = (index: number) => {
  form.products.splice(index, 1)
}

// 获取商品总数
const getTotalQuantity = () => {
  return form.products.reduce((sum, item) => sum + (item.quantity || 0), 0)
}

// 获取总金额
const getTotalAmount = () => {
  return form.products.reduce((sum, item) => sum + (item.totalPrice || 0), 0).toFixed(2)
}

// 添加配送点
const handleAddPoint = () => {
  form.deliveryPoints.push({
    address: '',
    contactName: '',
    contactPhone: '',
    plannedTime: '',
    notes: '',
    longitude: 0,
    latitude: 0
  })
}

// 移除配送点
const handleRemovePoint = (index: number) => {
  form.deliveryPoints.splice(index, 1)
  updateMapMarkers()
}

// 移动配送点顺序
const handleMoveUp = (index: number) => {
  if (index > 0) {
    const temp = form.deliveryPoints[index]
    form.deliveryPoints[index] = form.deliveryPoints[index - 1]
    form.deliveryPoints[index - 1] = temp
    updateMapMarkers()
  }
}

const handleMoveDown = (index: number) => {
  if (index < form.deliveryPoints.length - 1) {
    const temp = form.deliveryPoints[index]
    form.deliveryPoints[index] = form.deliveryPoints[index + 1]
    form.deliveryPoints[index + 1] = temp
    updateMapMarkers()
  }
}

// 地址变更
const handleAddressChange = async (index: number) => {
  // TODO: 调用地图API进行地址解析
}

// 在地图上选择位置
const handleSelectOnMap = (index: number) => {
  // TODO: 实现地图选点功能
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
    // TODO: 调用API保存配送单
    ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
    router.push('/delivery/list')
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败，请检查表单')
  }
}

onMounted(() => {
  initMap()
  if (isEdit.value) {
    // TODO: 获取配送单详情
  }
})
</script>

<style lang="scss" scoped>
.delivery-create {
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

    .section-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: $spacing-large;

      .section-title {
        margin: 0;
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
        font-weight: 500;
        margin-bottom: 2px;
      }

      .product-code {
        font-size: 12px;
        color: $text-secondary;
      }
    }
  }

  .products-summary {
    margin-top: $spacing-base;
    display: flex;
    justify-content: flex-end;
    gap: $spacing-large;

    .summary-item {
      color: $text-regular;

      strong {
        color: $text-primary;
        margin-left: 4px;

        &.total-amount {
          color: $danger-color;
          font-size: 16px;
        }
      }
    }
  }

  .route-container {
    display: grid;
    grid-template-columns: 1fr 400px;
    gap: $spacing-base;

    .map-container {
      height: 500px;
      border-radius: $border-radius-base;
      overflow: hidden;

      .map {
        width: 100%;
        height: 100%;
      }
    }
  }

  .point-info {
    .contact-info {
      display: flex;
      gap: $spacing-base;
      margin-top: $spacing-small;

      .contact-input {
        width: 50%;
      }
    }
  }
}

.full-width {
  width: 100%;
}

.total-price {
  color: $danger-color;
  font-weight: 500;
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