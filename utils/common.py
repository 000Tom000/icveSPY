import qrcode


def show_qrcode(url: str = None):
    # url = "https://sso.icve.com.cn/weChatScanningCode?sceneId=7f9df7aa158048fea72e11ae4ba41e40&t=1792980838615"
    qr = qrcode.QRCode(
        version=None,  # 自动选择二维码大小
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,  # 每个小方块的像素大小
        border=4  # 二维码边框
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    import matplotlib.pyplot as plt
    plt.imshow(img, cmap="gray")
    plt.axis("off")  # 隐藏坐标轴
    plt.show()