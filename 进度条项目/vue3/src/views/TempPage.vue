<template>
    <div>
        <el-table :data="filterfetchTableDataDetailsDetails" style="width: 100%" height="350" >
<!--            <el-table-column label="id" prop="id"/>-->
            <el-table-column label="分组名" prop="group_name"/>
            <el-table-column label="创建时间" prop="create_time"/>
            <el-table-column label="车牌号" prop="car_number"/>
            <el-table-column align="right">
                <template #header>
                    <el-input v-model="searchDetails" size="small" placeholder="搜索车牌号"/>
                </template>
                <template #default="scope">
                    <el-button size="small" @click="handleEditDetails(scope.$index, scope.row)">
                        编辑
                    </el-button>
                    <el-button
                            size="small"
                            type="danger"
                            @click="handleDeleteDetails(scope.$index, scope.row)"
                    >
                        删除
                    </el-button>
                </template>
            </el-table-column>
        </el-table>

        <!-- 编辑模态框 -->
        <el-dialog title="编辑车牌号信息" v-model="editDialogVisible" width="50%" >
            <el-form :model="editFormData" label-width="100px">
                <el-form-item label="分组名">
                    <el-input v-model="editFormData.group_name" disabled/>
                </el-form-item>
                <el-form-item label="创建时间">
                    <el-input v-model="editFormData.create_time" disabled/>
                </el-form-item>
                <el-form-item label="车牌号">
                    <el-input v-model="editFormData.car_number"/>
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="editDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="saveEditDetails">保存</el-button>
            </template>
        </el-dialog>
    </div>
</template>

<script lang="ts" setup>
import { computed, ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

interface User {
    id: string
    group_name: string
    car_number: string
    create_time: string
}

const searchDetails = ref('')
const editDialogVisible = ref(false)
const editFormData = ref<User>({
    id: '',
    group_name: '',
    car_number: '',
    create_time: ''
})

const fetchTableDataDetails = ref<User[]>([])

const fetchfetchTableDataDetails = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:8002/violation/history/group_name_details/', {
            params: {
                group_name: 'ytyt',
                create_time: '2024-08-20 15:18:39'
            }
        })
        fetchTableDataDetails.value = response.data
    } catch (error) {
        console.error('Failed to fetch table data:', error)
        ElMessage({
            message: '数据获取失败',
            type: 'error',
        })
    }
}

onMounted(fetchfetchTableDataDetails)

const filterfetchTableDataDetailsDetails = computed(() =>
    fetchTableDataDetails.value.filter(
        (data) =>
            !searchDetails.value ||
            data.car_number.toLowerCase().includes(searchDetails.value.toLowerCase())
    )
)

const handleEditDetails = (index: number, row: User) => {
    editFormData.value = { ...row }
    editDialogVisible.value = true
}

const saveEditDetails = async () => {
    try {
        const response = await axios.post('http://127.0.0.1:8002/edit', {
            id: editFormData.value.id,
            group_name: editFormData.value.group_name,
            car_number: editFormData.value.car_number,
            create_time: editFormData.value.create_time
        })
        console.log('保存成功:', response.data)

        const index = fetchTableDataDetails.value.findIndex((item) => item.id === editFormData.value.id)
        if (index !== -1) {
            fetchTableDataDetails.value[index] = { ...editFormData.value }
        }
        editDialogVisible.value = false
    } catch (error) {
        console.error('保存失败:', error)
        ElMessage({
            message: '保存失败',
            type: 'error',
        })
    }
}

const handleDeleteDetails = (index: number, row: User) => {
    console.log(index, row)
}
</script>
