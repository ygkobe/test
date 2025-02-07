<template>
  <div style="max-width: 100%; ">
    <el-row :gutter="20">

    </el-row>

    <el-table
      v-loading="loading"
      element-loading-text="数据加载中..."
       :element-loading-spinner="svg"
      :data="currentPageData"
      style="width: 100%; border-radius: 15px; box-shadow: none;  height: auto; padding: 5px; "
    >

      <el-table-column prop="answer">
        <template #header>
          <el-input
            v-model.trim="searchText"
            placeholder="搜索问题"
            :prefix-icon="Search"
            @input="handleSearch"
            style="border-radius: 120px; width: 100%;"
          />
        </template>

        <template #default="scope">
          <el-card
            style="max-width: 100%; border-radius: 5px; overflow-y: auto"
          >
            <template #header>
              <div>


                <el-text
                  type="info"
                  tag="b"
                  style="font-size: 16px; color: black"
                >
                    <el-tag type="primary">{{ scope.row.ip }}</el-tag>
                  <el-tag type="info">{{ scope.row.create_time }}</el-tag>


                </el-text>

              </div>
            </template>
              <div>
                  {{ scope.row.question }}
              </div>

          </el-card>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      :page-sizes="[5, 10, 15, 20, 25]"
      :page-size="pageSize"
      :current-page.sync="currentPage"
      layout="total,sizes,prev,pager,next,jumper"
      :total="filteredData.length"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      style="margin: 10px"
    ></el-pagination>
  </div>
</template>

<script setup lang="ts">
import { Calendar, Search } from '@element-plus/icons-vue';
import MarkdownIt from 'markdown-it';
import { ref, computed, onBeforeMount } from 'vue';
import axios from 'axios';

const md = new MarkdownIt();

const pageSize = ref(5);
const currentPage = ref(1);
const searchText = ref('');
const dataList = ref([]);
const loading = ref(true); // Loading indicator state

onBeforeMount(() => {
  axios
    .get('http://127.0.0.1:8002/chat/history/')
    .then((response) => {
      console.log(response.data);
      dataList.value = response.data.reverse();
    })
    .catch((error) => {
      console.error('Error loading data:', error);
    })
    .finally(() => {
      loading.value = false; // Set loading to false when data loading is complete
    });
});

const handleSearch = () => {
  currentPage.value = 1; // Reset to first page when searching
};

interface Item {
    question: string;
    // other properties as needed
}

const filteredData = computed(() => {
  if (searchText.value === '') {
    return dataList.value;
  } else {
    return (dataList.value as Item[]).filter(item => item.question.includes(searchText.value));
  }
});

const svg = `
        <path class="path" d="
          M 30 15
          L 28 17
          M 25.61 25.61
          A 15 15, 0, 0, 1, 15 30
          A 15 15, 0, 1, 1, 27.99 7.5
          L 15 15
        " style="stroke-width: 4px; fill: rgba(0, 0, 0, 0)"/>
      `

const currentPageData = computed(() => {
  const startIndex = (currentPage.value - 1) * pageSize.value;
  return filteredData.value.slice(startIndex, startIndex + pageSize.value);
});

const handleSizeChange = (val: number) => {
  pageSize.value = val;
  currentPage.value = 1; // Reset to first page when changing page size
};

const handleCurrentChange = (val: number) => {
  currentPage.value = val;
};
</script>

<style scoped>
.dialog-footer button:first-child {
  margin-right: 10px;
}

.my-message-box.el-message-box__header {
  background-color: #3498db;
  color: white;
}

.my-message-box.el-message-box__content {
  font-size: 16px;
}

.el-row {
  margin-bottom: 20px;
}

.el-row:last-child {
  margin-bottom: 0;
}

.el-col {
  border-radius: 4px;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
</style>
