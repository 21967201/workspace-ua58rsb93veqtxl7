=== 全自动 WorkBuddy 诊断和修复 ===
时间: 05/30/2026 12:00:44

[1/8] 检查当前进程状态...
  ✅ WorkBuddy 未运行

[2/8] 检查端口 58733...
  ✅ 端口未被占用

[3/8] 捕获实际错误...
  启动 WorkBuddy 并捕获输出到: D:\Cache\Temp\tmp5DCC.tmp.txt
  ❌ WorkBuddy 进程已退出
  检查 Windows 事件日志...
  ⚠️ 未在事件日志中找到相关错误

[4/8] 检查 .NET Runtime...
  ✅ 找到 .NET: C:\Program Files\dotnet\dotnet.exe (版本: )

[5/8] 检查 Visual C++ Redistributable...
  ✅ 找到: Microsoft Visual C++ 2010  x64 Redistributable - 10.0.40219 Microsoft Visual C++ 2005 Redistributable (x64) Microsoft Visual C++ 2010  x86 Redistributable - 10.0.40219 Microsoft Visual C++ 2008 Redistributable - x64 9.0.30729.7523 Microsoft Visual C++ 2008 Redistributable - x86 9.0.30729.6161 Microsoft Visual C++ 2005 Redistributable

[6/8] 尝试以兼容模式运行...
  检查可执行文件...
    文件版本: 4.24.2
    产品版本: 4.24.2.0
    创建时间: 05/29/2026 17:52:52
  尝试以管理员身份运行...
  ❌ 管理员身份启动失败（进程已退出）

[7/8] 检查数据文件权限...
  ❌ 数据库文件不存在: D:\WorkBuddyX\.workbuddy\workbuddy.db

[8/8] 最终诊断和修复建议...
  ❌ WorkBuddy 无法运行

🔧 自动修复建议（已全自动生成）:

1. 完全卸载并重新安装:
   - 设置 → 应用 → WorkBuddy → 卸载
   - 删除: D:\WorkBuddy, D:\WorkBuddyX, D:\WorkBuddyData
   - 重新启动
   - 下载最新版本: https://workbuddy.ai/download
   - 安装到: D:\WB (短路径，避免权限问题)

2. 安装必需依赖:
   - .NET 6 Desktop Runtime: https://dotnet.microsoft.com/download/dotnet/6.0
   - Visual C++ Redistributable 2019+: https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist

3. 以管理员身份运行:
   - 右键 WorkBuddy.exe → 以管理员身份运行

4. 检查防火墙/杀毒软件:
   - 将 WorkBuddy.exe 添加到白名单

5. 联系官方支持:
   - https://workbuddy.ai/support
   - 提供错误截图: 'Internal error [CodeBuddyCodeBackend]'
