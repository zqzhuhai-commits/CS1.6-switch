# 反恐精英 CS 1.6 — Switch 测试包

![CS 1.6 图标](artwork/CS-1.6-icon.jpg)

基于用户提供的 CS 1.6 数据文件和已发布的 Xash3D Switch CS 引擎整理。包含 Switch NRO 客户端、NSP 前端、手柄配置和本地机器人对战配置。

**状态：v0.1.0-test。尚未经过 Switch 真机验证。** 这是旧版引擎的资源适配与打包，不是重新编写或完成真机验证的全新移植。

## 下载

- [完整客户端与 NSP 测试包](https://github.com/zqzhuhai-commits/CS1.6-switch/releases/tag/v0.1.0-test)
- [单独下载 NSP 前端](https://github.com/zqzhuhai-commits/CS1.6-switch/raw/refs/heads/main/binaries/Counter-Strike-CS-1.6-Forwarder.nsp)
- [单独下载 NRO](https://github.com/zqzhuhai-commits/CS1.6-switch/raw/refs/heads/main/binaries/xash3d-cstrike.nro)

NSP 已嵌入新制作的黑金 CS 1.6 图标；原图及 256×256 JPEG 见 `artwork/`。

NSP 显示名称：**反恐精英 CS 1.6**。标题 ID：`0100c516a0160000`。

## 安装

1. 下载完整包，把“SD卡根目录”中的 `switch` 和 `xash3d` 文件夹复制到 SD 卡根目录。已有同名目录请先备份配置。
2. 安装包内 `NSP前端/Counter-Strike-CS-1.6-Forwarder.nsp`，从主菜单图标启动。
3. 前端固定加载 `sdmc:/switch/xash3d-cstrike.nro`；资源放在 `/xash3d/cstrike` 和 `/xash3d/valve`，不要移动或重命名入口。
4. 如前端无法启动，可按住 R 打开已安装游戏，进入完整内存 hbmenu，直接运行 NRO，对比排查。避免使用相册 Applet 模式测试。

NSP 只是启动入口，单独安装 NSP 不包含客户端与游戏数据。

## 本地对战

创建局域网游戏，选择 `de_dust2`，进入地图后选择队伍。

减号打开控制台，输入：

```text
exec switch_offline.cfg
```

机器人命令：`bot_quota 7`；清除机器人：`bot_quota 0`。引擎内含机器人相关命令，但实际进入地图和机器人行为仍需真机验证。

## 手柄配置

| 按键 | 功能 |
| --- | --- |
| 左/右摇杆 | 移动/视角，沿用引擎原生控制 |
| ZR / ZL | 射击/副攻击 |
| L / R | 蹲下/换弹 |
| 左摇杆按下 | 慢走 |
| A / B | 购买/跳跃 |
| X / Y | 切上把武器/使用 |
| 方向上/下 | 自动购买/重复购买 |
| 方向左/右 | 切武器 |
| 加号/减号 | 菜单/控制台 |

数字购买菜单与队伍菜单可能需要触屏、屏幕键盘或 USB 键盘；便捷手柄数字菜单尚未实现。

## 已检查与待验证

已检查原始 ZIP CRC、生成 ZIP CRC、NRO/ASET/NACP 结构、NSP 的 PFS0/NCA 结构、NCA 文件摘要、标题 ID、显示名称和 NRO 路径。

尚未验证：Switch 实际启动、NSP 安装与跳转、地图加载、机器人、手柄、中文字库、帧率及联网。旧引擎与最新系统、公网服务器的兼容性不作保证。

原包内的 Linux ARM64 引擎、YaPB、AMX Mod X、Metamod、Windows DLL 不参与运行；地图、模型、声音及中文资源予以保留。使用 Switch 专用静态内置客户端和游戏逻辑。NRO 基于 `switchports/xash3d-switch v1.0.1`，仅修改 NACP 显示名称。

## 完整包的分卷备份

GitHub 对单个 Git 文件大小有限制，完整 ZIP 以分卷保存在 `package-parts/`。正常使用请优先下载 Releases 的完整 ZIP。

如需要从源码仓库重建下载包：

```sh
python3 scripts/assemble_package.py
```

脚本会验证每个分卷及完整 ZIP 的 SHA-256，输出 `CS16-Switch-v0.1.0-test.zip`。

## 排错

提交问题时附上固件、Atmosphere 版本、启动方式、出现问题的步骤，以及 `/xash3d` 下的日志（如 `xash.log`）。

## 来源与许可

- [Switch 引擎 v1.0.1](https://github.com/switchports/xash3d-switch/releases/tag/v1.0.1)
- [对应引擎源代码](https://github.com/switchports/xash3d-switch/tree/v1.0.1)，GPLv3，完整许可证见 `licenses/`。
- [Switch 安装指南](https://github.com/switchports/xash3d-switch/wiki/Installation-guide)
- [菜单资源 Xash Extras v0.19.2](https://github.com/FWGS/xash-extras/releases/tag/v0.19.2)
- [NSP 前端加载器](https://github.com/TooTallNate/switch-nsp-forwarder/tree/main/romfs/template/exefs)
- [hacBrewPack](https://github.com/rlaphoenix/hacBrewPack)

Counter-Strike、Half-Life 及其商标、游戏资源版权归原权利人所有。本包使用用户提供的资源；本仓库的配置与打包说明不改变原文件许可。本仓库未包含打包密钥。
