import os

import cv2
from PIL import Image, ImageOps, ImageFilter

# 由于转换素描图片时间过长，所以没有使用素描  等待后期完善


# 转换后视屏的存放路径
path = r"D:/pycharmproject/Video_Shift_Style/Result"

if not os.path.exists(path):
    os.makedirs(path)


# 视屏到照片(把每一帧都提取出来)
def video_to_images(videoPath):
    # 读取视频配置
    videoCapture = cv2.VideoCapture(videoPath)
    # 视屏帧的数量
    frameNumber = 0
    # 初始化开关（判断视频是否继续读取的开关）
    switch = True

    # 一帧一帧读取数据
    while switch:
        # 获取一帧的数据
        switch, frame = videoCapture.read()
        # 如果这一帧成功获取到数据
        if switch:
            # 帧数+1
            frameNumber = frameNumber + 1
            # 设置这一帧图片的保存路径
            picturePath = path + str(frameNumber) + '.jpg'
            # 这一帧图片保存
            cv2.imwrite(picturePath, frame)
            # 这一帧的图片转换成漫画
#############################################################################################
            Youhua(picturePath)
            # 删除原图片、保留漫画图
            os.remove(picturePath)
##############################################################################################
        else:
            break
    print('该视频一共有' + str(frameNumber) + '帧')
    # 释放资源
    videoCapture.release()
    cv2.destroyAllWindows()
    # 返回该视频有多少帧
    return frameNumber


# 照片到视频（把每一帧照片拼成视频）
def images_to_video(frameNumber):
    # 帧率
    fps = 15
    # 一共多少帧照片
    num_frames = frameNumber
    # 存放照片对象的数组
    img_array = []
    # 每一帧图片的宽和高
    img_height, img_width = getPicture_heightAndwidth(path + '1_Oil.jpg')
    # 循环读取图片
    for i in range(num_frames):
        filename = path + str(i + 1) + "_Oil.jpg"
        img = cv2.imread(filename)
        print('读取图片' + filename + '中....')
        # 如果图片为空
        if img is None:
            print(filename + " is non-existent!")
            continue
        # 把照片对象添加到数组中
        img_array.append(img)
    # 设置视频输出
    out = cv2.VideoWriter(path + 'CarttonVideo.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (img_width, img_height))
    # 开始图片拼接视频
    for i in range(len(img_array)):
        out.write(img_array[i])
        print('正在拼接第' + str(i + 1) + '张照片中...')

def Shuicai(picturePath):
    file_name = picturePath
    Output_FileName = picturePath.split(".")[0] + '_Oil.' + picturePath.split(".")[1]
    img_oil = cv2.imread(file_name)
    res = cv2.stylization(img_oil, sigma_s=200, sigma_r=0.6)
    cv2.imwrite(Output_FileName, res)
    # cv2.imwrite(Output_FileName, res)
    print('文件转换成漫画成功，保存在' + Output_FileName)


def Youhua(picturePath):
    file_name = picturePath
    Output_FileName = picturePath.split(".")[0] + '_Oil.' + picturePath.split(".")[1]
    img_oil = cv2.imread(file_name)
    res = cv2.xphoto.oilPainting(img_oil, 5,1)
    cv2.imwrite(Output_FileName, res)
    # cv2.imwrite(Output_FileName, res)
    print('文件转换成漫画成功，保存在' + Output_FileName)



# 照片转换成漫画风格
def Katong(picturePath):
    # 设置输入输出路径和文件名称
    imgInput_FileName = picturePath
    imgOutput_FileName = picturePath.split(".")[0] + '_Oil.' + picturePath.split(".")[1]

    # 属性设置
    num_down = 2  # 缩减像素采样的数目
    num_bilateral = 7  # 定义双边滤波的数目

    # 读取图片
    img_rgb = cv2.imread(imgInput_FileName)

    # 用高斯金字塔降低取样
    img_color = img_rgb
    for _ in range(num_down):
        img_color = cv2.pyrDown(img_color)

    # 重复使用小的双边滤波代替一个大的滤波
    for _ in range(num_bilateral):
        img_color = cv2.bilateralFilter(img_color, d=9, sigmaColor=9, sigmaSpace=7)

    # 升采样图片到原始大小
    for _ in range(num_down):
        img_color = cv2.pyrUp(img_color)

    # 转换为灰度并且使其产生中等的模糊
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    img_blur = cv2.medianBlur(img_gray, 7)

    # 检测到边缘并且增强其效果
    img_edge = cv2.adaptiveThreshold(img_blur, 255,
                                     cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY,
                                     blockSize=9,
                                     C=2)

    # 把两个照片的尺寸统一
    height = img_rgb.shape[0]
    width = img_rgb.shape[1]
    img_color = cv2.resize(img_color, (width, height))

    # 转换回彩色图像
    img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
    img_cartoon = cv2.bitwise_and(img_color, img_edge)

    # 保存转换后的图片
    cv2.imwrite(imgOutput_FileName, img_cartoon)
    print('文件转换成漫画成功，保存在' + imgOutput_FileName)


# 透明度转换 （素描转换的一部分）
def dodge(a, b, alpha):
    # alpha为图片透明度
    return min(int(a * 255 / (256 - b * alpha)), 255)


# 图片转换为素描
def Sumiao(picturePath, blur=25, alpha=1.0):
    # 设置输入输出路径和文件名称
    imgInput_FileName = picturePath
    imgOutput_FileName = picturePath.split(".")[0] + '_Oil.' + picturePath.split(".")[1]

    # 转化成ima对象
    img = Image.open(picturePath)
    # 将文件转成灰色
    img1 = img.convert('L')

    img2 = img1.copy()

    img2 = ImageOps.invert(img2)

    # 模糊度
    for i in range(blur):
        img2 = img2.filter(ImageFilter.BLUR)
    width, height = img1.size
    for x in range(width):
        for y in range(height):
            a = img1.getpixel((x, y))
            b = img2.getpixel((x, y))
            img1.putpixel((x, y), dodge(a, b, alpha))

    # 保存转换后文件
    img1.save(imgOutput_FileName)
    print('文件转换成漫画成功，保存在' + imgOutput_FileName)



# 获取图片的宽和高
def getPicture_heightAndwidth(picturePath):
    img = cv2.imread('D:\pycharmproject\Video_Shift_Style/Result1_Oil.jpg')
    # img = cv2.imread(picturePath)
    print(type(img))
    shape = img.shape
    # height width
    return shape[0], shape[1]


# 去除不需要的图片 只留下视屏
def deleteSomeFile(frameNumber):
    for i in range(frameNumber):
        print('正在删除第' + str(i+1) + '张照片')
        os.remove(path + str(i + 1) + "_oil.jpg")


if __name__ == '__main__':
    videoPath = input('输入视频路径：')
    frameNumber = video_to_images(videoPath)
    images_to_video(frameNumber)
    deleteSomeFile(frameNumber)
    print('视屏转换完成，该视频在'+path+'文件夹下面')