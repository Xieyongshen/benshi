import {
    wxRequest
} from '@/utils/wxRequest';

const apiBenshi = 'http://134.175.18.136:8000'


//测试能否连接本地服务器
const testCode = (params) => wxRequest(params, apiBenshi + "/new_add");
//进入me页面后自动检测登录态并获取头像昵称以登录
const login = (params) => wxRequest(params, apiBenshi + "/login");
//获取热门关键词
const getHotSearch = (params) => wxRequest(params, apiBenshi + "/api/getHotSearch");
//获取搜索结果
const getSearchResult = (params) => wxRequest(params, apiBenshi + "/api/getSearchResult");

//获取分类页面的大分类和小分类标签
const getCategory = (params) => wxRequest(params, apiBenshi + "/api/get_category");
//获取首页推荐标签
const getIndex = (params) => wxRequest(params, apiBenshi + "/api/get_index/recommand");
//获取卖家用户详情
const getPerson = (params) => wxRequest(params, apiBenshi + "/api/get_person");
const get_personWithoutLogin = (params) => wxRequest(params, apiBenshi + "/api/get_personWithoutLogin");

//获取卖家label下service详情
const getLabelServices = (params) => wxRequest(params, apiBenshi + "/api/get_labelServices");
//获取服务详情
const getServiceDetail = (params) => wxRequest(params, apiBenshi + "/api/get_serviceDetail");
//按分类获取标签详情
const getLabelOfTag = (params) => wxRequest(params, apiBenshi + "/api/get_labeloftag");
//获取服务下评价列表
const getComment = (params) => wxRequest(params, apiBenshi + "/api/getComment");

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
//获取单个订单详情
const getOrderDetail = (params) => wxRequest(params, apiBenshi + "/api/getOrderDetail");
//更改订单状态
const changeOrderStatus = (params) => wxRequest(params, apiBenshi + "/api/changeOrderStatus");
//删除订单
const deleteTheOrder = (params) => wxRequest(params, apiBenshi + "/api/deleteTheOrder");
//评价订单
const submitComment = (params) => wxRequest(params, apiBenshi + "/api/submitComment");
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
    getOrderDetail,
    changeOrderStatus,
    deleteTheOrder,
    submitComment,
    getComment,
    getSearchResult,
    getHotSearch,
    get_personWithoutLogin
}