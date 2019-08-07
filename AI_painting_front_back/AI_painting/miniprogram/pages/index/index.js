var context = null;// 使用 wx.createContext 获取绘图上下文 context
var isButtonDown = false;//是否在绘制中
var arrx = [];//动作横坐标
var arry = [];//动作纵坐标
var arrz = [];//总做状态，标识按下到抬起的一个组合
var canvasw = 0;//画布宽度
var canvash = 0;//画布高度
// pages/shouxieban/shouxieban.js
Page({
  /**
 * 页面的初始数据
 */
  data: {
    //canvas宽高
    canvasw: 0,
    canvash: 0,
    //canvas生成的图片路径
    canvasimgsrc: "",
    loading: false
  },
  //画布初始化执行
  startCanvas: function () {
    var that = this;
    //创建canvas
    this.initCanvas();
    //获取系统信息
    wx.getSystemInfo({
      success: function (res) {
        canvasw = res.windowWidth - 0;//设备宽度
        canvash = canvasw;
        that.setData({ 'canvasw': canvasw });//根据设备的宽度和高度对canvas画布的高度和宽度进行赋值
        that.setData({ 'canvash': canvash });
      }
    });

  },
  //初始化函数
  initCanvas: function () {
    // 使用 wx.createContext 获取绘图上下文 context
    context = wx.createCanvasContext('canvas');//获取canvasID为'canvas'的绘图上下文
    context.drawImage("image/white.png", 0, 0, canvasw, canvash);
    context.beginPath();
    context.setStrokeStyle('#000000');//颜色设为黑色
    context.setLineWidth(3);
    context.setLineCap('round');//画出线的的两端是椭圆形的
    context.setLineJoin('round');
  },
  //事件监听
  canvasIdErrorCallback: function (e) {
    console.error(e.detail.errMsg)
  },
  canvasStart: function (event) {
    isButtonDown = true;
    arrz.push(0);
    arrx.push(event.changedTouches[0].x);
    arry.push(event.changedTouches[0].y);

  },
  canvasMove: function (event) {//每次按着移动的时候都会对画面清除并重新绘制一次
    if (isButtonDown) {
      arrz.push(1);
      arrx.push(event.changedTouches[0].x);
      arry.push(event.changedTouches[0].y);

    };
    for (var i = 0; i < arrx.length; i++) {
      if (arrz[i] == 0) { //arrz[i]=0表示该点为绘图起始点
        context.moveTo(arrx[i], arry[i])
      } else {//如果arrz[i]=1表示该点为绘制点
        context.lineTo(arrx[i], arry[i])
      };

    };
    context.clearRect(0, 0, canvasw, canvash);//clearRect()方法清空给定矩形内的指定像素
    context.drawImage("image/white.png", 0, 0, canvasw, canvash);
    context.setStrokeStyle('#000000');
    context.setLineWidth(3);
    context.setLineCap('round');
    context.setLineJoin('round');
    context.stroke();

    context.draw(false);//不进行函数回调
  },
  canvasEnd: function (event) {
    isButtonDown = false;
  },
  //清除画布
  cleardraw: function () {
    //清除画布
    arrx = [];
    arry = [];
    arrz = [];
    context.clearRect(0, 0, canvasw, canvash);
    context.draw(true);
    wx.navigateTo({
      url: '../savedCartoon/savedCartoon'
    })
  },
  //提交签名内容
  setSign: function () {
    this.setData({
      loading: true
    })
    var that = this;
    if (arrx.length == 0) {
      wx.showModal({
        title: '提示',
        content: '签名内容不能为空！',
        showCancel: false
      });
      return false;
    };
    console.log("不是空的，canvas即将生成图片")
    //生成图片
    wx.canvasToTempFilePath({
      canvasId: 'canvas',
      success: function (res) {
        //console.log("canvas可以生成图片")
        //console.log(res.tempFilePath, 'canvas图片地址');
        //that.setData({ canvasimgsrc:res.tempFilePath })
        //把图片保存到相册里
        wx.saveImageToPhotosAlbum({
          filePath: res.tempFilePath,
          success(res) {
            console.log("保存图片：success");
            wx.showToast({
              title: '保存成功',
            });
          },
          fail(res) {
            console.log("保存图片：fail");
            console.log(res);
          }
        })
        
        wx.uploadFile({

          url: "http://106.75.34.228:82/infer-66f28b95-d8ec-4e11-a2fe-14a544cc6b16/",
          filePath: res.tempFilePath,  //文件路径  
          name: 'file',  //随意
          header: {
            'Content-Type': 'multipart/form-data',
            //'Authorization': wx.getStorageSync("access_token")
            //如果需要token的话要传
          },
          formData: {
            method: 'POST'   //请求方式
          },
          success(res) {
            //将收到的图片base64字符串流转化为图片
            //var array = wx.base64ToArrayBuffer(res.data)
            //var base64 = wx.arrayBufferToBase64(array)
            var base64 = res.data.replace(/[\r\n]/g, "")
//后台传过来的数据可能会有空格‘/n’ 所以去掉空格再调用base64方法即可
            that.setData({ canvasimgsrc: 'data:image/png;base64,' + base64 })
            that.setData({ loading: false            })
          }
        })
        
      },

      fail: function () {
        console.log("canvas不可以生成图片")
        wx.showModal({
          title: '提示',
          content: '微信当前版本不支持，请更新到最新版本！',
          showCancel: false
        });
      },
      complete: function () {

      }
    })
    


  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    //画布初始化执行
    this.startCanvas();

  }
})