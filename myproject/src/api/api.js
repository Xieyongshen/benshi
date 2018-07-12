import {
    wxRequest
} from '@/utils/wxRequest';

const apiBenshi = 'http://127.0.0.1:8000'

//微信的jscode换取sessionKey
const wxJsCode2Session = (params) => wxRequest(params, apiBenshi + "/api/wechat/jscode2session");
const user2session = (params) => wxRequest(params, apiBenshi + "/api/wechat/user2session?jsoncallback=?");

//测试能否连接本地服务器
const testCode = (params) => wxRequest(params, apiBenshi + "/new_add");