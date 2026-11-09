---
name: photo-from-bancho
description: 将真实食物照片制作成《潜水员戴夫》COOKSTA 风格的像素手机动态，再与原照片上下拼成 3:4 打卡图。适用于“在班乔寿司打卡”、PHOTO_FROM_BANCHO 或提供食物照片并要求制作戴夫风格打卡图的请求。
license: MIT
metadata:
  version: "0.2.1"
---

# 在班乔寿司打卡（PHOTO_FROM_BANCHO）

交付一张上方实拍、下方完整模拟截图的 3:4 竖图，以及单独的模拟截图。

## 输入

- 必需一张食物照片。用户明确提供多张并希望分别处理时，逐张生成。
- 可选评论、Tags、用户名、头像和自定义 COOKSTA 截图。每个字段独立处理，用户提供的文字和用户名按原样使用，提供的头像保留人物身份。Skill 自带 15 张真实截图，默认可以只用食物照片开始。
- 可选场景（班乔主店、分店、海上）、时段（白天、傍晚、夜晚）与天气（晴、雨、雾）。各项默认分别为班乔主店、白天、晴。参考图命名和匹配规则见 [场景参考表](references/scenes.md)。
- 缺省评论用中文食客口吻，通常 20～40 字。围绕可见的摆盘、颜色或食材写，不确定的鱼种、配料、店名和味道不当作事实。Tags 用 2～4 个相关话题。
- 缺省用户名用随机短昵称，头像用原创圆形像素人像。先随机选定 100～999 的点赞数，再将其写入生成指令。

## 生成模拟截图

需要合成或拼图时，读取 [AGENT_INSTALL.md](AGENT_INSTALL.md)，检查脚本运行环境并按需安装依赖。若只需提供生成提示词，跳过 Python 准备。

检查照片，提取食物数量、形状、配料、餐具、光线和取景特征。使用当前 Agent 已配置的图像编辑工具，并遵守其调用和数据传输规则。

默认使用**精确保真模式**。按 [场景参考表](references/scenes.md) 选择用户指定或与所选组合匹配的真实截图。从用户提供的参考目录或 Skill 的 `assets/scenes/` 中查找。保留原始截图作为底图，生成手机动态素材，再按 [动态替换流程](references/feed-compositing.md) 用脚本贴回。**默认去掉截图底部的「B 关闭」及其半透明底框**。只改当前动态和关闭提示所在区域，保留原始画布尺寸、A 控件及其余像素。

缺少对应真实截图时，请用户提供底图，或在用户明确接受近似背景后按 [场景参考表](references/scenes.md) 的兜底方式生成。缺少图像工具时，可提供填好的动态生成提示词，收到生成素材后再按上述流程合成。

生成动态素材时，可以使用下方提示词并填写实际内容。

```text
Create only the COOKSTA feed patch to fit [width:height] from the game reference,
with a food illustration above a white post panel. Use [photo] for the dish and
preserve its portions, tableware and angle. Render stepped, chunky pixel art.
Use [avatar], exact username “[username]”, pink likes “[count]”, dark gray
comment “[comment]” with the requested line breaks, and blue tags “[tags]”.
Leave clear space for the original A control. Omit the phone frame, navigation,
restaurant or ocean background, and B close prompt from the patch.
```

检查料理、文字、点赞数和换行，确认独立截图和拼图中都没有「B 关闭」及其底框。比对动态区和关闭提示区之外的像素及保护区。实际交付使用脚本合成后的 PNG。

## 拼接

以下命令以 Skill 目录为当前目录。将示例中的 `python3` 换成 [环境检查](AGENT_INSTALL.md) 选定的解释器，并将输入和输出参数换成实际路径。Skill 安装目录只读时，可在工作区执行并传入脚本的绝对路径。

用 [compose.py](scripts/compose.py) 输出默认 1536×2048 的拼图。上方裁切实拍图突出主体，下方等比例缩放并完整保留模拟截图。根据主体位置调节 `--photo-position-x` 和 `--photo-position-y`，取值 0～1，分别从左到右、从上到下。

```bash
python3 scripts/compose.py --photo food.jpg --screenshot cooksta.png \
  --output photo-from-bancho-3x4.png --photo-position-y 0.5
```

打开最终图确认食物主体、截图边缘及文字完整。将成品、提示词、场景组合和所用参考图文件名存放于用户指定的本地目录或工作区的 `output/`，以新文件名保留原文件。展示最终拼图、尺寸和下载链接，可附单独的模拟截图链接。默认布局细节无需逐项提醒。
