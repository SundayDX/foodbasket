<template>
  <div class="damage-detail">
    <!-- 页面头部 -->
    <div class="page-header card">
      <div class="header-content">
        <div class="header-left">
          <h2>报损单详情</h2>
          <el-tag
            :type="getStatusTagType(damage.status)"
            class="status-tag"
          >
            {{ getStatusText(damage.status) }}
          </el-tag>
        </div>
        <div class="header-actions">
          <el-button @click="handleBack">返回</el-button>
          <el-button
            v-if="damage.status === 'pending'"
            type="primary"
            @click="handleEdit"
          >
            编辑
          </el-button>
          <el-button
            v-if="damage.status === 'pending'"
            type="success"
            @click="handleApprove"
          >
            审核
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
            <el-descriptions-item label="报损单号">
              {{ damage.damageNumber }}
            </el-descriptions-item>
            <el-descriptions-item label="报损类型">
              <el-tag :type="getDamageTypeTag(damage.type)">
                {{ getDamageTypeText(damage.type) }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="申请人">
              {{ damage.reporter }}
            </el-descriptions-item>
            <el-descriptions-item label="申请时间">
              {{ damage.reportTime }}
            </el-descriptions-item>
            <el-descriptions-item label="审核人" v-if="damage.status !== 'pending'">
              {{ damage.approver }}
            </el-descriptions-item>
            <el-descriptions-item label="审核时间" v-if="damage.status !== 'pending'">
              {{ damage.approveTime }}
            </el-descriptions-item>
          </el-descriptions>
        </div>

        <!-- 商品信息 -->
        <div class="info-section card">
          <h3 class="section-title">商品信息</h3>
          <div class="product-info">
            <div class="product-header">
              <el-image
                :src="damage.product?.image"
                :preview-src-list="[damage.product?.image]"
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
                <div class="product-name">{{ damage.product?.name }}</div>
                <div class="product-code">{{ damage.product?.code }}</div>
                <div class="product-category">
                  分类：{{ damage.product?.category }}
                </div>
              </div>
            </div>
            <el-divider />
            <div class="damage-detail">
              <div class="detail-item">
                <span class="label">批次号：</span>
                <span class="value">{{ damage.batchNumber }}</span>
              </div>
              <div class="detail-item">
                <span class="label">报损数量：</span>
                <span class="value">{{ damage.quantity }} {{ damage.product?.unit }}</span>
              </div>
              <div class="detail-item">
                <span class="label">报损金额：</span>
                <span class="value amount">￥{{ damage.amount }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 报损原因 -->
        <div class="info-section card">
          <h3 class="section-title">报损原因</h3>
          <div class="reason-content">
            {{ damage.reason }}
          </div>
          <div class="damage-images">
            <el-image
              v-for="(image, index) in damage.images"
              :key="index"
              :src="image"
              :preview-src-list="damage.images"
              fit="cover"
              class="damage-image"
            />
          </div>
        </div>

        <!-- 处理记录 -->
        <div class="info-section card">
          <h3 class="section-title">处理记录</h3>
          <el-timeline>
            <el-timeline-item
              v-for="(record, index) in damage.records"
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
        <!-- 审核信息 -->
        <div class="status-section card" v-if="damage.status !== 'pending'">
          <h3>审核信息</h3>
          <div class="approve-info">
            <div class="info-item">
              <div class="label">审核结果</div>
              <div class="value">
                <el-tag
                  :type="damage.status === 'approved' ? 'success' : 'danger'"
                >
                  {{ damage.status === 'approved' ? '通过' : '拒绝' }}
                </el-tag>
              </div>
            </div>
            <div class="info-item">
              <div class="label">处理方式</div>
              <div class="value">{{ getHandlingMethodText(damage.handlingMethod) }}</div>
            </div>
            <div class="info-item">
              <div class="label">审核意见</div>
              <div class="value">{{ damage.approveComment }}</div>
            </div>
          </div>
        </div>

        <!-- 相关信息 -->
        <div class="status-section card">
          <h3>相关信息</h3>
          <div class="related-info">
            <div class="info-item">
              <div class="label">供应商</div>
              <div class="value">{{ damage.product?.supplier }}</div>
            </div>
            <div class="info-item">
              <div class="label">采购价</div>
              <div class="value">￥{{ damage.product?.purchasePrice }}</div>
            </div>
            <div class="info-item">
              <div class="label">当前库存</div>
              <div class="value">{{ damage.product?.stock }} {{ damage.product?.unit }}</div>
            </div>
            <div class="info-item">
              <div class="label">近30天报损</div>
              <div class="value">{{ damage.product?.damageCount || 0 }} 次</div>
            </div>
          </div>
        </div>

        <!-- 报损统计 -->
        <div class="status-section card">
          <div class="stat-header">
            <h3>报损统计</h3>
            <span class="stat-period">近30天</span>
          </div>
          <div class="stat-content">
            <div class="stat-chart" id="damageChart"></div>
            <div class="stat-summary">
              <div class="summary-item">
                <div class="item-value">{{ statistics.totalCount }}</div>
                <div class="item-label">报损次数</div>
              </div>
              <div class="summary-item">
                <div class="item-value">{{ statistics.totalQuantity }}</div>
                <div class="item-label">报损数量</div>
              </div>
              <div class="summary-item">
                <div class="item-value amount">￥{{ statistics.totalAmount }}</div>
                <div class="item-label">报损金额</div>
              </div>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>

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
import { useRoute, useRouter } from 'vue-router'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
import { Picture } from '@element-plus/icons-vue'
import * as echarts from 'echarts'

const route = useRoute()
const router = useRouter()

// 报损单数据
const damage = reactive({
  id: 1,
  damageNumber: 'D20240101001',
  type: 'natural',
  status: 'pending',
  reporter: '张三',
  reportTime: '2024-01-01 09:00:00',
  approver: '',
  approveTime: '',
  product: {
    name: '新鲜生菜',
    code: 'VEG001',
    category: '蔬菜',
    unit: 'kg',
    image: '',
    supplier: '供应商A',
    purchasePrice: 3.00,
    stock: 100,
    damageCount: 2
  },
  batchNumber: 'B20240101001',
  quantity: 10,
  amount: 50.00,
  reason: '由于运输过程中温度控制不当，部分商品出现腐烂。',
  images: [],
  handlingMethod: '',
  approveComment: '',
  records: [
    {
      type: 'create',
      title: '创建报损单',
      time: '2024-01-01 09:00:00',
      operator: '张三'
    }
  ]
})

// 统计数据
const statistics = reactive({
  totalCount: 5,
  totalQuantity: '50kg',
  totalAmount: '250.00'
})

// 审核对话框
const approveDialog = reactive({
  visible: false
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

// 初始化图表
const initChart = () => {
  const chartDom = document.getElementById('damageChart')
  if (!chartDom) return
  
  const myChart = echarts.init(chartDom)
  const option = {
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: ['1月1日', '1月2日', '1月3日', '1月4日', '1月5日']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        data: [5, 8, 3, 9, 6],
        type: 'line',
        smooth: true,
        areaStyle: {}
      }
    ]
  }
  myChart.setOption(option)
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

// 获取处理方式文本
const getHandlingMethodText = (method: string) => {
  switch (method) {
    case 'destroy':
      return '销毁'
    case 'discount':
      return '降价销售'
    case 'other':
      return '其他'
    default:
      return '未知'
  }
}

// 获取时间线项目类型
const getTimelineItemType = (type: string) => {
  switch (type) {
    case 'create':
      return 'primary'
    case 'approve':
      return 'success'
    case 'reject':
      return 'danger'
    default:
      return ''
  }
}

// 编辑
const handleEdit = () => {
  router.push(`/damage/create?id=${damage.id}`)
}

// 审核
const handleApprove = () => {
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
    // 更新状态
    damage.status = approveForm.result
    damage.handlingMethod = approveForm.handlingMethod
    damage.approveComment = approveForm.comment
    damage.approver = '李四'
    damage.approveTime = new Date().toLocaleString()
    // 添加记录
    damage.records.push({
      type: approveForm.result === 'approved' ? 'approve' : 'reject',
      title: approveForm.result === 'approved' ? '审核通过' : '审核拒绝',
      detail: approveForm.comment,
      time: damage.approveTime,
      operator: damage.approver
    })
  } catch (error) {
    console.error('审核失败:', error)
    ElMessage.error('审核失败')
  }
}

// 返回列表
const handleBack = () => {
  router.back()
}

onMounted(() => {
  initChart()
})
</script>

<style lang="scss" scoped>
.damage-detail {
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

  .product-info {
    .product-header {
      display: flex;
      gap: $spacing-base;

      .product-image {
        width: 80px;
        height: 80px;
        border-radius: $border-radius-base;
      }

      .product-detail {
        .product-name {
          font-size: 16px;
          font-weight: 500;
          margin-bottom: 4px;
        }

        .product-code {
          color: $text-secondary;
          margin-bottom: 4px;
        }

        .product-category {
          color: $text-regular;
        }
      }
    }

    .damage-detail {
      .detail-item {
        margin-bottom: 8px;

        &:last-child {
          margin-bottom: 0;
        }

        .label {
          color: $text-secondary;
          margin-right: $spacing-base;
        }

        .value {
          color: $text-primary;
          font-weight: 500;

          &.amount {
            color: $danger-color;
          }
        }
      }
    }
  }

  .reason-content {
    color: $text-regular;
    margin-bottom: $spacing-base;
    line-height: 1.6;
  }

  .damage-images {
    display: flex;
    gap: $spacing-base;
    flex-wrap: wrap;

    .damage-image {
      width: 120px;
      height: 120px;
      border-radius: $border-radius-base;
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

    .record-operator {
      font-size: 12px;
      color: $text-secondary;
    }
  }

  .approve-info,
  .related-info {
    .info-item {
      margin-bottom: $spacing-base;

      &:last-child {
        margin-bottom: 0;
      }

      .label {
        color: $text-secondary;
        margin-bottom: 4px;
      }

      .value {
        color: $text-primary;
      }
    }
  }

  .stat-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: $spacing-base;

    h3 {
      margin: 0;
    }

    .stat-period {
      font-size: 12px;
      color: $text-secondary;
    }
  }

  .stat-content {
    .stat-chart {
      height: 200px;
      margin-bottom: $spacing-base;
    }

    .stat-summary {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: $spacing-base;

      .summary-item {
        text-align: center;

        .item-value {
          font-size: 20px;
          font-weight: 600;
          color: $text-primary;
          margin-bottom: 4px;

          &.amount {
            color: $danger-color;
          }
        }

        .item-label {
          font-size: 12px;
          color: $text-secondary;
        }
      }
    }
  }
}

.full-width {
  width: 100%;
}

.image-placeholder {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: $background-color-light;
  border: 1px dashed $border-color-base;
  border-radius: $border-radius-base;
  
  .el-icon {
    font-size: 24px;
    color: $text-secondary;
  }
}
</style>