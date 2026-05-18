import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Layout from '../views/Layout.vue'
import BuildingList from '../views/BuildingList.vue'
import RoomList from '../views/RoomList.vue'
import StudentList from '../views/StudentList.vue'
import CheckInList from '../views/CheckInList.vue'
import RepairList from '../views/RepairList.vue'

const routes = [
  { path: '/login', name: 'Login', component: Login },
  {
    path: '/',
    name: 'Layout',
    component: Layout,
    redirect: '/buildings',
    children: [
      { path: 'buildings', name: 'BuildingList', component: BuildingList, meta: { title: '宿舍楼管理' } },
      { path: 'rooms', name: 'RoomList', component: RoomList, meta: { title: '房间管理' } },
      { path: 'students', name: 'StudentList', component: StudentList, meta: { title: '学生管理' } },
      { path: 'checkin', name: 'CheckInList', component: CheckInList, meta: { title: '入住管理' } },
      { path: 'repair', name: 'RepairList', component: RepairList, meta: { title: '报修管理' } }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.path !== '/login' && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
