import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit
from PyQt5.QtCore import Qt
from Crypto.Cipher import DES3
from Crypto.Hash import MD5
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad  # 导入填充和去填充工具

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("对称加密")  # 设置窗口标题
        self.setGeometry(100, 100, 400, 300)  # 设置窗口尺寸

        layout = QVBoxLayout()  # 垂直布局

        self.label_key = QLabel("密钥：")  # 密钥标签
        self.edit_key = QLineEdit()  # 密钥输入框
        layout.addWidget(self.label_key)
        layout.addWidget(self.edit_key)

        self.label_plain_text = QLabel("明文：")  # 明文标签
        self.edit_plain_text = QTextEdit()  # 明文输入框
        layout.addWidget(self.label_plain_text)
        layout.addWidget(self.edit_plain_text)

        self.label_cipher_text = QLabel("密文：")  # 密文标签
        self.edit_cipher_text = QTextEdit()  # 密文输入框
        layout.addWidget(self.label_cipher_text)
        layout.addWidget(self.edit_cipher_text)

        self.label_decrypted_text = QLabel("解密后明文：")  # 解密后明文标签
        self.edit_decrypted_text = QTextEdit()  # 解密后明文输入框
        layout.addWidget(self.label_decrypted_text)
        layout.addWidget(self.edit_decrypted_text)

        self.button_generate_key = QPushButton("生成密钥")  # 生成密钥按钮
        self.button_generate_key.clicked.connect(self.generate_key)  # 生成密钥按钮点击事件
        layout.addWidget(self.button_generate_key)

        self.button_encrypt_text = QPushButton("加密文本")  # 加密文本按钮
        self.button_encrypt_text.clicked.connect(self.encrypt_text)  # 加密文本按钮点击事件
        layout.addWidget(self.button_encrypt_text)

        self.button_decrypt_text = QPushButton("解密文本")  # 解密文本按钮
        self.button_decrypt_text.clicked.connect(self.decrypt_text)  # 解密文本按钮点击事件
        layout.addWidget(self.button_decrypt_text)

        self.setLayout(layout)  # 设置主窗口布局为垂直布局

    def generate_key(self):  # 生成密钥的按钮点击事件方法
        key = get_random_bytes(24)  # 生成24字节的随机密钥，因为DES3的密钥是24字节
        self.edit_key.setText(key.hex())  # 转换密钥为十六进制表示，显示到密钥输入框

    def encrypt_text(self):  # 加密文本的按钮点击事件方法
        plain_text = self.edit_plain_text.toPlainText()  # 获取输入的明文
        key = bytes.fromhex(self.edit_key.text())  # 获取密钥并转换为字节类型
        key_hashed = MD5.new(key).digest()  # 使用MD5处理密钥
        
        des = DES3.new(key_hashed, DES3.MODE_ECB)  # 使用处理后的密钥创建DES3加密器对象，ECB模式
        padded_text = pad(plain_text.encode('utf-8'), DES3.block_size)  # 对明文进行填充
        cipher_text = des.encrypt(padded_text)  # 加密填充后的明文

        self.edit_cipher_text.setText(cipher_text.hex())  # 将加密的密文转换为十六进制，显示到密文输入框

    def decrypt_text(self):  # 解密文本的按钮点击事件方法
        cipher_text = bytes.fromhex(self.edit_cipher_text.toPlainText())  # 获取密文输入框的内容
        key = bytes.fromhex(self.edit_key.text())  # 获取密钥并转换为字节类型
        key_hashed = MD5.new(key).digest()  # 使用MD5处理密钥
        
        des = DES3.new(key_hashed, DES3.MODE_ECB)  # 使用处理后的密钥创建DES3解密器对象，ECB模式
        decrypted_padded_text = des.decrypt(cipher_text)  # 解密密文
        decrypted_text = unpad(decrypted_padded_text, DES3.block_size).decode('utf-8')  # 去除填充，并解码为字符串
        
        self.edit_decrypted_text.setText(decrypted_text)  # 显示解密后的明文

if __name__ == "__main__":
    app = QApplication(sys.argv)  # 创建应用程序
    window = MainWindow()  # 创建主窗口
    window.show()  # 显示主窗口
    sys.exit(app.exec_())  # 运行应用程序，并在关闭窗口后退出