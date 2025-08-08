<template>
  <div class="category-page">
    <div class="category-container">
      <!-- 左侧分类树 -->
      <div class="category-tree card">
        <div class="tree-header">
          <h3>商品分类</h3>
          <el-button type="primary" @click="handleAddRoot">
            <el-icon><Plus /></el-icon>
            新增根分类
          </el-button>
        </div>
        <div class="tree-content">
          <el-tree
            ref="treeRef"
            :data="categoryTree"
            :props="defaultProps"
            :expand-on-click-node="false"
            node-key="id"
            default-expand-all
            highlight-current
            @node-click="handleNodeClick"
          >
            <template #default="{ node, data }">
              <div class="custom-tree-node">
                <span class="node-label">{{ node.label }}</span>
                <span class="node-actions">
                  <el-button
                    type="primary"
                    link
                    @click.stop="handleAdd(data)"
                  >
                    添加子分类
                  </el-button>
                  <el-button
                    type="primary"
                    link
                    @click.stop="handleEdit(data)"
                  >
                    编辑
                  </el-button>
                  <el-button
                    type="danger"
                    link
                    @click.stop="handleDelete(node, data)"
                  >
                    删除
                  </el-button>
                </span>
              </div>
            </template>
          </el-tree>
        </div>
      </div>

      <!-- 右侧分类详情 -->
      <div class="category-detail card" v-if="currentCategory">
        <h3>分类详情</h3>
        <el-descriptions :column="1" border>
          <el-descriptions-item label="分类名称">
            {{ currentCategory.name }}
          </el-descriptions-item>
          <el-descriptions-item label="分类编码">
            {{ currentCategory.code }}
          </el-descriptions-item>
          <el-descriptions-item label="上级分类">
            {{ currentCategory.parentName || '无' }}
          </el-descriptions-item>
          <el-descriptions-item label="创建时间">
            {{ currentCategory.createTime }}
          </el-descriptions-item>
          <el-descriptions-item label="更新时间">
            {{ currentCategory.updateTime }}
          </el-descriptions-item>
          <el-descriptions-item label="分类描述">
            {{ currentCategory.description || '暂无描述' }}
          </el-descriptions-item>
        </el-descriptions>

        <div class="statistics mt-4">
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="stat-card">
                <div class="stat-title">商品数量</div>
                <div class="stat-value">{{ currentCategory.productCount || 0 }}</div>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="stat-card">
                <div class="stat-title">子分类数量</div>
                <div class="stat-value">{{ currentCategory.childrenCount || 0 }}</div>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="stat-card">
                <div class="stat-title">商品总库存</div>
                <div class="stat-value">{{ currentCategory.totalStock || 0 }}</div>
              </div>
            </el-col>
          </el-row>
        </div>
      </div>
    </div>

    <!-- 分类编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '新增分类' : '编辑分类'"
      width="500px"
    >
      <el-form
        ref="categoryFormRef"
        :model="categoryForm"
        :rules="categoryRules"
        label-width="100px"
      >
        <el-form-item label="分类名称" prop="name">
          <el-input v-model="categoryForm.name" placeholder="请输入分类名称" />
        </el-form-item>
        <el-form-item label="分类编码" prop="code">
          <el-input v-model="categoryForm.code" placeholder="请输入分类编码" />
        </el-form-item>
        <el-form-item label="上级分类" prop="parentId">
          <el-cascader
            v-model="categoryForm.parentId"
            :options="categoryOptions"
            :props="cascaderProps"
            clearable
            placeholder="请选择上级分类"
            class="full-width"
          />
        </el-form-item>
        <el-form-item label="分类描述" prop="description">
          <el-input
            v-model="categoryForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入分类描述"
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
import { Plus } from '@element-plus/icons-vue'

// 分类树配置
const defaultProps = {
  children: 'children',
  label: 'name'
}

const cascaderProps = {
  value: 'id',
  label: 'name',
  children: 'children',
  checkStrictly: true,
  emitPath: false
}

// 分类树数据
const categoryTree = ref([
  {
    id: 1,
    name: '蔬菜',
    code: 'VEG',
    children: [
      {
        id: 4,
        name: '叶菜类',
        code: 'VEG-LEAF'
      },
      {
        id: 5,
        name: '根茎类',
        code: 'VEG-ROOT'
      }
    ]
  },
  {
    id: 2,
    name: '水果',
    code: 'FRUIT',
    children: [
      {
        id: 6,
        name: '热带水果',
        code: 'FRUIT-TROP'
      }
    ]
  },
  {
    id: 3,
    name: '肉类',
    code: 'MEAT'
  }
])

// 当前选中的分类
const currentCategory = ref(null)
const treeRef = ref(null)

// 对话框相关
const dialogVisible = ref(false)
const dialogType = ref<'add' | 'edit'>('add')
const categoryFormRef = ref<FormInstance>()

// 分类表单
const categoryForm = reactive({
  name: '',
  code: '',
  parentId: null,
  description: ''
})

// 表单验证规则
const categoryRules: FormRules = {
  name: [
    { required: true, message: '请输入分类名称', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入分类编码', trigger: 'blur' },
    { pattern: /^[A-Z-]+$/, message: '只能包含大写字母和连字符', trigger: 'blur' }
  ]
}

// 处理节点点击
const handleNodeClick = (data: any) => {
  currentCategory.value = {
    ...data,
    createTime: '2024-01-01 12:00:00',
    updateTime: '2024-01-01 12:00:00',
    productCount: 10,
    childrenCount: data.children?.length || 0,
    totalStock: 100
  }
}

// 新增根分类
const handleAddRoot = () => {
  dialogType.value = 'add'
  Object.keys(categoryForm).forEach(key => {
    categoryForm[key] = ''
  })
  categoryForm.parentId = null
  dialogVisible.value = true
}

// 新增子分类
const handleAdd = (data: any) => {
  dialogType.value = 'add'
  Object.keys(categoryForm).forEach(key => {
    categoryForm[key] = ''
  })
  categoryForm.parentId = data.id
  dialogVisible.value = true
}

// 编辑分类
const handleEdit = (data: any) => {
  dialogType.value = 'edit'
  Object.keys(categoryForm).forEach(key => {
    categoryForm[key] = data[key]
  })
  dialogVisible.value = true
}

// 删除分类
const handleDelete = (node: any, data: any) => {
  ElMessageBox.confirm(
    '确定要删除该分类吗？如果存在子分类或关联商品将无法删除。',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(async () => {
    try {
      // TODO: 调用API删除分类
      ElMessage.success('删除成功')
      if (currentCategory.value?.id === data.id) {
        currentCategory.value = null
      }
    } catch (error) {
      console.error('删除分类失败:', error)
      ElMessage.error('删除失败')
    }
  }).catch(() => {})
}

// 提交表单
const handleSubmit = async () => {
  if (!categoryFormRef.value) return
  
  try {
    await categoryFormRef.value.validate()
    // TODO: 调用API保存分类
    ElMessage.success(dialogType.value === 'add' ? '添加成功' : '更新成功')
    dialogVisible.value = false
    // TODO: 刷新分类树
  } catch (error) {
    console.error('保存分类失败:', error)
    ElMessage.error('保存失败，请检查表单')
  }
}

// 分类选项（用于级联选择器）
const categoryOptions = ref([])

// 获取分类树
const getCategoryTree = async () => {
  try {
    // TODO: 调用API获取分类树
    categoryOptions.value = categoryTree.value
  } catch (error) {
    console.error('获取分类树失败:', error)
    ElMessage.error('获取分类树失败')
  }
}

onMounted(() => {
  getCategoryTree()
})
</script>

<style lang="scss" scoped>
.category-page {
  height: 100%;
}

.category-container {
  display: grid;
  grid-template-columns: 360px 1fr;
  gap: $spacing-base;
  height: 100%;
}

.category-tree {
  .tree-header {
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

  .tree-content {
    height: calc(100% - 40px);
    overflow-y: auto;
  }

  .custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-right: $spacing-base;
    font-size: 14px;

    .node-label {
      font-size: 14px;
    }

    .node-actions {
      display: none;
    }
  }

  :deep(.el-tree-node__content:hover) {
    .node-actions {
      display: block;
    }
  }
}

.category-detail {
  h3 {
    margin: 0 0 $spacing-large;
    font-size: 16px;
    font-weight: 600;
  }

  .statistics {
    .stat-card {
      background-color: $background-color-light;
      padding: $spacing-base;
      border-radius: $border-radius-base;
      text-align: center;

      .stat-title {
        color: $text-regular;
        font-size: 14px;
        margin-bottom: $spacing-small;
      }

      .stat-value {
        color: $text-primary;
        font-size: 24px;
        font-weight: 600;
      }
    }
  }
}

.full-width {
  width: 100%;
}
</style>