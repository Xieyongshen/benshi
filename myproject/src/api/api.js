import {
    wxRequest
} from '@/utils/wxRequest';

const apiBenshi = 'http://192.168.137.241:8000'


//测试能否连接本地服务器
const testCode = (params) => wxRequest(params, apiBenshi + "/new_add");
//进入me页面后自动检测登录态并获取头像昵称以登录
const login = (params) => wxRequest(params, apiBenshi + "/login");

//获取分类页面的大分类和小分类标签
const getCategory = (params) => wxRequest(params, apiBenshi + "/api/get_category");
//获取首页推荐标签
const getIndex = (params) => wxRequest(params, apiBenshi + "/api/get_index/recommand");
//获取卖家用户详情
const getPerson = (params) => wxRequest(params, apiBenshi + "/api/get_person");

//修改个人签名
const changeDesc = (params) => wxRequest(params, apiBenshi + "/api/changeDesc");

//获取个人关注列表
const getFollow = (params) => wxRequest(params, apiBenshi + "/api/get_follow");
//获取个人收藏列表
const getStar = (params) => wxRequest(params, apiBenshi + "/api/get_star");
//获取某个标签类关注状态
const getFollowStatus = (params) => wxRequest(params, apiBenshi + "/api/get_followstatus");
//改变某个标签的关注状态
const changeFollowStatus = (params) => wxRequest(params, apiBenshi + "/api/change_followstatus");
export default {
    getCategory,
    getIndex,
    getPerson,
    login,
    getFollow,
    getStar,
    changeDesc,
    getFollowStatus,
    changeFollowStatus
}