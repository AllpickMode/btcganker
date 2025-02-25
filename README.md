# BTCGanker

该项目是一个Python脚本，旨在生成比特币地址并检查它们是否与目标地址匹配。如果找到匹配的地址，脚本会将私钥、公钥和地址保存到文件中，并可选地发送电子邮件通知。

## 功能

- **多核支持**：利用多核CPU加速地址生成过程。
- **可配置设置**：通过`config.ini`文件配置CPU使用率、最小工作线程数和网络连接。
- **邮件通知**：在找到匹配地址或达到指定时间间隔时发送电子邮件。
- **日志记录**：将生成的密钥和地址保存到文件（`btcganker.txt`）中。

## 环境要求

- Python 3.x
- `bitcoin`库
- `smtplib`用于邮件通知
- `configparser`用于读取配置文件
- `multiprocessing`用于并行处理

## 安装步骤

1. **克隆仓库**
   
2. **安装依赖**
   - 无需安装依赖，可直接运行

3. **配置脚本**
   - 编辑`config.ini`文件以设置CPU使用率、最小工作线程数和邮件配置。
   - 在`addresses.py`文件中添加目标比特币地址。

## 配置文件

`config.ini`文件包含以下部分：

- **DEFAULT**：
  - `CPU_HALF`：设置为`True`以使用一半的CPU核心，或`False`以使用全部核心（留一个空闲）。
  - `MIN_WORKERS`：使用的最小工作线程数。
  - `ENABLE_INTERNET`：设置为`True`以启用邮件通知，或`False`以禁用。

- **EMAIL**：
  - `SMTP_SERVER`：SMTP服务器地址。
  - `SMTP_PORT`：SMTP服务器端口。
  - `SENDER_EMAIL`：发件人邮箱地址。
  - `RECEIVER_EMAIL`：收件人邮箱地址。
  - `SENDER_PASSWORD`：发件人邮箱密码。

## 使用方法

运行脚本：

```bash
python btcganker.py
```

脚本将开始生成比特币地址并检查它们是否与目标地址匹配。如果找到匹配的地址，详细信息将保存到`btcganker.txt`中，并在启用邮件通知时发送电子邮件。

## 输出内容

- **控制台输出**：
  - 显示使用的CPU核心数量。
  - 记录开始时间和目标地址数量。
  - 打印执行过程中的状态信息。

- **文件输出**：
  - 将匹配的私钥、公钥和地址保存到`btcganker.txt`中。

- **邮件输出**：
  - 如果`ENABLE_INTERNET`设置为`True`，则发送包含匹配密钥和地址的电子邮件。

## 示例 `config.ini`

```ini
[DEFAULT]
CPU_HALF = False
MIN_WORKERS = 1
ENABLE_INTERNET = True

[EMAIL]
SMTP_SERVER = smtp.example.com
SMTP_PORT = 465
SENDER_EMAIL = your-email@example.com
RECEIVER_EMAIL = receiver-email@example.com
SENDER_PASSWORD = your-email-password
```

## 示例 `addresses.py`

```python
TARGET_ADDRESSES = [
    "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
    "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy",
    # 在此添加更多目标地址
]
```

## 许可证

该项目基于MIT许可证，详情请参阅[LICENSE](LICENSE)文件。

## 免责声明

该脚本仅用于教育目的。作者不对该工具的滥用负责。使用时请自行承担风险。

## 致谢

- 感谢`bitcoin`库的开发者提供了处理比特币地址的必要工具。