# whenconnect

[![PyPI version](https://badge.fury.io/py/whenconnect.svg)](https://badge.fury.io/py/whenconnect)


> when your android connected, do sth :)

## What For

提供一个简洁方便的方案以解决设备连接上电脑时的初始化工作，例如安装应用、启动应用，或是定制任何你希望的。

## Usage

如果你希望，在设备123456F成功连接电脑后执行函数A，你只需要：

```python
from whenconnect import when_connect, start_detect


def A(device):
    print('call function A', device)


# 开始监听
start_detect()

# 事件注册
when_connect(device=['123456F'], do=A)
```

这样做之后，在你的程序执行时whenconnect将会同步检测123456F是否已经连接上，如果连接上，将把设备ID传入函数A并执行它：

```bash
call function A 123456F
```

当然，你也可以选择响应所有设备：

```python
when_connect(device='any', do=A)
```

这样做之后，一旦新增了android设备都会执行函数A。

- 生命周期与你的程序保持一致
- 如果你的程序结束了，监听也将不再进行

如果你只是单纯希望它单独作为一个长期的监听模块存在，只需要让你的程序保持工作即可：

- 在末尾加入死循环
- 嵌入到服务器
- `...`

## API

See `whenconnect/api.py` for detail.

## Install

Only tested on python3.

```
pip install whenconnect
```

## License

MIT
