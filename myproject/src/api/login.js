import wepy from 'wepy';

const login = async (params) => {
    let login_res = await wepy.login();
    console.log(login_res.code)
    let code = login_res.code
    let get_res = await wepy.getUserInfo()
    let encryptedData = get_res.encryptedData || 'encry';
    let iv = get_res.iv || 'iv';
    let jwt = await wepy.request({
        url:
            'http://192.168.137.241:8000' +
            '/auth/token?code=' +
            code,
        data: {
            username: encryptedData,
            password: iv,
            grant_type: 'password',
            auth_approach: 'wxapp'
        },
        method: 'POST',
        header: {
            'Content-Type':
                'application/x-www-form-urlencoded'
        },
    });
    wx.showToast({
        title: '登录成功',
        icon: 'success'
    });
    wx.setStorageSync('jwt',jwt);
    console.log(jwt)
    return jwt
}

module.exports = {
    login
}

