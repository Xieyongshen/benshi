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
//获取卖家label下service详情
const getLabelServices = (params) => wxRequest(params, apiBenshi + "/api/get_labelServices");
//获取服务详情
const getServiceDetail = (params) => wxRequest(params, apiBenshi + "/api/get_serviceDetail");
//按分类获取标签详情
const getLabelOfTag = (params) => wxRequest(params, apiBenshi + "/api/get_labeloftag");


//修改个人签名
const changeDesc = (params) => wxRequest(params, apiBenshi + "/api/changeDesc");

//获取个人关注列表
const getFollow = (params) => wxRequest(params, apiBenshi + "/api/get_follow");
//获取个人收藏列表
const getStar = (params) => wxRequest(params, apiBenshi + "/api/get_star");
//获取某个tag类关注状态
const getFollowStatus = (params) => wxRequest(params, apiBenshi + "/api/get_followstatus");
//改变某个tag的关注状态
const changeFollowStatus = (params) => wxRequest(params, apiBenshi + "/api/change_followstatus");
//改变某个label的收藏状态
const changeStarStatus = (params) => wxRequest(params, apiBenshi + "/api/change_starstatus");
//删除收藏列表中的某些标签
const deleteStar = (params) => wxRequest(params, apiBenshi + "/api/delete_star");

//用户提交订单
const submitTheOrder = (params) => wxRequest(params, apiBenshi + "/api/submitTheOrder");
//获取用户所有订单
const getOrders = (params) => wxRequest(params, apiBenshi + "/api/getOrders");
//获取用户订单详情
const getOrderDetail = (params) => wxRequest(params, apiBenshi + "/api/getOrderDetail");
export default {
    getCategory,
    getIndex,
    getPerson,
    login,
    getFollow,
    getStar,
    changeDesc,
    getFollowStatus,
    changeFollowStatus,
    changeStarStatus,
    getLabelOfTag,
    deleteStar,
    getLabelServices,
    getServiceDetail,
    submitTheOrder,
    getOrders,
    getOrderDetail
}