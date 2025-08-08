<template>
  <div class="delivery-detail">
    <!-- 页面头部 -->
    <div class="page-header card">
      <div class="header-content">
        <div class="header-left">
          <h2>配送单详情</h2>
          <el-tag
            :type="getStatusTagType(delivery.status)"
            class="status-tag"
          >
            {{ getStatusText(delivery.status) }}
          </el-tag>
        </div>
        <div class="header-actions">
          <el-button @click="handleBack">返回</el-button>
          <el-button
            v-if="delivery.status === 'delivering'"
            type="success"
            @click="handleComplete"
          >
            完成配送
          </el-button>
          <el-button
            v-if="delivery.status === 'pending'"
            type="primary"
            @click="handleEdit"
          >
            编辑
          </el-button>
        </div>
      </div>
    </div>

    <el-row :gutter="20" class="detail-container">
      <!-- 左侧信息区 -->
      <el-col :span="16">
        <!-- 基本信息 -->
        <div class="info-section card">
          <h3 class="section-title">基本信息</h3>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="配送单号">
              {{ delivery.deliveryNumber }}
            </el-descriptions-item>
            <el-descriptions-item label="创建时间">
              {{ delivery.createTime }}
            </el-descriptions-item>
            <el-descriptions-item label="配送司机">
              <div class="driver-info">
                <span>{{ delivery.driver?.name }}</span>
                <el-tag size="small" type="info">{{ delivery.driver?.phone }}</el-tag>
              </div>
            </el-descriptions-item>
            <el-descriptions-item label="车牌号">
              {{ delivery.vehicleNumber }}
            </el-descriptions-item>
            <el-descriptions-item label="发货时间">
              {{ delivery.startTime || '未发货' }}
            </el-descriptions-item>
            <el-descriptions-item label="完成时间">
              {{ delivery.endTime || '未完成' }}
            </el-descriptions-item>
          </el-descriptions>
        </div>

        <!-- 配送商品 -->
        <div class="info-section card">
          <h3 class="section-title">配送商品</h3>
          <el-table
            :data="delivery.products"
            border
            style="width: 100%"
          >
            <el-table-column label="商品信息" min-width="300">
              <template #default="{ row }">
                <div class="product-info">
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
                  <div class="product-detail">
                    <div class="product-name">{{ row.name }}</div>
                    <div class="product-code">{{ row.code }}</div>
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="unitPrice" label="单价" width="120">
              <template #default="{ row }">
                ￥{{ row.unitPrice }}
              </template>
            </el-table-column>
            <el-table-column prop="quantity" label="数量" width="120">
              <template #default="{ row }">
                {{ row.quantity }} {{ row.unit }}
              </template>
            </el-table-column>
            <el-table-column label="总价" width="120">
              <template #default="{ row }">
                <span class="total-price">￥{{ row.totalPrice }}</span>
              </template>
            </el-table-column>
          </el-table>

          <div class="products-summary">
            <span class="summary-item">
              商品种类：<strong>{{ delivery.products?.length }}</strong>
            </span>
            <span class="summary-item">
              商品总数：<strong>{{ getTotalQuantity() }}</strong>
            </span>
            <span class="summary-item">
              总金额：<strong class="total-amount">￥{{ getTotalAmount() }}</strong>
            </span>
          </div>
        </div>

        <!-- 配送记录 -->
        <div class="info-section card">
          <h3 class="section-title">配送记录</h3>
          <el-timeline>
            <el-timeline-item
              v-for="(record, index) in delivery.records"
              :key="index"
              :type="getTimelineItemType(record.type)"
              :timestamp="record.time"
              placement="top"
            >
              <div class="record-content">
                <div class="record-title">{{ record.title }}</div>
                <div class="record-detail" v-if="record.detail">
                  {{ record.detail }}
                </div>
                <div class="record-images" v-if="record.images?.length">
                  <el-image
                    v-for="(image, imgIndex) in record.images"
                    :key="imgIndex"
                    :src="image"
                    :preview-src-list="record.images"
                    fit="cover"
                    class="record-image"
                  />
                </div>
                <div class="record-operator">
                  操作人：{{ record.operator }}
                </div>
              </div>
            </el-timeline-item>
          </el-timeline>
        </div>
      </el-col>

      <!-- 右侧状态区 -->
      <el-col :span="8">
        <!-- 配送进度 -->
        <div class="status-section card">
          <div class="progress-info">
            <div class="progress-header">
              <h3>配送进度</h3>
              <div class="progress-value">{{ getDeliveryProgress() }}%</div>
            </div>
            <el-progress
              :percentage="getDeliveryProgress()"
              :status="getProgressStatus(delivery.status)"
              :stroke-width="15"
            />
            <div class="delivery-stats">
              <div class="stats-item">
                <div class="stats-value">{{ delivery.completedPoints || 0 }}</div>
                <div class="stats-label">已完成</div>
              </div>
              <div class="stats-item">
                <div class="stats-value">{{ delivery.pendingPoints || 0 }}</div>
                <div class="stats-label">待配送</div>
              </div>
              <div class="stats-item">
                <div class="stats-value">{{ delivery.totalDistance || 0 }}km</div>
                <div class="stats-label">总里程</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 配送点状态 -->
        <div class="status-section card">
          <h3>配送点状态</h3>
          <div class="delivery-points">
            <div
              v-for="(point, index) in delivery.deliveryPoints"
              :key="point.id"
              class="point-item"
              :class="{ active: point.status === 'delivering' }"
            >
              <div class="point-header">
                <div class="point-index">{{ index + 1 }}</div>
                <el-tag
                  :type="getPointStatusType(point.status)"
                  size="small"
                >
                  {{ getPointStatusText(point.status) }}
                </el-tag>
              </div>
              <div class="point-content">
                <div class="point-address">{{ point.address }}</div>
                <div class="point-contact">
                  {{ point.contactName }} {{ point.contactPhone }}
                </div>
                <div class="point-time">
                  <div class="time-item">
                    <span class="label">预计：</span>
                    <span class="value">{{ point.plannedTime }}</span>
                  </div>
                  <div class="time-item" v-if="point.actualTime">
                    <span class="label">实际：</span>
                    <span class="value">{{ point.actualTime }}</span>
                  </div>
                </div>
              </div>
              <div class="point-actions" v-if="delivery.status === 'delivering'">
                <template v-if="point.status === 'pending'">
                  <el-button
                    type="primary"
                    size="small"
                    @click="handleStartDelivery(point)"
                  >
                    开始配送
                  </el-button>
                </template>
                <template v-if="point.status === 'delivering'">
                  <el-button
                    type="success"
                    size="small"
                    @click="handleCompletePoint(point)"
                  >
                    完成配送
                  </el-button>
                  <el-button
                    type="danger"
                    size="small"
                    @click="handleReportException(point)"
                  >
                    异常上报
                  </el-button>
                </template>
              </div>
            </div>
          </div>
        </div>

        <!-- 实时位置 -->
        <div class="status-section card">
          <div class="map-header">
            <h3>实时位置</h3>
            <span class="update-time">更新于：{{ delivery.lastLocationTime }}</span>
          </div>
          <div id="locationMap" class="location-map"></div>
        </div>
      </el-col>
    </el-row>

    <!-- 异常上报对话框 -->
    <el-dialog
      v-model="exceptionDialog.visible"
      title="异常情况上报"
      width="500px"
    >
      <el-form
        ref="exceptionFormRef"
        :model="exceptionForm"
        :rules="exceptionRules"
        label-width="100px"
      >
        <el-form-item label="异常类型" prop="type">
          <el-select
            v-model="exceptionForm.type"
            placeholder="请选择异常类型"
            class="full-width"
          >
            <el-option label="无法联系" value="unreachable" />
            <el-option label="地址错误" value="wrong_address" />
            <el-option label="拒收" value="rejected" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="异常说明" prop="description">
          <el-input
            v-model="exceptionForm.description"
            type="textarea"
            :rows="3"
            placeholder="请详细描述异常情况"
          />
        </el-form-item>
        <el-form-item label="现场照片">
          <el-upload
            class="exception-upload"
            action="/api/upload"
            list-type="picture-card"
            :on-success="handleUploadSuccess"
            :before-upload="beforeUpload"
          >
            <el-icon><Plus /></el-icon>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="exceptionDialog.visible = false">取消</el-button>
          <el-button type="primary" @click="handleExceptionSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
import { Picture, Plus } from '@element-plus/icons-vue'
import AMapLoader from '@amap/amap-jsapi-loader'

const route = useRoute()
const router = useRouter()

// 配送单数据
const delivery = reactive({
  id: 1,
  deliveryNumber: 'D20240101001',
  status: 'delivering',
  createTime: '2024-01-01 09:00:00',
  startTime: '2024-01-01 09:30:00',
  endTime: null,
  driver: {
    name: '张三',
    phone: '13800138000'
  },
  vehicleNumber: '京A12345',
  products: [
    {
      name: '新鲜生菜',
      code: 'VEG001',
      image: '',
      unitPrice: 5.00,
      quantity: 100,
      unit: 'kg',
      totalPrice: 500.00
    }
  ],
  deliveryPoints: [
    {
      id: 1,
      address: '北京市朝阳区xx路xx号',
      contactName: '李四',
      contactPhone: '13800138001',
      plannedTime: '10:00',
      actualTime: '10:05',
      status: 'completed'
    },
    {
      id: 2,
      address: '北京市海淀区xx路xx号',
      contactName: '王五',
      contactPhone: '13800138002',
      plannedTime: '11:00',
      status: 'delivering'
    }
  ],
  records: [
    {
      type: 'start',
      title: '开始配送',
      time: '2024-01-01 09:30:00',
      operator: '张三'
    },
    {
      type: 'point',
      title: '完成配送点1',
      detail: '配送完成，客户已签收',
      images: [],
      time: '2024-01-01 10:05:00',
      operator: '张三'
    }
  ],
  completedPoints: 1,
  pendingPoints: 1,
  totalDistance: 15,
  lastLocationTime: '2024-01-01 10:30:00'
})

// 地图实例
let map: any = null
let marker: any = null
let locationTimer: any = null

// 异常上报对话框
const exceptionDialog = reactive({
  visible: false,
  point: null
})

const exceptionFormRef = ref<FormInstance>()
const exceptionForm = reactive({
  type: '',
  description: '',
  images: []
})

const exceptionRules: FormRules = {
  type: [
    { required: true, message: '请选择异常类型', trigger: 'change' }
  ],
  description: [
    { required: true, message: '请输入异常说明', trigger: 'blur' }
  ]
}

// 初始化地图
const initMap = async () => {
  try {
    const AMap = await AMapLoader.load({
      key: 'your-amap-key',
      version: '2.0'
    })
    
    map = new AMap.Map('locationMap', {
      zoom: 13,
      center: [116.397428, 39.90923]
    })

    // 添加车辆标记
    marker = new AMap.Marker({
      position: [116.397428, 39.90923],
      icon: 'path/to/vehicle-icon.png',
      offset: new AMap.Pixel(-15, -15)
    })
    map.add(marker)

    // 开始定时更新位置
    startLocationUpdate()
  } catch (error) {
    console.error('地图加载失败:', error)
    ElMessage.error('地图加载失败')
  }
}

// 开始定时更新位置
const startLocationUpdate = () => {
  locationTimer = setInterval(() => {
    // TODO: 调用API获取最新位置
    updateLocation({
      longitude: 116.397428,
      latitude: 39.90923,
      time: new Date().toLocaleString()
    })
  }, 10000)
}

// 更新位置信息
const updateLocation = (location: any) => {
  if (marker) {
    marker.setPosition([location.longitude, location.latitude])
    delivery.lastLocationTime = location.time
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

// 获取配送点状态类型
const getPointStatusType = (status: string) => {
  switch (status) {
    case 'pending':
      return 'info'
    case 'delivering':
      return 'warning'
    case 'completed':
      return 'success'
    case 'exception':
      return 'danger'
    default:
      return 'info'
  }
}

// 获取配送点状态文本
const getPointStatusText = (status: string) => {
  switch (status) {
    case 'pending':
      return '待配送'
    case 'delivering':
      return '配送中'
    case 'completed':
      return '已完成'
    case 'exception':
      return '异常'
    default:
      return '未知'
  }
}

// 获取时间线项目类型
const getTimelineItemType = (type: string) => {
  switch (type) {
    case 'start':
      return 'primary'
    case 'point':
      return 'success'
    case 'exception':
      return 'danger'
    default:
      return ''
  }
}

// 获取配送进度
const getDeliveryProgress = () => {
  const total = delivery.deliveryPoints.length
  if (!total) return 0
  return Math.round((delivery.completedPoints / total) * 100)
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

// 获取商品总数
const getTotalQuantity = () => {
  return delivery.products.reduce((sum, item) => sum + (item.quantity || 0), 0)
}

// 获取总金额
const getTotalAmount = () => {
  return delivery.products.reduce((sum, item) => sum + (item.totalPrice || 0), 0).toFixed(2)
}

// 开始配送点
const handleStartDelivery = async (point: any) => {
  try {
    // TODO: 调用API开始配送
    ElMessage.success('开始配送')
    point.status = 'delivering'
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败')
  }
}

// 完成配送点
const handleCompletePoint = async (point: any) => {
  try {
    // TODO: 调用API完成配送
    ElMessage.success('配送完成')
    point.status = 'completed'
    delivery.completedPoints++
    delivery.pendingPoints--
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败')
  }
}

// 异常上报
const handleReportException = (point: any) => {
  exceptionDialog.point = point
  exceptionDialog.visible = true
}

// 处理异常提交
const handleExceptionSubmit = async () => {
  if (!exceptionFormRef.value) return
  
  try {
    await exceptionFormRef.value.validate()
    // TODO: 调用API提交异常
    ElMessage.success('异常上报成功')
    exceptionDialog.visible = false
    if (exceptionDialog.point) {
      exceptionDialog.point.status = 'exception'
    }
  } catch (error) {
    console.error('提交失败:', error)
    ElMessage.error('提交失败')
  }
}

// 图片上传成功
const handleUploadSuccess = (response: any) => {
  exceptionForm.images.push(response.url)
}

// 图片上传前检查
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

// 完成配送
const handleComplete = async () => {
  try {
    // TODO: 调用API完成配送
    ElMessage.success('配送已完成')
    delivery.status = 'completed'
    delivery.endTime = new Date().toLocaleString()
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败')
  }
}

// 编辑配送单
const handleEdit = () => {
  router.push(`/delivery/create?id=${delivery.id}`)
}

// 返回列表
const handleBack = () => {
  router.back()
}

onMounted(() => {
  initMap()
})

onUnmounted(() => {
  if (locationTimer) {
    clearInterval(locationTimer)
  }
})
</script>

<style lang="scss" scoped>
.delivery-detail {
  .page-header {
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

        .status-tag {
          font-size: 14px;
        }
      }

      .header-actions {
        display: flex;
        gap: $spacing-base;
      }
    }
  }

  .detail-container {
    .info-section {
      margin-bottom: $spacing-base;

      .section-title {
        margin: 0 0 $spacing-large;
        font-size: 16px;
        font-weight: 600;
      }
    }

    .status-section {
      margin-bottom: $spacing-base;

      h3 {
        margin: 0 0 $spacing-base;
        font-size: 16px;
        font-weight: 600;
      }
    }
  }

  .driver-info {
    display: flex;
    align-items: center;
    gap: $spacing-base;
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

  .record-content {
    .record-title {
      font-weight: 500;
      margin-bottom: 4px;
    }

    .record-detail {
      color: $text-regular;
      margin-bottom: 8px;
    }

    .record-images {
      display: flex;
      gap: $spacing-base;
      margin-bottom: 8px;

      .record-image {
        width: 80px;
        height: 80px;
        border-radius: $border-radius-small;
      }
    }

    .record-operator {
      font-size: 12px;
      color: $text-secondary;
    }
  }

  .progress-info {
    .progress-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: $spacing-base;

      h3 {
        margin: 0;
      }

      .progress-value {
        font-size: 24px;
        font-weight: 600;
        color: $primary-color;
      }
    }

    .delivery-stats {
      margin-top: $spacing-base;
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: $spacing-base;

      .stats-item {
        text-align: center;
        padding: $spacing-base;
        background-color: $background-color-light;
        border-radius: $border-radius-base;

        .stats-value {
          font-size: 20px;
          font-weight: 600;
          color: $text-primary;
          margin-bottom: 4px;
        }

        .stats-label {
          font-size: 12px;
          color: $text-secondary;
        }
      }
    }
  }

  .delivery-points {
    .point-item {
      padding: $spacing-base;
      border: 1px solid $border-color-base;
      border-radius: $border-radius-base;
      margin-bottom: $spacing-base;
      transition: $transition-base;

      &:last-child {
        margin-bottom: 0;
      }

      &.active {
        border-color: $primary-color;
        background-color: rgba($primary-color, 0.05);
      }

      .point-header {
        display: flex;
        align-items: center;
        gap: $spacing-base;
        margin-bottom: $spacing-base;

        .point-index {
          width: 24px;
          height: 24px;
          border-radius: 50%;
          background-color: $background-color-light;
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: 500;
        }
      }

      .point-content {
        .point-address {
          font-weight: 500;
          margin-bottom: 4px;
        }

        .point-contact {
          font-size: 13px;
          color: $text-regular;
          margin-bottom: 8px;
        }

        .point-time {
          font-size: 12px;

          .time-item {
            margin-bottom: 2px;

            &:last-child {
              margin-bottom: 0;
            }

            .label {
              color: $text-secondary;
            }
          }
        }
      }

      .point-actions {
        margin-top: $spacing-base;
        display: flex;
        gap: $spacing-base;
      }
    }
  }

  .map-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: $spacing-base;

    h3 {
      margin: 0;
    }

    .update-time {
      font-size: 12px;
      color: $text-secondary;
    }
  }

  .location-map {
    height: 300px;
    border-radius: $border-radius-base;
    overflow: hidden;
  }
}

.exception-upload {
  :deep(.el-upload--picture-card) {
    width: 100px;
    height: 100px;
    line-height: 100px;
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