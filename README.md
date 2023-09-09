# Handler
基于Mediapipe的手势控制赛车游戏程序

## 项目介绍

这是一个使用人工智能技术实现手势控制赛车游戏的项目,旨在通过手势识别技术,让用户可以用自己的手势来操控赛车,实现更自然、更沉浸的游戏体验。

## 项目功能

- 使用USB摄像头采集用户的手势图像
- 识别用户的手势类别和方向
- 根据手势生成游戏手柄指令
- 控制赛车游戏的转向、加速等动作
- 支持多种主流赛车游戏

## 项目技术

- 使用OpenCV进行图像处理
- 使用meidapipe模型,实现手势关键点识别
- 使用手指角度关系进行主要手势识别
- 使用vgamepad生成虚拟游戏手柄信号,实现游戏控制
- 使用PySide设计用户界面,提供实时反馈和参数配置

## 项目安装

- 安装Python3.8版本
- 安装`requiremens.txt`内的OpenCV、meidapipe、vgamepad、PySide2等第三方库
- 下载本项目源码
- 运行`main.py`文件

## 项目使用

- 连接USB摄像头,确保摄像头能正常工作
- 打开本项目,选择想要玩的赛车游戏
- 按照界面上的提示,做出相应的手势
- 享受游戏吧!
## 项目演示

- 手柄测试+游戏演示

[<video src="./Handler/demo/demo.mp4"></video>](https://youtu.be/EMBXtiW4zEc)

- 代码优化后游玩地平线4

【手势控制开车？手势控制翻车！深度学习手势交互项目游玩地平线4实机演示】 

https://www.bilibili.com/video/BV1r94y1s7bv/?share_source=copy_web&vd_source=60aeca39dc2529deea2a3d691853cbf7

## Todo

- [x] window端流畅运行，识别准确
- [ ] 使用mediapipe的task模型文件进行手势识别(目前Google还未支持windows端模型文件读取)
- [ ] 完善前端，增加可调节的参数
- [ ] 增加更多动作映射
- [ ] 适配macos，linux
- [ ] 适配移动端

## 项目联系

如果你对本项目有任何问题或建议,欢迎联系我们:

- 邮箱:1378198481@qq.com
- 微信:
