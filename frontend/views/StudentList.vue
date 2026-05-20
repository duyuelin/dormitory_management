<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>学生列表</span>
        <el-button type="primary" @click="handleAdd"><el-icon><Plus /></el-icon>添加学生</el-button>
      </div>
    </template>
    <el-table :data="list" v-loading="loading" stripe>
      <el-table-column prop="student_id" label="学号" width="120" />
      <el-table-column prop="name" label="姓名" width="100" />
      <el-table-column prop="gender" label="性别" width="80" />
      <el-table-column prop="college" label="学院" width="150" />
      <el-table-column prop="major" label="专业" width="120" />
      <el-table-column prop="class_name" label="班级" width="100" />
      <el-table-column prop="phone" label="电话" width="120" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="scope">
          <el-tag :type="getStatusType(scope.row.status)" size="small">{{ getStatusText(scope.row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="scope">
          <el-button type="primary" size="small" @click="handleEdit(scope.row)">编辑</el-button>
          <el-button type="danger" size="small" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { getStudentList, deleteStudent } from '../api/student'

const loading = ref(false)
const list = ref([])

const getStatusType = (status) => ({ 0: 'info', 1: 'success', 2: 'warning' }[status] || 'info')
const getStatusText = (status) => ({ 0: '已退宿', 1: '在住', 2: '待入住' }[status] || '未知')

const fetchList = async () => {
  loading.value = true
  try {
    const res = await getStudentList()
    list.value = res.data
  } finally {
    loading.value = false
  }
}

const handleAdd = () => ElMessage.info('请参考完整代码实现添加功能')
const handleEdit = (row) => ElMessage.info('请参考完整代码实现编辑功能')
const handleDelete = async (row) => {
  await ElMessageBox.confirm(`确定要删除学生${row.name}吗？`, '提示', { type: 'warning' })
  await deleteStudent(row.id)
  ElMessage.success('删除成功')
  fetchList()
}

onMounted(() => fetchList())
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>
