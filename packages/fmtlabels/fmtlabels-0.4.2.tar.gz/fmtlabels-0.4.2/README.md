# 情感分析结果标注格式转换

这个工具将情感分析结果标注的格式从CSV转换为JSON。输出格式依照[标注规范](http://aiwiki.yimian.com.cn/labelling/standard.html)

## 安装：

	pip3 install .
	
## 使用格式：

    #fmtcsv会剔除重复的样本
	fmtcsv <category> 1.csv 2.csv ...

	#fmtlines用于流水线处理数据，不会剔除重复的样本
	fmtlines <category> 1.txt

结果输出到stdout
