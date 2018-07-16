import {
    wxRequest
} from '@/utils/wxRequest';

const apiBenshi = 'http://192.168.137.241:8000'


//测试能否连接本地服务器
const testCode = (params) => wxRequest(params, apiBenshi + "/new_add");

//获取分类页面的大分类和小分类标签
const getCategory = (params) => wxRequest(params, apiBenshi + "/api/get_category");
//获取首页推荐标签
const getIndex = (params) => wxRequest(params, apiBenshi + "/api/get_index/recommand");
//获取卖家用户详情
const getPerson = (params) => wxRequest(params, apiBenshi + "/api/get_person");

export default {
    getCategory,
    getIndex,
    getPerson
}