'''
監看近 dmp ftp 近 24 小時的檔案是否有缺少

'''
from ftplib import FTP
from datetime import datetime, timedelta
import lineTool

def main():
    try:
        check()
    except Exception as e:
        print(str(e))
        print('舊誤發生，進行通知')
        lineTool.lineNotify('xxx', str(e))


def check():

    checkList = []
    for i in range(0, 25):
        dt = datetime.now() - timedelta(hours=i)
        checkList.append(f'eitc_bundle_{dt.strftime("%Y-%m-%d_%H")}.zip')


    ftp = FTP(host='xxx', user='xxx', passwd='xxx')
    for filedata in ftp.mlsd():
        filename, meta = filedata
        if not meta.get("type") == "file":
            continue

        if filename in checkList:
            fileSize = ftp.size(filename)
            if fileSize < 1000000:
                raise Exception(f'{filename} 僅 {fileSize} bytes，檔案過小異常')

            # 檢驗正常，移除檢查清單
            print(f'{filename} 檢查正常')
            checkList.remove(filename)

    if len(checkList) > 0:
        raise Exception(f'ftp 資料缺少 !  {checkList}')

    print('正常結束')
    ftp.quit()



if __name__ == '__main__':
    main()
