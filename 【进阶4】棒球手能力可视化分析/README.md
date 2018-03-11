【概要】</br>
1.一个包含 1,157 名棒球手的数据集</br>
2.包括他们的用手习惯（左手还是右手）、身高（英寸）、体重（磅）、击球率和全垒得分</br>
3.x轴==击球率，y轴==全垒得分，圆圈面积==体重，颜色==用手习惯，身高分组动画</br>
4.可视化目的，展现这些球手的表现差异</br>

【设计】</br>
1.数据集除姓名外包含5个属性，主要度量为击球率、全垒得分，分别编码为X、Y坐标轴</br>
2.身高由于重复数值多，转为有序维度，编码为动画选择</br>
3.用手习惯维度编码为颜色，体重维度编码为圆圈面积</br>
4.根据反馈更改可视化</br>

【反馈】</br>
1.动画效果中坐标轴原点始终存在无意义的数据点，建议删掉</br>
2.weight度量未能编码到圆圈面积</br>
3.指示器的悬浮框提示为name和height,name后的数据为计数值，建议悬浮窗提示更改为：height(上)、count(下)</br>
4.每一帧动画中建议添加改组动画的height值</br>
5.添加图表标题</br>

【资源】</br>
1.https://github.com/d3/d3/wiki/API--%E4%B8%AD%E6%96%87%E6%89%8B%E5%86%8C</br>
2.https://github.com/PMSI-AlignAlytics/dimple/wiki</br>
3.http://dimplejs.org/examples_index.html</br>
4.http://wiki.jikexueyuan.com/project/d3wiki/</br>