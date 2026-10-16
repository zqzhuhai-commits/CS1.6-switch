> **最新真机反馈（2026-10-16）**：方案 01、02、03 都未消除花屏；`r_drawentities 0` 后不再花屏。新增 [实体渲染隔离测试地图 04](CS16-Switch-HappyValley-Entity-Test04.zip)（[说明](04-solid-entities/README.md)）。新增独立地图 `happyvalley_lt_solid`，保留所有几何和贴图，改用普通不透明实体绘制；这是隔离测试，效果待验证。测试时务必恢复 `r_drawentities 1`。

> **2026-10-16 真机反馈**：方案 01 和 02 在 `happyvalley_lt.bsp`、`happyvalley_lt_fix.bsp` 上仍花屏。新增 [地图纹理兼容测试 03](CS16-Switch-HappyValley-Texture-Test03.zip)（[说明](03-pot-textures/README.md)），只关闭 NPOT 纹理支持，效果待验证。以下 01、02 保留作排查记录。

# 反恐精英 CS 1.6：地图花屏兼容性测试

适用于用户新提供、能运行的 Xash3D FWGS 0.20 Switch 包，游戏目录为 `/switch/CS16/`。这是定位渲染问题的配置测试，尚未经过 Switch 真机验证，不能保证消除花屏。

## 安装与比较

1. 完全退出游戏。先自行备份 SD 卡上的 `/switch/CS16/cstrike/opengl.cfg`。
2. 将 `01-sync` 内的 `switch` 文件夹复制到 SD 卡根目录，覆盖同名配置。重新启动游戏，在视频中的同一地图、同一位置转动视角测试。
3. 如果仍花屏，完全退出，将 `02-single-texture` 内的 `switch` 文件夹复制到 SD 卡根目录，覆盖配置后重新启动，再比较同一位置。
4. 同时测试 `de_dust2`，记录两张地图在原配置、方案 1、方案 2 下是否异常，以及帧率是否明显下降。
5. 回退时优先恢复你自己的备份。`rollback` 提供的是所提交参考 ZIP 中的原始配置；复制其中的 `switch` 到 SD 卡根目录并重新启动即可恢复该参考配置。

每次只复制一份方案。不要把整个测试包一起覆盖到 SD 卡。

| 方案 | 相对参考配置的变化 | 目的 |
| --- | --- | --- |
| 01-sync | `gl_finish 0` → `1` | 测试帧间 GPU 工作同步是否影响异常；可能降低帧率 |
| 02-single-texture | 在方案 1 基础上，`gl_arb_multitexture 1` → `0` | 进一步测试多重纹理路径是否相关；画面或性能可能变化 |
| rollback | 参考包原始 `opengl.cfg` | 回退 |

补丁只包含 `opengl.cfg`，无需重装 NSP。保持现有 NRO、动态库、游戏数据和手柄配置。没有加入旧引擎的二进制日志补丁。

## 视频与静态检查结论

视频可见建筑表面随视角出现异常图案，部分表面间歇消失；武器和 HUD 大体稳定。这支持优先调查地图绘制、纹理状态或深度问题，但不能从视频确定具体原因。

参考 ZIP 全包 CRC 检查通过。719 张 CS BSP 的贴图目录检查未发现无效的内嵌 mipmap；其中 16 张自定义地图存在未找到的外部贴图，需要另行区分。文件完整性检查通过并不代表渲染正确。

参考渲染器的 `gl_vbo` 默认值是 0，参考配置也未显式启用它，因此没有把问题归因于“默认开启 VBO”。两个方案均使用引擎现有配置项，没有修改地图或引擎二进制。

当前上游代码中 `engine/client/dll_int/ref_common.c` 会在初始化视频时执行渲染器配置，`ref/gl/gl_rmain.c` 的 `R_RenderFrame` 在 `gl_finish` 开启时调用 `glFinish`，`ref/gl/gl_opengl.c` 检查 `gl_arb_multitexture`。参考包是 `8366800a-dirty` 自定义构建；当前上游代码只用于理解相关行为，不能替代该构建的真机测试。

请反馈实际地图文件名（地图选择界面的名称或控制台中的 `.bsp` 名称）、三个配置的结果及启动方式。只有方案 1 改善时，应优先保留方案 1；若两个方案都无效，应回退，继续调查地图与渲染器，避免长期沿用无效设置。

上游参考：https://github.com/FWGS/xash3d-fwgs
