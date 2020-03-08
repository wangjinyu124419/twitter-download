# twitter-media
借助三个开源库完成某个twitter 用户的图片和视频的下载，
可以一次性下载你关注的所有用户，或者单独下载某个用户的
三个开源库如下：
twint：爬取所有twitter文
you-get下载推特视频，不过有时候you-get会下载失败，不过多线程速度快
twitter-video-downloader：也是下载视频，you-get失败时调用这个，成功非常高，而且视频质量更好，但是速度慢，目前社单线程的，调用cpu合成很耗资源）
