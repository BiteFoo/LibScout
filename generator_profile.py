#coding:utf-8
import os


def iter_file(p:str)->str:
    for root,_,fs in os.walk(p):
        for f in fs:
            if f == "library.xml":
                yield os.path.join(root,f)

def generate_profile(p:str):
    """
    如果我们使用 -m 则不会输出执行成的日志，去掉-m 则会给出相关日志
    :param p:
    :return:
    """
    for f in iter_file(p):
        cmd = f"java -jar .\\build\\libs\\LibScout.jar -o profile -m   -a D:\\Android\sdk\\platforms\\android-31\\android.jar -x \"{f}\"  \"{os.path.dirname(f)}\""
        print(f"=> cmd : {cmd}")
        os.system(cmd)
        # break


if __name__ == "__main__":
    p = r"D:\CodeDocument\android_sdk_scraper\download-lib-repos"
    generate_profile(p)


