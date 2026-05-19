<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>宿舍楼列表</span>
        <el-button type="primary" @click="handleAdd"><el-icon><Plus /></el-icon>添加宿舍楼</el-button>
      </div>
    </template>
    <el-table :data="list" v-loading="loading" stripe>
      <el-table-column prop="name" label="楼名" width="120" />
      <el-table-column prop="code" label="楼号" width="100" />
      <el-table-column prop="floors" label="楼层数" width="80" />
      <el-table-column prop="total_beds" label="总床位" width="80" />
      <el-table-column prop="available_beds" label="空余床位" width="100">
        <template #default="scope">
          <el-tag :type="scope.row.available_beds > 0 ? 'success' : 'danger'">{{ scope.row.available_beds }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="manager" label="宿管" width="100" />
      <el-table-column prop="manager_phone" label="宿管电话" width="120" />
      <el-table-column prop="gender" label="类型" width="80">
        <template #default="scope"><el-tag size="small">{{ scope.row.gender }}</el-tag></template>
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
import { getBuildingList, deleteBuilding } from '../api/building'

const loading = ref(false)
const list = ref([])

const fetchList = async () => {
  loading.value = true
  try {
    const res = await getBuildingList()
    list.value = res.data
  } finally {
    loading.value = false
  }
}

const handleAdd = () => ElMessage.info('请参考完整代码实现添加功能')
const handleEdit = (row) => ElMessage.info('请参考完整代码实现编辑功能')
const handleDelete = async (row) => {
  await ElMessageBox.confirm(`确定要删除${row.name}吗？`, '提示', { type: 'warning' })
  await deleteBuilding(row.id)
  ElMessage.success('删除成功')
  fetchList()
}

onMounted(() => fetchList())
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>
