# MusicBox Tape Generator
## 由MIDI文件或EMID文件生成音乐盒子纸带图谱



现支持以下功能：

- 生成30音或15音的纸带图谱（需更改`exportpics`中`is_30_note`参数来切换）
- 生成图片添加音名标识（蓝色标记，排版有待改善）
- 生成图片添加小节标识（每栏右侧）
- 生成图片自动标记孔位数量统计，默认每100个孔统计并显示一次
- 生成图片自动添加水印
- 生成图片自动高亮没有落在网格线交点上的孔位（默认用粉红色标记）
- 在生成的最后一张图片的最后一栏下方显示孔位和纸带长度统计（分别默认用青色和亮黄色标记）



Python编写的程序，用于.emid与.mid文件的互相转换，以及生成纸带设计稿图片

需要`Pillow, mido`模块以及`libraqm.dll`动态链接库



个人B站：[Alex的八音盒](https://space.bilibili.com/1507877086)

致谢原作者：@[BiologyHazard](https://github.com/BiologyHazard)

原项目地址：https://github.com/BiologyHazard/MusicBoxDesigner

