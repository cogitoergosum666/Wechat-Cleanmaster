from distutils import filelist
import os
import time
import shutil

import platform
from progress.bar import Bar





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
    for name in filelist:

        #print(os.listdir())
        os.chdir(name)
        subfilelist = os.listdir('.')

        if 'File' not in subfilelist:
            os.chdir('..')
            
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
            os.system('rd '+ name + '/S /Q')
        bar.next()
    bar.finish()
    return filedest,filecount


if __name__ == '__main__':
    print("微信缓存要你命1000系统已经启动，鲨！")
    print("本脚本还在测试阶段，请谨慎使用")
    msgattach_dir = input("请键入微信msgattach路径，如缺省则默认本文件已经在msgattach目录下")
    filedest,filecount = work(msgattach_dir)
    print(str(filecount) + "个文件已经存入当前目录下"+filedest+"文件夹，其余项目清理完毕")