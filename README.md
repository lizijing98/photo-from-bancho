# 在班乔寿司打卡 · PHOTO_FROM_BANCHO

`photo-from-bancho` 是一个将食物照片变成《潜水员戴夫》COOKSTA 风格像素动态的 Skill。它会导出一张 3:4 的 PNG 组合图，上方是实拍，下方是模拟截图，并单独保存模拟截图。

## 示例

| 原图 | 模拟截图 | 组合产物 |
| --- | --- | --- |
| ![eg1.jpeg](./examples/eg1.jpeg) | ![eg1-cooksta.png](./examples/eg1-cooksta.png) | ![eg1-photo-from-bancho-3x4.png](./examples/eg1-photo-from-bancho-3x4.png) |
| ![eg2.jpeg](./examples/eg2.jpeg) | ![eg2-cooksta.png](./examples/eg2-cooksta.png) | ![eg2-photo-from-bancho-3x4.png](./examples/eg2-photo-from-bancho-3x4.png) |

## 让 Agent 帮你安装

把下面的安装指令发给你的 Agent。

```text
从 https://github.com/lizijing98/photo-from-bancho/tree/main/skills/photo-from-bancho 安装完整的 photo-from-bancho Skill。按 Skill 目录里的 AGENT_INSTALL.md 的流程进行检查安装。
```

## 使用

附上一张实拍食物照片，将下面的指令发给 Agent。

```text
使用 photo-from-bancho，把这张照片做成班乔寿司打卡图。
```

可以指定配文、Tags、用户名和头像，也可以要求配文分行。未填写的字段会自动生成。想贴近某个游戏界面时，可以额外提供一张 COOKSTA 参考截图。只提供食物照片时，Skill 会根据文字布局描述制作模拟截图。

Agent 没有图像工具时，可以先获取生成提示词，再把生成好的截图交给 Agent 拼接。

## 隐私与许可

仓库中的示例照片已移除 GPS、拍摄时间和设备信息。使用在线图像工具时，照片及参考图会按该工具的规则处理。

本项目为非官方同人工作流。游戏名称、界面与美术的权利归相应权利方，用户自行提供的图片不属于本项目的许可范围。代码与文档采用 [MIT 许可](LICENSE)。
