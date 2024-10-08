# Proactive-Sales-Agent
[English](README.md)

实验性项目：为大模型销售代理引入**时间观念** ，促使它能根据时间流逝的情况和用户**主动交谈**。 作为长期项目，目标是构建和人一模一样的销售代理，项目起点是[ShampooSalesAgent](https://github.com/jackfsuia/ShampooSalesAgent)。

演示:

<p align="center"><img src="images/proactive talk.png" width="100%" ></p>

## 使用
把你申请的API key写入[api-config.json](models/api-config.json). 然后运行
```
python app.py
```
## 原理
每过一段时间就提醒大模型销售现在离上次客户讲话已经过去了多久，让大模型自己决定要不要主动说些话。
## 结果
仍在改进中。目前只能完成简单效果，比如它会主动提醒你它已经等了你多久，假如你提前告诉它让他等你几分钟的话。
## 未来方向
- 微调让其掌握时间观念。
