---
name: photo-from-bancho
description: 将真实食物照片制作成《潜水员戴夫》COOKSTA 风格的像素手机动态，再与原照片上下拼成 3:4 打卡图。适用于“在班乔寿司打卡”、PHOTO_FROM_BANCHO 或提供食物照片并要求制作戴夫风格打卡图的请求。
license: MIT
metadata:
  version: "0.1.0"
---

# 在班乔寿司打卡（PHOTO_FROM_BANCHO）

交付一张上方实拍、下方完整模拟截图的 3:4 竖图，以及单独的模拟截图。

## 输入

- 必需一张食物照片。用户明确提供多张并希望分别处理时，逐张生成。
- 可选评论、Tags、用户名、头像和 COOKSTA 参考截图。每个字段独立处理，用户提供的文字和用户名按原样使用，提供的头像保留人物身份。
- 缺省评论用中文食客口吻，通常 20～40 字。围绕可见的摆盘、颜色或食材写，不确定的鱼种、配料、店名和味道不当作事实。Tags 用 2～4 个相关话题。
- 缺省用户名用随机短昵称，头像用原创圆形像素人像。先随机选定 100～999 的点赞数，再将其写入生成指令。

## 生成模拟截图

需要裁切或拼图时，读取 [AGENT_INSTALL.md](AGENT_INSTALL.md)，检查脚本运行环境并按需安装依赖。若只需提供生成提示词，跳过 Python 准备。

检查照片，提取食物数量、形状、配料、餐具、光线和取景特征。使用当前 Agent 已配置的图像编辑工具，并遵守其调用和数据传输规则。

- **有用户提供的参考截图**：将它作为编辑目标，食物照片只作料理内容参考。保留参考的布局，以照片中的料理替换原动态插图。
- **只有食物照片**：用照片作料理内容参考，按下方描述生成完整的 COOKSTA 风格模拟截图。此模式的布局由图像工具按描述绘制。
- **环境缺少可用的图像工具**：输出已填写的生成提示词。用户提供生成好的模拟截图后，从裁切和拼接继续。用户已提供可用截图时，可直接执行拼接。不要自行切换付费服务。

将以下布局描述与观察结果、动态字段一起写入提示词。提供参考截图或头像时，明确指出每张图片的用途。

```text
Create a landscape COOKSTA-style game screenshot, roughly 16:9. Set a centered
dark portrait phone over a softly blurred seaside sushi restaurant with a wooden
counter, tropical foliage, and a small hanging pufferfish charm beside the phone.
Use a pink COOKSTA header with 时间线 / 升级 / 我的信息 tabs, a large landscape food
image, and a white social post panel below it.
Inside the food image, depict [visible dish, arrangement, tableware and angle
from the photo]. Preserve the food identity and portion count. Use deliberately
clustered square pixels, stepped silhouettes, limited color ramps and blocky
highlights. Keep the phone text readable.
Post panel: round pixel avatar [description or provided reference], exact
username “[username]”, pink likes “[count]” and small A prompt. Set the comment
“[comment]” in dark gray and “[tags]” in light blue on a separate line below it.
Use requested line breaks and leave comfortable white space. The white panel
continues to the screenshot bottom. Remove the entire B 关闭 overlay, including
its icon and backing. No extra text or watermark.
```

检查料理与实拍是否对应，评论、用户名、点赞数、Tags 和换行是否准确。确认手机、挂件及餐厅构图完整，且没有「B 关闭」提示。发现明显错误时局部修正并复查。

## 裁切与拼接

以下命令以 Skill 目录为当前目录。将示例中的 `python3` 换成 [环境检查](AGENT_INSTALL.md) 选定的解释器，并将输入和输出参数换成实际路径。Skill 安装目录只读时，可在工作区执行并传入脚本的绝对路径。

若白色动态区下方仍有暗色屏幕条或间距，用 [trim_screenshot.py](scripts/trim_screenshot.py) 在白色面板下边缘裁切。根据当前图确定结束行，`--bottom` 不包含该行。面板已到截图底边时直接使用原图。

```bash
python3 scripts/trim_screenshot.py --input cooksta.png --bottom 903 --output cooksta-trimmed.png
```

上例的 903 仅用于说明参数。用 [compose.py](scripts/compose.py) 输出默认 1536×2048 的拼图。上方裁切实拍图突出主体，下方完整保留裁齐后的截图并等比例缩放。根据主体位置调节 `--photo-position-x` 和 `--photo-position-y`，取值 0～1，分别从左到右、从上到下。

```bash
python3 scripts/compose.py --photo food.jpg --screenshot cooksta-trimmed.png \
  --output photo-from-bancho-3x4.png --photo-position-y 0.5
```

打开最终图确认食物主体、截图边缘及文字完整。将成品与提示词记录存放于用户指定的本地目录或工作区的 `output/`，以新文件名保留原文件。展示最终拼图、尺寸和下载链接，可附单独的模拟截图链接。默认布局细节无需逐项提醒。
