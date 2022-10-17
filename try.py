from distutils import filelist
import os
import time
import shutil

import platform
from progress.bar import Bar

'''
文件夹计算大小函数参考了：https://blog.csdn.net/w55100/article/details/92081182
'''
def getdirsize(dir):
   size = 0
   for root, dirs, files in os.walk(dir):
      size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
   return size
 
#dirpath = '/aaa/bbb/'
# sz = getdirsize(dirpath)
# print(sz)

def checksize(filename,returnvalue = 'mb'):
    current_path = os.getcwd()
    file_path = os.path.join(current_path,filename)
    size_byte = getdirsize(file_path)#os.path.getsize(file_path)
    size_kb = size_byte/1024
    size_mb = size_kb/1024
    size_gb = size_mb/1024
    if returnvalue == 'mb':#预备了不同的输出接口
        return size_mb,'MB'
    elif returnvalue == 'byte':
        return size_byte,'B'
    elif returnvalue == 'kb':
        return size_kb,'KB'
    elif returnvalue == 'gb':
        return size_gb,'GB'


def work(Msgattach_dir = None):
    if Msgattach_dir != None:
        os.chdir(Msgattach_dir)
    print("当前python版本是" + str(platform.python_version()))
    fileList_unfilter=os.listdir('.')
    filelist = []
    for name in fileList_unfilter:
        if len(name) >30: #避免把非微信缓存文件夹也鲨了
            filelist.append(name)
    time1 = time.localtime()

    filedest = 'File_'+ time.strftime("%Y-%m-%d",time1)
    filecount = 0
    bar = Bar('Processing',max = len(filelist))
    try:
        os.mkdir(filedest)
    except:
        pass
    sizecount = 0
    for name in filelist:

        #print(os.listdir())
        os.chdir(name)
        subfilelist = os.listdir('.')

        if 'File' not in subfilelist:
            os.chdir('..')
            sizecount += checksize(name)[0]
            os.system('rd '+ name + '/S /Q')
            #os.remove(name)
        else:
            os.chdir('File')
            file_received_files_list = os.listdir()
            for datefile in file_received_files_list:
                os.chdir(datefile)
                file_received_list = os.listdir() #日期文件夹里面
                if len(file_received_list) != 0: #如果里面有文件
                    for file in file_received_list:
                        if os.path.exists('../../../'+filedest):
                            time.sleep(1)#避免运行过快重名
                            name1 = file.split('.')[0] + time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime()) + '.'+ file.split('.')[-1]
                            os.rename(file,name1)
                        shutil.move(name1,'../../../'+filedest)#假如已经存在则...
                        filecount += 1
                os.chdir('..')
            os.chdir('../..')
            #print(os.listdir())
            sizecount += checksize(name)[0]
            os.system('rd '+ name + '/S /Q')
        bar.next()
    bar.finish()
    return filedest,filecount,sizecount


if __name__ == '__main__':
    print("微信缓存要你命1500系统已经启动，鲨！")
    print("本脚本还在测试阶段，请谨慎使用")
    msgattach_dir = input("请键入微信msgattach路径，如缺省则默认本文件已经在msgattach目录下：")
    filedest,filecount,sizecount = work(msgattach_dir)
    print(str(filecount) + "个文件已经存入当前目录下"+filedest+"文件夹，其余项目清理完毕,共清理{:.3f}MB大小的空间".format(sizecount))