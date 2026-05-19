<template>
  <el-container class="layout-container">
    <el-aside width="200px" class="aside">
      <div class="logo">🏠 宿舍管理系统</div>
      <el-menu :default-active="$route.path" router class="menu" background-color="#304156" text-color="#bfcbd9" active-text-color="#409eff">
        <el-menu-item index="/buildings"><el-icon><OfficeBuilding /></el-icon>宿舍楼管理</el-menu-item>
        <el-menu-item index="/rooms"><el-icon><House /></el-icon>房间管理</el-menu-item>
        <el-menu-item index="/students"><el-icon><User /></el-icon>学生管理</el-menu-item>
        <el-menu-item index="/checkin"><el-icon><DocumentChecked /></el-icon>入住管理</el-menu-item>
        <el-menu-item index="/repair"><el-icon><Tools /></el-icon>报修管理</el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <div class="header-right">
          <el-dropdown @command="handleCommand">
            <span class="user-info">
              <el-icon><User /></el-icon>
              {{ user.real_name || user.username }}
              <el-icon class="el-icon--right"><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-main class="main"><router-view /></el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { OfficeBuilding, House, User, DocumentChecked, Tools, ArrowDown } from '@element-plus/icons-vue'

const router = useRouter()
const user = ref(JSON.parse(localStorage.getItem('user') || '{}'))

const handleCommand = (command) => {
  if (command === 'logout') {
    ElMessageBox.confirm('确定要退出登录吗？', '提示', { type: 'warning' }).then(() => {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      ElMessage.success('已退出登录')
      router.push('/login')
    })
  }
}
</script>

<style scoped>
.layout-container { height: 100vh; }
.aside { background-color: #304156; }
.logo { height: 60px; display: flex; align-items: center; justify-content: center; color: #fff; font-size: 16px; font-weight: bold; border-bottom: 1px solid #1f2d3d; }
.menu { border-right: none; }
.header { background-color: #fff; box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08); display: flex; align-items: center; justify-content: flex-end; }
.user-info { cursor: pointer; display: flex; align-items: center; color: #606266; }
.main { background-color: #f0f2f5; padding: 20px; }
</style>
