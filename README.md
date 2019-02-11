EX: 以[刀劍神域 Alicization [1A]](https://ani.gamer.com.tw/animeVideo.php?sn=10849)舉例
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
|``next()``|回傳下一集的物件，若沒有下一集回傳None|Anime('10924')|
|``previous()``|回傳上一集的物件，若沒有上一集回傳None|None|
|``series()``|回傳Series物件|Series('10849')|
|``m3u8('720p')``|回傳一個[m3u8物件](https://github.com/globocom/m3u8)，參數為解析度，預設為可用的最高解析度|(720p)|
|``m3u8s()``|回傳一個m3u8的list依序為360p,540p,720p,1080p，若不可用的為None|[(360p), (540p), (720p), None]|

# Series物件
可以用任何一集的sn
```
sao3 = Series(10849)
```
## 用法
||意義|值|
|:---:|:---:|:---:|
|`sao3.title`|系列標題|刀劍神域 Alicization|
|`sao3[0]`|第一集的Anime物件|(1A)
|`sao3['1A']`|1A的Anime物件|(同上)
|`sao3[-1]`|最後一集(最新一集)的Anime物件|(18)(目前)
|`for episode in sao3`|從第一集到最後一集|
|`len(sao3)`|總共幾集|19(目前)|
