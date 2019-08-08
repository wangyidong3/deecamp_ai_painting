// miniprogram/pages/savedCartoon/savedCartoon.js
Page({

  /**
   * Page initial data
   */
  data: {
    
  },

  /**
   * Lifecycle function--Called when page load
   */
  onLoad: function (options) {

  },

  back: function(){
    wx.navigateBack()
  },

  share: function (){
    wx.showToast({
      title: '请点击右上角分享按钮。',
      icon: 'none',
      duration: 2000//持续的时间
    })
  },

  album: function(){
    //把图片保存到相册里
    // get imge from prevous page.
    wx.saveImageToPhotosAlbum({
      filePath: "./101.jpg",
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
  },
  /**
   * Lifecycle function--Called when page is initially rendered
   */
  onReady: function () {

  },

  /**
   * Lifecycle function--Called when page show
   */
  onShow: function () {

  },

  /**
   * Lifecycle function--Called when page hide
   */
  onHide: function () {

  },

  /**
   * Lifecycle function--Called when page unload
   */
  onUnload: function () {

  },

  /**
   * Page event handler function--Called when user drop down
   */
  onPullDownRefresh: function () {

  },

  /**
   * Called when page reach bottom
   */
  onReachBottom: function () {

  },

  /**
   * Called when user click on the top right corner to share
   */
  onShareAppMessage: function () {

  }

})