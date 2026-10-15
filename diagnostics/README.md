反恐精英 CS 1.6 — 输出日志诊断包

用途
本包用于排查没有生成日志的启动闪退，仅增加引擎文字输出的文件记录。
不是已确认修复闪退的版本，也尚未经过 Switch 真机测试。

安装
1. 先备份 SD 卡原文件 /switch/xash3d-cstrike.nro，例如改名为 xash3d-cstrike-original.nro.bak。
2. 将本包“SD卡根目录”内的 switch 文件夹复制到 SD 卡根目录，覆盖同名 NRO。
3. 保留之前安装的 NSP，无需重装前端；也保留 /xash3d 游戏资源。
4. 再次启动“反恐精英 CS 1.6”，复现一次退出。
5. 查看 SD 卡根目录的 CS16-debug.log，并把它发来。
   例如电脑中 SD 卡盘符为 X: 时，文件是 X:\CS16-debug.log。

记录范围
补丁在引擎的 Sys_Print 输出路径增加 fopen(追加)、fwrite、fclose。
每条消息完成后关闭文件，以尽量保留退出前已输出的内容。
不依赖原引擎被禁用的 Sys_InitLog 初始化，也不依赖 -log 参数。
如果在引擎首次文字输出前就退出，或 SD 卡无法写入，仍可能没有文件。
如果依然没有日志，请附上启动至退出的视频或报错照片，并说明从 NSP 图标还是完整内存 hbmenu 启动。

恢复
将备份的原始 NRO 放回 /switch/xash3d-cstrike.nro 即可恢复。

验证与范围
已验证：输入代码段摘要、修改位置原指令、代码空闲区、NRO 结构、
ARM64 模拟器中的成功写入路径和文件打开失败路径、栈对齐、寄存器恢复及原输出跳转。
模拟验证中的文件操作为接口模拟，不代表已在 Switch 上验证实际 SD 卡写入。
未修改游戏资源、对战逻辑、渲染设置或时钟服务。

源码与许可证
补丁生成脚本及模拟检查脚本位于“诊断补丁源码”。
补丁基于 https://github.com/switchports/xash3d-switch/releases/tag/v1.0.1 的 CS NRO。
上游源代码：https://github.com/switchports/xash3d-switch/tree/v1.0.1
原引擎 GPLv3 许可证见同目录文件。
