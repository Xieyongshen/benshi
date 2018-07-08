import {
    wxRequest
} from '@/utils/wxRequest';

const apiBenshi = ''

//微信的jscode换取sessionKey
const wxJsCode2Session = (params) => wxRequest(params, apiBenshi + "/api/wechat/jscode2session");
const user2session = (params) => wxRequest(params, apiBenshi + "/api/wechat/user2session?jsoncallback=?");