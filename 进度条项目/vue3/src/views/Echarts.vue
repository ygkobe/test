<template>
    <div style="max-width: 100%; background-color: #f0f4f8; border-radius: 1px;">
        <el-row :gutter="10">
            <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" style=" padding: 10px">

                <el-text class="mx-1" type="info" size="large">最近一周每天提问次数</el-text>
                <div class="grid-content ep-bg-purple" style="padding: 10px; border: 0.1px solid #000; background-color: #ffffff; border-radius: 8px;">
                    <div id="chart1" class="chart"></div>
                </div>
            </el-col>
            <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" style="padding: 10px">
                <el-text class="mx-1" type="info" size="large">最近一周访问次数最多的5个ip</el-text>
                <div class="grid-content ep-bg-purple-light" style="padding: 10px; border: 0.1px solid #000; background-color: #ffffff; border-radius: 8px;">
                    <div id="chart2" class="chart"></div>
                </div>
            </el-col>
            <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" style="margin-top: 10px; padding: 10px">
                <el-text class="mx-1" type="info" size="large">不同时间段访问次数</el-text>
                <div class="grid-content ep-bg-purple-light" style="padding: 10px; border: 0.1px solid #000; background-color: #ffffff; border-radius: 8px;">
                    <div id="chart3" class="chart"></div>
                </div>
            </el-col>
            <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" style="margin-top: 10px; padding: 10px">

                 <el-text class="mx-1" type="info" size="large">提问类型</el-text>
                <div class="grid-content ep-bg-purple-light" style="padding: 10px; border: 0.1px solid #000; background-color: #ffffff; border-radius: 8px;">
                    <div id="chart4" class="chart"></div>
                </div>
            </el-col>
        </el-row>
    </div>
</template>

<style>
.el-col {
    border-radius: 4px;
}

.grid-content {
    border-radius: 4px;
    min-height: 36px;
    padding: 10px;
}

.chart {
    width: 100%;
    height: 300px;
}
</style>

<script>
import axios from 'axios';
import * as echarts from 'echarts';

export default {
    mounted() {
        this.fetchChart1Data();
        this.fetchChart2Data();
        this.fetchChart3Data();
        this.fetchChart4Data();
    },
    methods: {

        async fetchChart1Data() {
            try {
                const response = await axios.get('http://127.0.0.1:8002/chat/echarts/daily_questions/');
                const data = response.data;
                const chart1 = echarts.init(document.getElementById('chart1'));
                const option = {
                    tooltip: {},
                    xAxis: {
                        data: data.day,
                        axisLine: {
                            lineStyle: {
                                color: '#000' // 轴线颜色
                            }
                        },
                        axisLabel: {
                            color: '#000' // 标签颜色
                        }
                    },
                    yAxis: {
                        axisLine: {
                            lineStyle: {
                                color: '#000' // 轴线颜色
                            }
                        },
                        axisLabel: {
                            color: '#000' // 标签颜色
                        }
                    },
                    series: [
                        {
                            name: '访问次数',
                            type: 'bar',
                            barWidth: 20,
                            data: data.count,
                            itemStyle: {
                                color: '#5470C6'
                            },
                            label: {
                                show: true,
                                position: 'top',
                                fontSize: 14,
                                color: '#000'
                            }
                        }
                    ]
                };
                chart1.setOption(option);
            } catch (error) {
                console.error('Error fetching chart1 data:', error);
            }
        },

        async fetchChart2Data() {
            try {
                const response = await axios.get('http://127.0.0.1:8002/chat/echarts/ip_day_count/');
                const data = response.data;
                const chart2 = echarts.init(document.getElementById('chart2'));
                const option = {
                    tooltip: {
                        trigger: 'axis',
                        textStyle: {
                            color: '#000'
                        }
                    },
                    legend: {
                        data: data.ip_list,
                        textStyle: {
                            color: '#000'
                        }
                    },
                    grid: {
                        top: '10%',
                        left: '5%',
                        right: '4%',
                        bottom: '13%',
                        containLabel: true
                    },
                    toolbox: {
                        feature: {
                            saveAsImage: {}
                        }
                    },
                    xAxis: {
                        type: 'category',
                        boundaryGap: false,
                        data: data.date_list,
                        axisLine: {
                            lineStyle: {
                                color: '#000' // 轴线颜色
                            }
                        },
                        axisLabel: {
                            color: '#000' // 标签颜色
                        }
                    },
                    yAxis: {
                        type: 'value',
                        axisLine: {
                            lineStyle: {
                                color: '#000' // 轴线颜色
                            }
                        },
                        axisLabel: {
                            color: '#000' // 标签颜色
                        }
                    },
                    series: data.series
                };
                chart2.setOption(option);
            } catch (error) {
                console.error('Error fetching chart2 data:', error);
            }
        },

        async fetchChart3Data() {
            try {
                const response = await axios.get('http://127.0.0.1:8002/chat/echarts/different_time_periods/');
                const data = response.data;
                const chart3 = echarts.init(document.getElementById('chart3'));
                const option = {
                    xAxis: {
                        type: 'category',
                        data: data.beijing_hour_created,
                        axisLine: {
                            lineStyle: {
                                color: '#000' // 轴线颜色
                            }
                        },
                        axisLabel: {
                            color: '#000' // 标签颜色
                        }
                    },
                    yAxis: {
                        type: 'value',
                        axisLine: {
                            lineStyle: {
                                color: '#000' // 轴线颜色
                            }
                        },
                        axisLabel: {
                            color: '#000' // 标签颜色
                        }
                    },
                    series: [
                        {
                            data: data.count_per_hour,
                            type: 'line',
                            itemStyle: {
                                color: '#5470C6'
                            },
                            label: {
                                show: true,
                                position: 'top',
                                fontSize: 14,
                                color: '#000'
                            }
                        }
                    ]
                };
                chart3.setOption(option);
            } catch (error) {
                console.error('Error fetching chart3 data:', error);
            }
        },

        async fetchChart4Data() {
            try {
                const response = await axios.get('http://127.0.0.1:8002/chat/echarts/question_type/');
                const data = response.data;
                const chart4 = echarts.init(document.getElementById('chart4'));
                const option = {
                    tooltip: {
                        trigger: 'item',
                        textStyle: {
                            color: '#000'
                        }
                    },
                    legend: {
                        orient: 'vertical',
                        left: 'left',
                        textStyle: {
                            color: '#000'
                        }
                    },
                    series: [
                        {
                            name: '提问类型',
                            type: 'pie',
                            radius: '50%',
                            data: data,
                            emphasis: {
                                itemStyle: {
                                    shadowBlur: 10,
                                    shadowOffsetX: 0,
                                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                                }
                            }
                        }
                    ]
                };
                chart4.setOption(option);
            } catch (error) {
                console.error('Error fetching chart4 data:', error);
            }
        }
    }
};
</script>
