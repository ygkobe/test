<template>
    <div class="block" style="margin: 20px">

        <el-button @click="centerDialogVisible = true" type="primary" style="margin-left: 20px">创建分组</el-button>

        <el-input v-model="searchQuery" @input="searchGroups" aria-label="搜索分组名" placeholder="搜索分组名"
                  style="margin: 10px; width: 300px; float: right"/>

        <el-dialog v-model="centerDialogVisible" title="创建数据分组" width="30%">
            <el-input v-model="groupName" aria-label="请输入分组名" placeholder="请输入分组名"
                      style="margin: 10px; width: 300px"/>

            <el-upload
                    ref="upload"
                    class="upload-demo"
                    :limit="1"
                    :on-exceed="handleExceed"
                    :auto-upload="false"
                    :file-list="fileList"
                    @change="handleChange"
                    style="margin: 10px"
            >
                <template #trigger>
                    <el-button type="primary">上传文件</el-button>
                </template>
            </el-upload>

            <template #footer>
                <span class="dialog-footer">
                    <el-button type="primary" @click="submitUpload">提交</el-button>
                </span>
            </template>
        </el-dialog>

        <el-dialog v-model="dialogVisible" title="组员车牌号详情" width="70%">
            <el-table :data="currentTableDataInner" style="width: 100%">
<!--                <el-table-column label="id" prop="id"/>-->
                <el-table-column label="分组名" prop="group_name"/>
                <el-table-column label="车牌号" prop="car_number"/>
                <el-table-column align="right">
                    <template #header>
                        <el-input v-model="searchDetails" size="small" @input="searchGroupsInner" placeholder="搜索车牌号"/>
                    </template>
                    <template #default="scope">
                        <el-button size="small" @click="handleEditDetails(scope.$index, scope.row)">编辑</el-button>
                        <el-button size="small" type="danger" @click="handleDeleteDetails(scope.$index, scope.row)">
                            删除
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>

            <!-- 编辑模态框 -->
            <el-dialog title="编辑车牌号信息" v-model="editDialogVisible" width="50%">
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

            <!-- 分页组件 -->
            <div class="demo-pagination-block" style="margin-top: 20px;">
                <el-pagination
                        v-model:currentPage="currentPageInner"
                        v-model:page-size="pageSizeInner"
                        :page-sizes="[10, 20, 30, 40]"
                        layout="total, sizes, prev, pager, next, jumper"
                        :total="totalItemsInner"
                        @size-change="handleSizeChangeInner"
                        @current-change="handleCurrentChangeInner"
                />
            </div>

            <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">关闭</el-button>
        </span>
            </template>
        </el-dialog>


        <div style="margin: 10px; margin-top: 20px">
            <el-table :data="currentTableData" style="width: 100%" :row-class-name="'custom-table-row'">
                <el-table-column prop="id" label="id" width="100"/>


                <el-table-column>
                    <template #header>
                        分组名
                    </template>
                    <template #default="scope">

                        <el-button type="text" @click="handleEdit(scope.row.group_name, scope.row.create_time)">
                            {{ scope.row.group_name }}
                        </el-button>


                    </template>
                </el-table-column>

                <el-table-column prop="create_time" label="创建时间"/>


                <el-table-column prop="count" label="分组数量" witdh="80"/>

                <el-table-column width="400">
                    <template #header>
                        选择时间
                    </template>
                    <template #default="scope">
                        <el-date-picker
                                v-model="dateRanges[scope.$index]"
                                type="daterange"
                                unlink-panels
                                range-separator="至"
                                start-placeholder="开始日期"
                                end-placeholder="结束日期"
                                :shortcuts="shortcuts"
                                :size="size"
                        />
                    </template>
                </el-table-column>

                <el-table-column>
                    <template #header>
                        填写token
                    </template>
                    <template #default="scope">
                        <el-input v-model="tokenInputs[scope.$index]" type="text" aria-label="请输入token"
                                  placeholder="请输入token"/>
                    </template>
                </el-table-column>

                <el-table-column width="170">
                    <template #header>
                        执行进度
                    </template>
                    <template #default="scope">

                        <el-progress
                                :text-inside="true"
                                :stroke-width="24"
                                :percentage="percentages[scope.$index]"
                                :status="statuses[scope.$index]"
                                :striped="percentages[scope.$index] < 100"
                                :striped-flow="percentages[scope.$index] < 100"
                                :duration="3"
                        />
                    </template>
                </el-table-column>

                <el-table-column align="right">
                    <template #header>
                        操作
                    </template>
                    <template #default="scope">

                        <el-popconfirm
                                confirm-button-text="是"
                                cancel-button-text="否"
                                :icon="InfoFilled"
                                icon-color="#626AEF"
                                title="是否删除此分组"
                                @confirm="confirmEvent(scope.row.group_name, scope.row.create_time)"
                                @cancel="cancelEvent"
                        >
                            <template #reference>
                                <el-button>删除</el-button>
                            </template>
                        </el-popconfirm>


                        <el-button
                                :loading="execute_loading[scope.$index]"
                                element-loading-text="Loading..."
                                element-loading-spinner="el-icon-loading"
                                type="primary"
                                @click="sendRequest(scope.$index, scope.row)">执行
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>

        <div class="demo-pagination-block" style="margin-top: 20px;">
            <el-pagination
                    v-model:currentPage="currentPage"
                    v-model:page-size="pageSize"
                    :page-sizes="[10, 20, 30, 40]"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="totalItems"
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
            />
        </div>
    </div>
</template>

<script lang="ts" setup>
import {ref, computed, onMounted} from 'vue';
import axios from 'axios';
import {ElMessage, ElNotification} from 'element-plus';
import type {UploadInstance, UploadProps, UploadUserFile, UploadRawFile} from 'element-plus';
import {genFileId} from 'element-plus';

const centerDialogVisible = ref(false);
const groupName = ref('');
const size = ref<'' | 'large' | 'small'>('');
const fileList = ref<UploadUserFile[]>([]);
const tableData = ref([]);
const dateRanges = ref<Record<number, [string, string] | null>>({});
const dialogVisible = ref(false);
const dialogMessageTable = ref([]);
const tokenInputs = ref<Record<number, string>>({});

// 使用对象记录每行的loading状态
const execute_loading = ref<Record<number, boolean>>({});

const upload = ref<UploadInstance | null>(null);
// 分页相关引用
const currentPage = ref(1);
const currentPageInner = ref(1);
const pageSize = ref(10);
const pageSizeInner = ref(10);
const totalItems = ref(0);
const totalItemsInner = ref(0);

// 搜索相关引用
const searchQuery = ref('');
const filteredTableData = ref([]);
const filteredTableDataInner = ref([]);

const percentage = ref(0);
const status = ref('active');

const percentages = ref<Record<number, number>>({});
const statuses = ref<Record<number, string>>({});


// 定义一个对象来存储每个进度条对应的 taskId 和 intervalId
const taskDetails = ref<Record<number, { taskId: string | null, intervalId: number | null }>>({});

const getProgress = async (index: number, group_name: string, cstDateRange: any) => {
    const taskId = taskDetails.value[index]?.taskId;
    if (!taskId) return; // 如果 taskId 不存在，直接返回

    const response = await fetch(`http://127.0.0.1:8002/violation/task/get_progress/?task_id=${taskId}`);
    const data = await response.json();
    percentages.value[index] = data.progress;

    if (percentages.value[index] < 41) {
        statuses.value[index] = 'exception';
    } else if (percentages.value[index] <= 70) {
        statuses.value[index] = 'warning';
    } else if (percentages.value[index] <= 90) {
        statuses.value[index] = '';
    } else if (percentages.value[index] === 100) {
        statuses.value[index] = 'success';
        ElNotification({
            title: '任务执行完成',
            message: '请打开下载目录，查看excel文件',
            duration: 0,
            type: 'success'
        });

        // 任务完成后停止当前进度条的轮询
        if (taskDetails.value[index]?.intervalId !== null) {
            clearInterval(taskDetails.value[index].intervalId!);
        }

        // 动态生成文件名
        const currentDateTime = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
        const customFileName = `${group_name}_${currentDateTime}.xlsx`;

        // 生成下载链接并下载文件
        const downloadUrl = `http://127.0.0.1:8002/violation/task/download_excel/?task_id=${taskId}&group_name=${group_name}&date_range=${cstDateRange}`;
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = customFileName; // 使用自定义的文件名
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
};


// 计算当前页数据
const currentTableData = computed(() => {
    const start = (currentPage.value - 1) * pageSize.value;
    const end = start + pageSize.value;
    return filteredTableData.value.slice(start, end);
});

// Computed property for paginated table data
const currentTableDataInner = computed(() => {
  const start = (currentPageInner.value - 1) * pageSizeInner.value;
  const end = start + pageSizeInner.value;
  return filteredTableDataInner.value.slice(start, end);
});



const searchGroups = () => {
    if (!searchQuery.value) {
        filteredTableData.value = tableData.value;
    } else {
        filteredTableData.value = tableData.value.filter((group: any) =>
            group.group_name.includes(searchQuery.value)
        );
    }
    totalItems.value = filteredTableData.value.length;
    handleCurrentChange(1);
};
// Search function to filter table data based on searchDetails


const searchGroupsInner = () => {
    console.log(searchDetails.value)
  if (!searchDetails.value) {
    filteredTableDataInner.value = dialogMessageTable.value; // Restore full data
  } else {
    filteredTableDataInner.value = dialogMessageTable.value.filter((group: any) =>
      group.car_number.includes(searchDetails.value)
    );
  }
  totalItemsInner.value = filteredTableDataInner.value.length;
    handleCurrentChangeInner(1);
};




const handleEdit = async (group_name: string, create_time: string) => {

    try {
        const response = await axios.get('http://127.0.0.1:8002/violation/history/group_name_details/?group_name=' + group_name + "&create_time=" + create_time, {
            headers: {
                'Content-Type': 'application/json'
            }
        });

        dialogMessageTable.value = response.data || 'No details available';
        filteredTableDataInner.value = dialogMessageTable.value;
        totalItemsInner.value = filteredTableDataInner.value.length;

        dialogVisible.value = true;
    } catch (error) {
        console.error('There was an error fetching the group details!', error);
        ElMessage.error('获取分组详情失败');
    }
};

const handleExceed: UploadProps['onExceed'] = (files) => {
    upload.value!.clearFiles();
    const file = files[0] as UploadRawFile;
    file.uid = genFileId();
    upload.value!.handleStart(file);
};

const handleChange = (file: UploadUserFile) => {
    fileList.value = [file];
};

const submitUpload = async () => {
    if (!groupName.value) {
        ElMessage.warning('请先输入分组名');
        return;
    }

    if (fileList.value.length === 0) {
        ElMessage.warning('请先上传文件');
        return;
    }

    const formData = new FormData();
    // formData.append('file', fileList.value[0].raw);
    formData.append('file', fileList.value[0].raw as Blob);
    formData.append('group_name', groupName.value);

    try {
        centerDialogVisible.value = false;
        ElMessage.success('分组请求已发送');
        const response = await axios.post('http://127.0.0.1:8002/violation/upload/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
        // console.log('Response:', response.data);
        ElMessage.success('分组创建成功');
        fetchGroupHistory()
        // window.location.reload()

    } catch (error) {
        console.error('There was an error uploading the file!', error);
        ElMessage.error('分组创建失败，请检查文件格式');
    } finally {
        centerDialogVisible.value = false;
        fileList.value = [];
        groupName.value = '';
        fetchGroupHistory();
    }
};


async function sendRequest(index: number, row: any) {
    // startTask(index);

    const dateRange = dateRanges.value[index];

    const token = tokenInputs.value[index];
    if (!dateRange) {
        ElMessage.warning('请先选择日期范围');
        return;
    }

    // Convert dateRange to China Standard Time (CST)
    const convertToCST = (date: string) => {
        const utcDate = new Date(date);
        const cstDate = new Date(utcDate.getTime() + 8 * 60 * 60 * 1000);
        return cstDate.toISOString().slice(0, 10);
    };

    const cstDateRange = dateRange.map((date: string) => convertToCST(date));
    // console.log(cstDateRange)

    if (!token) {
        ElMessage.warning('请先填写token');
        return;
    }

    try {
        // 设置当前行的loading状态
        execute_loading.value[index] = true;


        const response = await axios.post('http://127.0.0.1:8002/violation/task/start_task/', {
            group_id: row.id,
            date_range: cstDateRange,
            token: token,
            group_name: row.group_name,
            create_time: row.create_time
        }, {
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const data = response.data;
        // 保存 taskId 和 intervalId 到 taskDetails 中

        taskDetails.value[index] = {
            taskId: data.task_id,
            intervalId: window.setInterval(() => getProgress(index, row.group_name, cstDateRange), 700),
        };

        ElMessage.success('开始任务');
    } catch (error) {
        console.error('There was an error opening the webpage!', error);
        ElMessage.error('请求失败');
    } finally {
        // 重置当前行的loading状态
        execute_loading.value[index] = false;
    }
}


const fetchGroupHistory = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:8002/violation/history/group_history/', {
            headers: {
                'Content-Type': 'application/json'
            }
        });
        tableData.value = response.data;
        filteredTableData.value = tableData.value;
        totalItems.value = filteredTableData.value.length;
    } catch (error) {
        console.error('There was an error fetching the group history!', error);
        ElMessage.error('获取历史记录失败');
    }
};

onMounted(fetchGroupHistory);

const shortcuts = ref([
    {
        text: '最近一周',
        value: () => {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
            return [start, end];
        },
    },
    {
        text: '最近一个月',
        value: () => {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
            return [start, end];
        },
    },
    {
        text: '最近三个月',
        value: () => {
            const end = new Date();
            const start = new Date();
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 90);
            return [start, end];
        },
    },
]);

const handleSizeChange = (newSize: number) => {
    pageSize.value = newSize;
    handleCurrentChange(1);
};

const handleSizeChangeInner = (newSize: number) => {
    pageSizeInner.value = newSize;
    handleCurrentChangeInner(1);
};

const handleCurrentChange = (newPage: number) => {
    currentPage.value = newPage;
};

const handleCurrentChangeInner = (newPage: number) => {
    currentPageInner.value = newPage;
};




import {InfoFilled} from '@element-plus/icons-vue'

const confirmEvent = async (group_name: string, create_time: string) => {
    try {
        // 发送DELETE请求
        const response = await axios.delete('http://127.0.0.1:8002/violation/history/delete_group/', {
            data: {
                group_name: group_name,
                create_time: create_time
            },
            headers: {
                'Content-Type': 'application/json'
            }
        })

        // 请求成功后的处理
        // console.log('Delete response:', response.data)
        ElMessage({
            message: '成功删除分组: ' + group_name,
            type: 'success',
        })
        // window.location.reload()
        fetchGroupHistory()

    } catch (error) {
        console.error('Error deleting group:', error)
        ElMessage.error('删除分组失败 ' + error)
    } finally {
        fetchGroupHistory();
    }
}

const cancelEvent = () => {
    // console.log('cancel!')
    ElMessage('取消删除分组')
}


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


const handleEditDetails = (index: number, row: User) => {
    editFormData.value = {...row}
    editDialogVisible.value = true
}

const saveEditDetails = async () => {
    try {
        const response = await axios.post('http://127.0.0.1:8002/violation/history/car_number_edit/', {
            id: editFormData.value.id,
            group_name: editFormData.value.group_name,
            car_number: editFormData.value.car_number,
            create_time: editFormData.value.create_time
        })
        console.log('保存成功:', response.data)

        const index = fetchTableDataDetails.value.findIndex((item) => item.id === editFormData.value.id)
        if (index !== -1) {
            fetchTableDataDetails.value[index] = {...editFormData.value}
        }

        handleEdit(editFormData.value.group_name, editFormData.value.create_time)

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

<style scoped>
/* 样式部分保持不变 */
.el-popper.is-customized {
    /* Set padding to ensure the height is 32px */
    padding: 6px 12px;
    background: linear-gradient(90deg, rgb(159, 229, 151), rgb(204, 229, 129));
}

.el-popper.is-customized .el-popper__arrow::before {
    background: linear-gradient(45deg, #b2e68d, #bce689);
    right: 0;
}

.el-table.custom-table-row {
    --el-table-tr-bg-color: #f5f5f5; /* 浅灰色背景 */
}
</style>
