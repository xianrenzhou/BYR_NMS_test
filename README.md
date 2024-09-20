# BYR_NMS_test
## 说明

只使用了request 和time库

直接运行main.py即可

## 运行结果

![image-20240920150509669](https://r2img.xianrenzhou.top/pics/2024/09/12db05f9581d298f6e5481e351002f5a.png)

![image-20240920182646615](https://r2img.xianrenzhou.top/pics/2024/09/3021fbf96ee75a6760948c06b018c96b.png)

## NMS进阶题思路
1.状态是随机的，如果需要百分百保活，肯定不是用心跳api



2.token过期后，返回jwt无效或过期



3.搜索一下jwt可知，jwt是JSON Web Token，可以通过某种算法算出来



4.百度 jwt 解密网站，把程序给的jwt放进去，发现变化的只有时间戳



5.改下时间戳，测试，不通过，再看jwt定义，发现还需要一个secret key



6.找半天发现secretkey是启动命令的Hello_new_Byrs_1234123412341234，再次改时间戳，通过
