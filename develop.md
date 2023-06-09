# Develop Doc
1、scraper module: 一个爬虫模块，用来下载仓库的jar\aar  
2、profile module :生成profile 用于标识不同atk版本
```sh
使用scripts 下的library-scraper.py下载jar或者aar
使用library-generator.sh 生成profile文件
```

3、match module: 对目标app进行对比并输出检测结果
```sh
#结果将保存在results/pkgname/results.json
java -jar build/libs/atk.jar -o  match  -a /home/loopher/android-sdk/platforms/android-30/android.jar -p ./LibScout-Profiles/  bb.apk -j results
```

4、lib_api_analysis  module: 重新分析下载的jar/aar的变更  --j 保存结果到json文件

```sh
java -jar build/libs/atk.jar  -o lib_api_analysis -a /home/loopher/android-sdk/platforms/android-30/android.jar -j sdk_profiles scripts/my-lib-repo/

```
5、updatability module : 更新变更的结果 使用这个模式，我们需要指定lib_api_analysis模块生成的数据
6、目前重写了下载libs的程序可以加速下载，同时预先处理了下载过的libs ![ATKScraper](https://github.com/BiteFoo/ATKScraper)
7、通过执行`generator_profile.py` 来执行命令进行预处理profile信息，保存到`./profile/`

由于在执行profile的时候很吃内存，目前仅使用个执行生成，如果机器配置够好，考虑将gengerator内设置成多线程模式执行密令。

## 测试
使用`./gradlew build` 进行编译出来jar文件
### 测试识别App
查看3
### 测试生成profile
查看`gerator_profile.py`，需要注意的是，有些下载的`aar`内部使用的是`class.jar`文件来加载核心的库，实际保存的是在`libs/xxx.jar` 例如`jpush` 的
就是这样，因此我单独写了一个程序来处理这个问题，将aar内部的核心jar导出来，同时保存`aar`为`zip`文件，脚本如下
```python
#coding:utf-8

import os
import zipfile 


def iter_files(p:str)->str:
	for root,_,fs in os.walk(p):
		for f in fs:
			# print(f)
			if f.endswith(".aar") or  f.endswith(".jar"):
				yield os.path.join(root,f)

def export_android_jar(p:str):
	# print("->export ",p)
	ok = False 
	with zipfile.ZipFile(p) as zout:
		for name in zout.namelist():
			if "class.jar" != name and name.endswith(".jar"):
				save = p.replace(".aar",".jar")
				if os.path.isfile(save):
					continue
				with open(save,'wb') as fp:
					fp.write(zout.read(name))
					ok =True 
					print("-> save successed: ",save)
	if ok:
		os.rename(p,p.replace(".aar",".zip"))


print("--< start")
p = "/path/to/download-lib-repos/jpush"
for f in  iter_files(p):
	export_android_jar(f)
```
