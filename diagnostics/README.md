反恐精英 CS 1.6 — 独立目录日志诊断版

本次修改
NRO：/switch/CS16/xash3d-cstrike.nro
日志：/switch/CS16/logs/CS16-debug.log
NSP：仍显示“反恐精英 CS 1.6”，标题 ID 0100c516a0160000，版本 1.0.1。
游戏资源继续读取 /xash3d/cstrike 和 /xash3d/valve，不需要移动游戏资源。

安装
1. 将原来的 /switch/xash3d-cstrike.nro 备份至电脑后移走。
2. 将本包“SD卡根目录”内的 switch 文件夹复制到 SD 卡根目录。
3. 重新安装本包“NSP前端”中的 Counter-Strike-CS-1.6-Forwarder.nsp。
   此前的前端仍指向旧路径，移动 NRO 后必须更新 NSP；标题 ID 相同。
4. 启动“反恐精英 CS 1.6”，复现一次闪退。
5. 把 /switch/CS16/logs/CS16-debug.log 发来。

也可按住 R 打开已安装游戏，进入完整内存 hbmenu，然后打开 CS16 文件夹运行 NRO。
无需从相册 Applet 模式启动。

诊断范围
本包仅增加日志记录和调整入口路径，不代表闪退已经修复。
日志在引擎每次文字输出后通过 fopen(追加)、fwrite、fclose 记录。
已通过 ARM64 指令模拟检查、文件打开失败分支检查、NRO/NSP 结构和路径检查、ZIP CRC 检查。
模拟中的文件操作是接口模拟；尚未在 Switch 上验证实际 SD 卡写入、NSP 跳转和游戏运行。
如果引擎首次文字输出前已退出，或 SD 卡无法写入，仍可能没有日志。
如果没有日志，请发启动到退出的视频或错误照片，并注明从 NSP 还是 hbmenu 启动。

恢复旧版
恢复此前的原 NRO 与原 NSP，并使用旧版的入口路径即可。

源码和许可
诊断补丁生成脚本、模拟检查脚本及 GPLv3 许可证见“诊断补丁源码”。
引擎源代码：https://github.com/switchports/xash3d-switch/tree/v1.0.1
