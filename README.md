# StandardsDownloader
全国行业标准信息服务平台文档一键自动下载

Automation downloader for standards in national public service platform



## 如何使用

1. 打开全国标准信息公共服务平台https://std.samr.gov.cn/ ，搜索想要下载的标准名称

2. 点击标准标题查看详情，复制详情页网址：https://std.samr.gov.cn/hb/search/stdHBDetailed?id=xxx

3. 执行脚本，其后输入网址：

   ```shell
   python ./download_std.py
   > input the url: https://std.samr.gov.cn/hb/search/stdHBDetailed?id=xxx
   ```

4. 静等脚本执行完成，如果标准文档内容不可以被查看，则会打印出不可查看原因；否则标准文档会下载至脚本执行目录
