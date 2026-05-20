<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>房间列表</span>
        <el-button type="primary" @click="handleAdd"><el-icon><Plus /></el-icon>添加房间</el-button>
      </div>
    </template>
    <el-table :data="list" v-loading="loading" stripe>
      <el-table-column prop="building_name" label="所属楼栋" width="120" />
      <el-table-column prop="room_number" label="房间号" width="100" />
      <el-table-column prop="floor" label="楼层" width="80" />
      <el-table-column prop="room_type" label="房间类型" width="100" />
      <el-table-column prop="total_beds" label="总床位" width="80" />
      <el-table-column prop="available_beds" label="空余床位" width="100">
        <template #default="scope">
          <el-tag :type="scope.row.available_beds > 0 ? 'success' : 'danger'">{{ scope.row.available_beds }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="price" label="住宿费/学期" width="120">
        <template #default="scope">¥{{ scope.row.price }}</template>
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
import { getRoomList, deleteRoom } from '../api/room'

const loading = ref(false)
const list = ref([])

const fetchList = async () => {
  loading.value = true
  try {
    const res = await getRoomList()
    list.value = res.data
  } finally {
    loading.value = false
  }
}

const handleAdd = () => ElMessage.info('请参考完整代码实现添加功能')
const handleEdit = (row) => ElMessage.info('请参考完整代码实现编辑功能')
const handleDelete = async (row) => {
  await ElMessageBox.confirm(`确定要删除房间${row.room_number}吗？`, '提示', { type: 'warning' })
  await deleteRoom(row.id)
  ElMessage.success('删除成功')
  fetchList()
}

onMounted(() => fetchList())
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>
