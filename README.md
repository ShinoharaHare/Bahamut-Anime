EX: 以[刀劍神域 Alicization [1A]](https://ani.gamer.com.tw/animeVideo.php?sn=10849)舉例，sn為10849
# Anime物件

 ```
 anime = Anime(10849)
 ```
### Attributes
||意義|值|
|:---:|:---:|:---:|
| ``title`` |動漫標題|'刀劍神域 Alicization [1A]'|
| ``episode``|集數|'1A'|
| ``next_sn``|下一集的ID ('0'表示沒有)|'10924'|
| ``previous_sn``|上一集的ID ('0'表示沒有)|'0'|
### Methods
||意義|值|
|:---:|:---:|:---:|
|``next()``|回傳下一集的物件，若沒有下一集回傳None|\<Anime\>|
|``previous()``|回傳上一集的物件，若沒有上一集回傳None|None|
|``series()``|回傳一個Series物件|\<Series\>|
|``m3u8('720p')``|回傳一個[m3u8物件](https://github.com/globocom/m3u8)，參數為解析度，預設為可用的最高解析度|\<m3u8\>|
|``m3u8s()``|回傳一個dict，包含所有解析度的m3u8|{'360p': \<m3u8\>, '540p': \<m3u8\>, '720p': \<m3u8\>}

# Series物件
可以用任何一集的sn
```
sao3 = Series(10849)
```
## 用法
||意義|值|
|:---:|:---:|:---:|
|`sao3.title`|系列標題|刀劍神域 Alicization|
|`sao3[0]`|第一集的Anime物件|\<Anime\>(1A)
|`sao3['1A']`|1A的Anime物件|\<Anime\>(同上)
|`sao3[-1]`|最後一集(最新一集)的Anime物件|\<Anime\>(18)
|`for episode in sao3`|從第一集到最後一集(最新一集)|
|`len(sao3)`|總共幾集|\<Anime\>(19)|
