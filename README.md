# Novel word frequency analysis, word cloud graph and character social relationship network graph
 基于任意小说词云图与关系网络图构建
通过jieba分词，wordcloud和networkx，实现词频分析和人物社交关系，并将结果展示为词云图和社交关系网络图，此方法成熟后可以加入图书馆电子信息系统，作用于任意一本小说，便于读者快速建立小说初印象。

/***
首先利用word_freq得到小说词频，基于此添加主要人物名字（name)，同一人物不同称呼(same_word函数)，额外虚词（stop_words.txt)
配置好后，运行所有main函数，导出词频统计，词云图，画出人物关系网络图
此外可以通过主程序中的configure设置图像大小，颜色，线条和点等参数