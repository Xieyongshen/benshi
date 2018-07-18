import wepy from 'wepy';
import util from './util';
import md5 from './md5';
import tip from './tip'

const API_SECRET_KEY = 'www.benshi.com'
const TIMESTAMP = util.getCurrentTime()
const SIGN = md5.hex_md5((TIMESTAMP + API_SECRET_KEY).toLowerCase())

// const wxRequest = async(params = {}, url) => {
//     tip.loading();
//     let data = params.query || {};
//     data.sign = SIGN;
//     data.time = TIMESTAMP;
//     let res = await wepy.request({
//         url: url,
//         method: params.method || 'GET',
//         data: data,
//         header: { 'Content-Type': 'application/json' },
//     });
//     tip.loaded();
//     return res;
// };

const wxRequest = async(params = {}, url) => {
    tip.loading();
    let data = params.query || {};
    let res = await wepy.request({
        url: url,
        method: params.method || 'GET',
        data: data,
        header: params.header || { 'Content-Type': 'application/json' },
        // success: function(res1) {
        //     // console.log(res1)
        //     return res1;
        // }
    });
    // console.log(res)
    tip.loaded();
    return res;
};


module.exports = {
    wxRequest
}
