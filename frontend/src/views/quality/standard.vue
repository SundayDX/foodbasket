<template>
  <div class="quality-standard">
    <!-- 页面头部 -->
    <div class="page-header card">
      <div class="header-content">
        <h2>质量检查标准管理</h2>
        <div class="header-actions">
          <el-button type="primary" @click="handleCreate">
            <el-icon><Plus /></el-icon>
            新建标准
          </el-button>
        </div>
      </div>
    </div>

    <el-row :gutter="20">
      <!-- 左侧分类树 -->
      <el-col :span="6">
        <div class="category-tree card">
          <div class="tree-header">
            <h3>商品分类</h3>
            <el-input
              v-model="categoryKeyword"
              placeholder="搜索分类"
              clearable
              @input="filterCategory"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </div>
          <div class="tree-content">
            <el-tree
              ref="treeRef"
              :data="categoryTree"
              :props="defaultProps"
              :filter-node-method="filterNode"
              node-key="id"
              highlight-current
              @node-click="handleNodeClick"
            />
          </div>
        </div>
      </el-col>

      <!-- 右侧标准列表 -->
      <el-col :span="18">
        <div class="standard-list card">
          <el-table
            v-loading="loading"
            :data="standardList"
            border
            style="width: 100%"
          >
            <el-table-column prop="standardCode" label="标准编号" width="180" />
            <el-table-column prop="standardName" label="标准名称" min-width="200" />
            <el-table-column label="适用范围" width="150">
              <template #default="{ row }">
                <el-tag size="small">{{ row.category }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="检查项目" min-width="250">
              <template #default="{ row }">
                <div class="check-items">
                  <el-tag
                    v-for="item in row.items"
                    :key="item.name"
                    size="small"
                    :type="getItemTypeTag(item.type)"
                    class="check-item"
                  >
                    {{ item.name }}
                  </el-tag>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="version" label="版本" width="100" />
            <el-table-column label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ getStatusText(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="更新信息" width="180">
              <template #default="{ row }">
                <div class="update-info">
                  <div>{{ row.updater }}</div>
                  <div class="update-time">{{ row.updateTime }}</div>
                </div>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right">
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
                  @click="handleVersion(row)"
                >
                  版本
                </el-button>
                <el-button
                  type="danger"
                  link
                  @click="handleDelete(row)"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-col>
    </el-row>

    <!-- 标准编辑对话框 -->
    <el-dialog
      v-model="standardDialog.visible"
      :title="standardDialog.type === 'create' ? '新建质量标准' : '编辑质量标准'"
      width="800px"
      destroy-on-close
    >
      <el-form
        ref="standardFormRef"
        :model="standardForm"
        :rules="standardRules"
        label-width="100px"
      >
        <el-form-item label="标准名称" prop="standardName">
          <el-input
            v-model="standardForm.standardName"
            placeholder="请输入标准名称"
          />
        </el-form-item>
        <el-form-item label="适用范围" prop="category">
          <el-cascader
            v-model="standardForm.category"
            :options="categoryOptions"
            :props="{ checkStrictly: true }"
            clearable
            placeholder="请选择适用范围"
            class="full-width"
          />
        </el-form-item>

        <!-- 检查项目 -->
        <div class="check-items-form">
          <div class="items-header">
            <h4>检查项目</h4>
            <el-button type="primary" link @click="handleAddItem">
              <el-icon><Plus /></el-icon>
              添加项目
            </el-button>
          </div>
          <div
            v-for="(item, index) in standardForm.items"
            :key="index"
            class="item-form"
          >
            <el-row :gutter="20">
              <el-col :span="8">
                <el-form-item
                  :prop="'items.' + index + '.name'"
                  :rules="{ required: true, message: '请输入项目名称', trigger: 'blur' }"
                >
                  <el-input
                    v-model="item.name"
                    placeholder="项目名称"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="6">
                <el-form-item
                  :prop="'items.' + index + '.type'"
                  :rules="{ required: true, message: '请选择项目类型', trigger: 'change' }"
                >
                  <el-select
                    v-model="item.type"
                    placeholder="项目类型"
                  >
                    <el-option label="必检项" value="required" />
                    <el-option label="选检项" value="optional" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item
                  :prop="'items.' + index + '.standard'"
                  :rules="{ required: true, message: '请输入检查标准', trigger: 'blur' }"
                >
                  <el-input
                    v-model="item.standard"
                    placeholder="检查标准"
                  />
                </el-form-item>
              </el-col>
              <el-col :span="2">
                <el-button
                  type="danger"
                  circle
                  plain
                  @click="handleRemoveItem(index)"
                >
                  <el-icon><Delete /></el-icon>
                </el-button>
              </el-col>
            </el-row>
            <el-form-item
              :prop="'items.' + index + '.description'"
              :rules="{ required: true, message: '请输入检查说明', trigger: 'blur' }"
            >
              <el-input
                v-model="item.description"
                type="textarea"
                :rows="2"
                placeholder="检查说明"
              />
            </el-form-item>
          </div>
        </div>

        <el-form-item label="备注" prop="remark">
          <el-input
            v-model="standardForm.remark"
            type="textarea"
            :rows="3"
            placeholder="请输入备注信息"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="standardDialog.visible = false">取消</el-button>
          <el-button type="primary" @click="handleStandardSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 版本历史对话框 -->
    <el-dialog
      v-model="versionDialog.visible"
      title="版本历史"
      width="700px"
    >
      <el-timeline>
        <el-timeline-item
          v-for="(version, index) in versionDialog.history"
          :key="index"
          :timestamp="version.createTime"
          placement="top"
        >
          <div class="version-item">
            <div class="version-header">
              <span class="version-number">v{{ version.version }}</span>
              <el-tag
                size="small"
                :type="version.current ? 'success' : ''"
              >
                {{ version.current ? '当前版本' : '历史版本' }}
              </el-tag>
            </div>
            <div class="version-content">
              <div class="update-items">
                <div
                  v-for="(item, itemIndex) in version.updateItems"
                  :key="itemIndex"
                  class="update-item"
                >
                  <el-tag
                    size="small"
                    :type="getUpdateTypeTag(item.type)"
                  >
                    {{ getUpdateTypeText(item.type) }}
                  </el-tag>
                  <span class="update-detail">{{ item.content }}</span>
                </div>
              </div>
              <div class="version-info">
                <span>更新人：{{ version.updater }}</span>
                <span class="version-remark" v-if="version.remark">
                  备注：{{ version.remark }}
                </span>
              </div>
            </div>
          </div>
        </el-timeline-item>
      </el-timeline>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Search, Plus, Delete
} from '@element-plus/icons-vue'

// 分类树相关
const categoryKeyword = ref('')
const treeRef = ref(null)
const defaultProps = {
  children: 'children',
  label: 'name'
}

const categoryTree = ref([
  {
    id: 1,
    name: '蔬菜',
    children: [
      { id: 4, name: '叶菜类' },
      { id: 5, name: '根茎类' }
    ]
  },
  {
    id: 2,
    name: '水果',
    children: [
      { id: 6, name: '热带水果' }
    ]
  }
])

const categoryOptions = ref([
  {
    value: 1,
    label: '蔬菜',
    children: [
      { value: 4, label: '叶菜类' },
      { value: 5, label: '根茎类' }
    ]
  },
  {
    value: 2,
    label: '水果',
    children: [
      { value: 6, label: '热带水果' }
    ]
  }
])

// 加载状态
const loading = ref(false)

// 标准列表数据
const standardList = ref([
  {
    id: 1,
    standardCode: 'STD20240101001',
    standardName: '叶菜类入库质量标准',
    category: '叶菜类',
    items: [
      { name: '外观', type: 'required' },
      { name: '新鲜度', type: 'required' },
      { name: '包装', type: 'optional' }
    ],
    version: 'v1.0',
    status: 'active',
    updater: '张三',
    updateTime: '2024-01-01 09:00:00'
  }
])

// 标准编辑对话框
const standardDialog = reactive({
  visible: false,
  type: 'create'
})

const standardFormRef = ref<FormInstance>()
const standardForm = reactive({
  standardName: '',
  category: null,
  items: [],
  remark: ''
})

const standardRules: FormRules = {
  standardName: [
    { required: true, message: '请输入标准名称', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择适用范围', trigger: 'change' }
  ]
}

// 版本历史对话框
const versionDialog = reactive({
  visible: false,
  history: [
    {
      version: '1.0',
      current: true,
      createTime: '2024-01-01 09:00:00',
      updater: '张三',
      updateItems: [
        { type: 'add', content: '新增外观检查项' },
        { type: 'add', content: '新增新鲜度检查项' }
      ],
      remark: '初始版本'
    }
  ]
})

// 过滤分类树
const filterNode = (value: string, data: any) => {
  if (!value) return true
  return data.name.includes(value)
}

watch(categoryKeyword, (val) => {
  treeRef.value?.filter(val)
})

// 选择分类
const handleNodeClick = (data: any) => {
  // TODO: 根据分类获取标准列表
}

// 新建标准
const handleCreate = () => {
  standardDialog.type = 'create'
  standardDialog.visible = true
}

// 编辑标准
const handleEdit = (row: any) => {
  standardDialog.type = 'edit'
  // TODO: 填充表单数据
  standardDialog.visible = true
}

// 查看版本历史
const handleVersion = (row: any) => {
  // TODO: 获取版本历史
  versionDialog.visible = true
}

// 删除标准
const handleDelete = (row: any) => {
  ElMessageBox.confirm(
    '确定要删除该质量标准吗？',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      // TODO: 调用API删除标准
      ElMessage.success('删除成功')
    } catch (error) {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

// 添加检查项目
const handleAddItem = () => {
  standardForm.items.push({
    name: '',
    type: '',
    standard: '',
    description: ''
  })
}

// 移除检查项目
const handleRemoveItem = (index: number) => {
  standardForm.items.splice(index, 1)
}

// 提交标准
const handleStandardSubmit = async () => {
  if (!standardFormRef.value) return
  
  try {
    await standardFormRef.value.validate()
    // TODO: 调用API保存标准
    ElMessage.success(standardDialog.type === 'create' ? '创建成功' : '更新成功')
    standardDialog.visible = false
  } catch (error) {
    console.error('提交失败:', error)
    ElMessage.error('提交失败，请检查表单')
  }
}

// 获取检查项目类型标签
const getItemTypeTag = (type: string) => {
  switch (type) {
    case 'required':
      return 'danger'
    case 'optional':
      return ''
    default:
      return ''
  }
}

// 获取状态类型
const getStatusType = (status: string) => {
  switch (status) {
    case 'active':
      return 'success'
    case 'inactive':
      return 'info'
    default:
      return ''
  }
}

// 获取状态文本
const getStatusText = (status: string) => {
  switch (status) {
    case 'active':
      return '启用'
    case 'inactive':
      return '停用'
    default:
      return '未知'
  }
}

// 获取更新类型标签
const getUpdateTypeTag = (type: string) => {
  switch (type) {
    case 'add':
      return 'success'
    case 'modify':
      return 'warning'
    case 'delete':
      return 'danger'
    default:
      return ''
  }
}

// 获取更新类型文本
const getUpdateTypeText = (type: string) => {
  switch (type) {
    case 'add':
      return '新增'
    case 'modify':
      return '修改'
    case 'delete':
      return '删除'
    default:
      return '未知'
  }
}
</script>

<style lang="scss" scoped>
.quality-standard {
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
    }
  }

  .category-tree {
    height: calc(100vh - 180px);

    .tree-header {
      margin-bottom: $spacing-base;

      h3 {
        margin: 0 0 $spacing-base;
        font-size: 16px;
        font-weight: 600;
      }
    }

    .tree-content {
      height: calc(100% - 90px);
      overflow-y: auto;
    }
  }

  .standard-list {
    .check-items {
      display: flex;
      flex-wrap: wrap;
      gap: 4px;

      .check-item {
        margin: 0;
      }
    }

    .update-info {
      font-size: 13px;

      .update-time {
        color: $text-secondary;
        margin-top: 4px;
      }
    }
  }

  .check-items-form {
    margin-bottom: $spacing-base;
    padding: $spacing-base;
    border: 1px solid $border-color-light;
    border-radius: $border-radius-base;

    .items-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: $spacing-base;

      h4 {
        margin: 0;
        font-size: 16px;
        font-weight: 500;
      }
    }

    .item-form {
      margin-bottom: $spacing-base;
      padding: $spacing-base;
      border: 1px dashed $border-color-base;
      border-radius: $border-radius-base;

      &:last-child {
        margin-bottom: 0;
      }
    }
  }

  .version-item {
    .version-header {
      display: flex;
      align-items: center;
      gap: $spacing-base;
      margin-bottom: $spacing-base;

      .version-number {
        font-weight: 500;
      }
    }

    .version-content {
      .update-items {
        margin-bottom: $spacing-base;

        .update-item {
          margin-bottom: 4px;

          &:last-child {
            margin-bottom: 0;
          }

          .update-detail {
            margin-left: $spacing-small;
            color: $text-regular;
          }
        }
      }

      .version-info {
        font-size: 13px;
        color: $text-secondary;

        .version-remark {
          margin-left: $spacing-base;
        }
      }
    }
  }
}

.full-width {
  width: 100%;
}
</style>