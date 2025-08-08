<template>
  <div class="quality-detail">
    <!-- 页面头部 -->
    <div class="page-header card">
      <div class="header-content">
        <div class="header-left">
          <h2>质量检查详情</h2>
          <el-tag
            :type="getStatusType(checkInfo.status)"
            class="status-tag"
          >
            {{ getStatusText(checkInfo.status) }}
          </el-tag>
        </div>
        <div class="header-actions">
          <el-button @click="handleBack">
            返回列表
          </el-button>
          <el-button
            type="primary"
            v-if="checkInfo.status === 'pending'"
            @click="handleEdit"
          >
            编辑检查
          </el-button>
        </div>
      </div>
    </div>

    <el-row :gutter="20">
      <!-- 左侧基本信息 -->
      <el-col :span="16">
        <div class="basic-info card">
          <div class="section-header">
            <h3>基本信息</h3>
          </div>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="检查编号">
              {{ checkInfo.checkCode }}
            </el-descriptions-item>
            <el-descriptions-item label="检查时间">
              {{ checkInfo.checkTime }}
            </el-descriptions-item>
            <el-descriptions-item label="检查人员">
              {{ checkInfo.inspector }}
            </el-descriptions-item>
            <el-descriptions-item label="检查地点">
              {{ checkInfo.location }}
            </el-descriptions-item>
            <el-descriptions-item label="商品名称">
              {{ checkInfo.productName }}
            </el-descriptions-item>
            <el-descriptions-item label="批次号">
              {{ checkInfo.batchNumber }}
            </el-descriptions-item>
            <el-descriptions-item label="供应商">
              {{ checkInfo.supplier }}
            </el-descriptions-item>
            <el-descriptions-item label="检查标准">
              {{ checkInfo.standard }}
            </el-descriptions-item>
          </el-descriptions>
        </div>

        <!-- 检查项目结果 -->
        <div class="check-results card">
          <div class="section-header">
            <h3>检查结果</h3>
            <div class="result-summary">
              <el-tag type="success">合格项：{{ checkInfo.passCount }}</el-tag>
              <el-tag type="danger">不合格项：{{ checkInfo.failCount }}</el-tag>
              <el-tag>待检项：{{ checkInfo.pendingCount }}</el-tag>
            </div>
          </div>
          <el-table
            :data="checkInfo.items"
            border
            style="width: 100%"
          >
            <el-table-column prop="name" label="检查项目" min-width="150" />
            <el-table-column prop="standard" label="检查标准" min-width="200" />
            <el-table-column label="检查结果" width="120">
              <template #default="{ row }">
                <el-tag :type="getResultType(row.result)">
                  {{ getResultText(row.result) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="value" label="实测值" width="120" />
            <el-table-column prop="remark" label="备注" min-width="200" />
          </el-table>
        </div>

        <!-- 处理建议 -->
        <div class="suggestions card">
          <div class="section-header">
            <h3>处理建议</h3>
          </div>
          <div class="suggestion-content">
            <el-alert
              v-if="checkInfo.suggestion"
              :type="getSuggestionType(checkInfo.overallResult)"
              :title="checkInfo.suggestion"
              :description="checkInfo.suggestionDetail"
              show-icon
              :closable="false"
            />
          </div>
        </div>
      </el-col>

      <!-- 右侧照片和历史记录 -->
      <el-col :span="8">
        <!-- 检查照片 -->
        <div class="check-photos card">
          <div class="section-header">
            <h3>检查照片</h3>
            <el-button
              v-if="checkInfo.status === 'pending'"
              type="primary"
              link
              @click="handleUpload"
            >
              <el-icon><Upload /></el-icon>
              上传照片
            </el-button>
          </div>
          <div class="photo-list">
            <el-image
              v-for="(photo, index) in checkInfo.photos"
              :key="index"
              :src="photo.url"
              :preview-src-list="checkInfo.photos.map(p => p.url)"
              fit="cover"
              class="check-photo"
            >
              <template #placeholder>
                <div class="image-placeholder">
                  <el-icon><Picture /></el-icon>
                </div>
              </template>
            </el-image>
          </div>
        </div>

        <!-- 历史记录 -->
        <div class="check-history card">
          <div class="section-header">
            <h3>历史记录</h3>
          </div>
          <el-timeline>
            <el-timeline-item
              v-for="(record, index) in checkInfo.history"
              :key="index"
              :type="getTimelineType(record.type)"
              :timestamp="record.time"
              placement="top"
            >
              <div class="history-item">
                <span class="history-title">{{ record.title }}</span>
                <div class="history-content">{{ record.content }}</div>
                <div class="history-operator">
                  操作人：{{ record.operator }}
                </div>
              </div>
            </el-timeline-item>
          </el-timeline>
        </div>
      </el-col>
    </el-row>

    <!-- 照片上传对话框 -->
    <el-dialog
      v-model="uploadDialog.visible"
      title="上传检查照片"
      width="500px"
    >
      <el-upload
        class="upload-photos"
        action="/api/v1/quality/photos/upload"
        :headers="uploadHeaders"
        list-type="picture-card"
        :limit="5"
        :file-list="uploadDialog.fileList"
        :on-preview="handlePreview"
        :on-remove="handleRemove"
        :on-success="handleUploadSuccess"
        :on-error="handleUploadError"
        :before-upload="beforeUpload"
      >
        <el-icon><Plus /></el-icon>
      </el-upload>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="uploadDialog.visible = false">取消</el-button>
          <el-button type="primary" @click="handleUploadSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 照片预览 -->
    <el-dialog v-model="previewDialog.visible" width="800px">
      <img
        :src="previewDialog.url"
        alt="Preview Image"
        style="width: 100%"
      />
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  Upload, Plus, Picture
} from '@element-plus/icons-vue'

const router = useRouter()

// 检查信息
const checkInfo = reactive({
  checkCode: 'QC20240101001',
  checkTime: '2024-01-01 10:00:00',
  inspector: '张三',
  location: '1号仓库验收区',
  productName: '生菜',
  batchNumber: 'B20240101001',
  supplier: '绿色蔬菜基地',
  standard: '叶菜类入库质量标准v1.0',
  status: 'completed',
  passCount: 8,
  failCount: 2,
  pendingCount: 0,
  items: [
    {
      name: '外观',
      standard: '叶片完整，无破损',
      result: 'pass',
      value: '完好',
      remark: ''
    },
    {
      name: '新鲜度',
      standard: '叶片翠绿，无发黄',
      result: 'fail',
      value: '部分发黄',
      remark: '约20%叶片发黄'
    }
  ],
  overallResult: 'fail',
  suggestion: '建议降级处理',
  suggestionDetail: '由于部分叶片发黄，建议按照二级品处理，进行促销销售。',
  photos: [
    { url: 'https://example.com/photo1.jpg' },
    { url: 'https://example.com/photo2.jpg' }
  ],
  history: [
    {
      type: 'create',
      time: '2024-01-01 10:00:00',
      title: '创建检查',
      content: '创建质量检查任务',
      operator: '张三'
    },
    {
      type: 'update',
      time: '2024-01-01 10:30:00',
      title: '更新检查结果',
      content: '完成质量检查，记录检查结果',
      operator: '张三'
    }
  ]
})

// 上传对话框
const uploadDialog = reactive({
  visible: false,
  fileList: []
})

// 预览对话框
const previewDialog = reactive({
  visible: false,
  url: ''
})

// 上传配置
const uploadHeaders = {
  // TODO: 添加认证token
}

// 返回列表
const handleBack = () => {
  router.push('/quality/check')
}

// 编辑检查
const handleEdit = () => {
  // TODO: 跳转到编辑页面
}

// 上传照片
const handleUpload = () => {
  uploadDialog.visible = true
}

// 预览照片
const handlePreview = (file: any) => {
  previewDialog.url = file.url
  previewDialog.visible = true
}

// 移除照片
const handleRemove = (file: any, fileList: any[]) => {
  uploadDialog.fileList = fileList
}

// 上传成功
const handleUploadSuccess = (response: any, file: any) => {
  ElMessage.success('上传成功')
}

// 上传失败
const handleUploadError = () => {
  ElMessage.error('上传失败')
}

// 上传前验证
const beforeUpload = (file: File) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传图片文件！')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB！')
    return false
  }
  return true
}

// 提交上传
const handleUploadSubmit = () => {
  // TODO: 保存照片关联
  uploadDialog.visible = false
  ElMessage.success('保存成功')
}

// 获取状态类型
const getStatusType = (status: string) => {
  switch (status) {
    case 'pending':
      return 'warning'
    case 'completed':
      return 'success'
    default:
      return 'info'
  }
}

// 获取状态文本
const getStatusText = (status: string) => {
  switch (status) {
    case 'pending':
      return '待完成'
    case 'completed':
      return '已完成'
    default:
      return '未知'
  }
}

// 获取结果类型
const getResultType = (result: string) => {
  switch (result) {
    case 'pass':
      return 'success'
    case 'fail':
      return 'danger'
    default:
      return 'info'
  }
}

// 获取结果文本
const getResultText = (result: string) => {
  switch (result) {
    case 'pass':
      return '合格'
    case 'fail':
      return '不合格'
    default:
      return '待检'
  }
}

// 获取建议类型
const getSuggestionType = (result: string) => {
  switch (result) {
    case 'pass':
      return 'success'
    case 'fail':
      return 'warning'
    default:
      return 'info'
  }
}

// 获取时间线类型
const getTimelineType = (type: string) => {
  switch (type) {
    case 'create':
      return 'primary'
    case 'update':
      return 'success'
    case 'reject':
      return 'danger'
    default:
      return ''
  }
}
</script>

<style lang="scss" scoped>
.quality-detail {
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
    }
  }

  .card {
    margin-bottom: $spacing-base;

    .section-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: $spacing-base;

      h3 {
        margin: 0;
        font-size: 16px;
        font-weight: 600;
      }
    }
  }

  .check-results {
    .result-summary {
      display: flex;
      gap: $spacing-base;
    }
  }

  .check-photos {
    .photo-list {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: $spacing-base;

      .check-photo {
        width: 100%;
        height: 150px;
        border-radius: $border-radius-base;
        overflow: hidden;
        cursor: pointer;

        &:deep(.el-image__inner) {
          transition: transform 0.3s;

          &:hover {
            transform: scale(1.05);
          }
        }
      }

      .image-placeholder {
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: $background-color-base;
        color: $text-secondary;
        font-size: 24px;
      }
    }
  }

  .check-history {
    .history-item {
      .history-title {
        font-weight: 500;
        color: $text-primary;
      }

      .history-content {
        margin: 4px 0;
        color: $text-regular;
      }

      .history-operator {
        font-size: 13px;
        color: $text-secondary;
      }
    }
  }
}

.upload-photos {
  :deep(.el-upload--picture-card) {
    width: 100px;
    height: 100px;
    line-height: 100px;
  }
}
</style>