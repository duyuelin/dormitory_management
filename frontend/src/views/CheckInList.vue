<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>入住管理</span>
        <el-button type="primary" @click="handleCheckIn"><el-icon><Plus /></el-icon>办理入住</el-button>
      </div>
    </template>
    <el-table :data="list" v-loading="loading" stripe>
      <el-table-column prop="student_no" label="学号" width="120" />
      <el-table-column prop="student_name" label="姓名" width="100" />
      <el-table-column prop="building_name" label="宿舍楼" width="100" />
      <el-table-column prop="room_number" label="房间号" width="100" />
      <el-table-column prop="bed_number" label="床位号" width="80" />
      <el-table-column prop="check_in_date" label="入住日期" width="120" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="scope">
          <el-tag :type="getStatusType(scope.row.status)" size="small">{{ getStatusText(scope.row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="100" fixed="right">
        <template #default="scope">
          <el-button v-if="scope.row.status === 1" type="warning" size="small" @click="handleCheckOut(scope.row)">退宿</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { getCheckInList, checkOut } from '../api/checkin'

const loading = ref(false)
const list = ref([])

const getStatusType = (status) => ({ 0: 'info', 1: 'success' }[status] || 'info')
const getStatusText = (status) => ({ 0: '已退宿', 1: '在住' }[status] || '未知')

const fetchList = async () => {
  loading.value = true
  try {
    const res = await getCheckInList()
    list.value = res.data
  } finally {
    loading.value = false
  }
}

const handleCheckIn = () => ElMessage.info('请参考完整代码实现入住功能')
const handleCheckOut = async (row) => {
  await ElMessageBox.confirm(`确定要为学生${row.student_name}办理退宿吗？`, '提示', { type: 'warning' })
  await checkOut(row.id)
  ElMessage.success('退宿成功')
  fetchList()
}

onMounted(() => fetchList())
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>
