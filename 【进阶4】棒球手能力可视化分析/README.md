﻿#  D3.js可视化项目

## 概要
1. 一个包含 1,157 名棒球手的数据集
2. 包括他们的用手习惯（左手还是右手）、身高（英寸）、体重（磅）、击球率和全垒得分
3. x轴==击球率，y轴==全垒得分，圆圈面积==体重，颜色==用手习惯，身高分组动画
4. 可视化目的，展现这些球手的表现差异

## 设计
1. 数据集除姓名外包含5个属性，主要度量为击球率、全垒得分，分别编码为X、Y坐标轴
2. 身高由于重复数值多，转为有序维度，编码为动画选择
3. 用手习惯维度编码为颜色，体重维度编码为圆圈面积
4. 根据反馈更改可视化

## 反馈
1. 删掉动画效果中坐标轴原点始终存在无意义的数据点
2. weight度量未能编码到圆圈面积
3. 指示器的悬浮框提示为name和height,name后的数据为计数值，建议悬浮窗提示更改为：height(上)、count(下)
4. 每一帧动画中建议添加改组动画的height值
5. 添加图表标题

## 资源
- http://dimplejs.org/advanced_examples_viewer.html?id=advanced_storyboard_control
- https://github.com/d3/d3/wiki/API--%E4%B8%AD%E6%96%87%E6%89%8B%E5%86%8C
- https://github.com/PMSI-AlignAlytics/dimple/wiki
- http://dimplejs.org/examples_index.html
- http://wiki.jikexueyuan.com/project/d3wiki/