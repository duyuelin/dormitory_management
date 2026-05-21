<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>报修管理</span>
        <el-button type="primary" @click="handleSubmit"><el-icon><Plus /></el-icon>提交报修</el-button>
      </div>
    </template>
    <el-table :data="list" v-loading="loading" stripe>
      <el-table-column prop="building_name" label="宿舍楼" width="100" />
      <el-table-column prop="room_number" label="房间号" width="100" />
      <el-table-column prop="repair_type" label="报修类型" width="100" />
      <el-table-column prop="description" label="问题描述" min-width="200" />
      <el-table-column prop="contact_phone" label="联系电话" width="120" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="scope">
          <el-tag :type="getStatusType(scope.row.status)" size="small">{{ getStatusText(scope.row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="handler" label="处理人" width="100" />
      <el-table-column label="操作" width="100" fixed="right">
        <template #default="scope">
          <el-button v-if="scope.row.status === 0" type="success" size="small" @click="handleRepair(scope.row)">处理</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { getRepairList, handleRepair as doHandleRepair } from '../api/repair'

const loading = ref(false)
const list = ref([])

const getStatusType = (status) => ({ 0: 'warning', 1: 'primary', 2: 'success', 3: 'info' }[status] || 'info')
const getStatusText = (status) => ({ 0: '待处理', 1: '处理中', 2: '已完成', 3: '已取消' }[status] || '未知')

const fetchList = async () => {
  loading.value = true
  try {
    const res = await getRepairList()
    list.value = res.data
  } finally {
    loading.value = false
  }
}

const handleSubmit = () => ElMessage.info('请参考完整代码实现报修功能')
const handleRepair = async (row) => {
  await doHandleRepair(row.id, { status: 2, handle_result: '已修复' })
  ElMessage.success('处理完成')
  fetchList()
}

onMounted(() => fetchList())
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>
