王语晨
2022104842

python期末题目3
使用scrapy框架加入beautifulsoup，实现豆瓣读书（一周热门图书榜）图书信息爬取。
scrapyitem通过pipeline将图书名字、作者、图片，依次放入word文件，文件名为book.doc；
利用beautifulsoup爬取每本书书评，总结成词云图，保存在工程目录的wordcloud文件夹下。

用到的库：
爬虫相关：scrapy、beautifulsoup、urllib
文件路径：os、shutil、stat
工具：re、jieba、matplotlib、wordcloud

亮点：
1、通过继承ImagesPipeline类，并重写其中函数，实现图片的保存，实现了自定义图片名，不再是默认的哈希值，便于存取。
2、将文字图片同时保存，每生成一个item就去保存，不需要创建item列表，也突破txt文件不能保存图片的限制，利用python-word库实现。
3、读取评论生成词云图，无论这本书书评有没有10页，都可以正常爬取，如果空会返回空列表，有很强的健壮性，同时词云图可以设置停用词，可以添加进txt文档，过滤无关项，评论整体是没有保存的，但在爬取的过程中是会打印的，所以想仔细看也是完全没问题的。
4、在程序运行前清除过往的爬取记录，不会存留过时错误的信息。
5、有较高的可移植性，爬取内容保存目录不使用严格路径，无论工程目录在哪，都保存在工程目录及其子目录下，不会找不到内容。

总之，对于我这种喜欢看书的人来说，多少还有那么一点用，书荒的时候可以试试！

使用方法：
打开cmd到X:...\DoubanBook\DoubanBook
输入crapy crawl EveryWeekHotBook回车
应该就ok了

有问题可以联系作者【狗头】