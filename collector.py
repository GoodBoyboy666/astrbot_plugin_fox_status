import datetime
import platform
import psutil

def get_cpu_name():
    if platform.system() == "Windows":
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
            processor_name = winreg.QueryValueEx(key, "ProcessorNameString")[0]
            winreg.CloseKey(key)
            return processor_name.strip()
        except:
            pass
    elif platform.system() == "Linux":
        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "model name" in line:
                        return line.split(":")[1].strip()
        except:
            pass
    return platform.processor()

#获取系统详情
def get_system_info():
    return (
        f"  🖥️ 系统: {platform.system()} {platform.release()} {platform.machine()}\n"
    )
    

#获取CPU温度
def get_cpu_temp():
    try:
        #Windows不可用
        func = getattr(psutil, "sensors_temperatures", None)
        if not func:
            return None
        temps = func()
        if not temps:
            return None
        for name in ['coretemp', 'cpu_thermal', 'k10temp', 'zenpower']:
            if name in temps:
                for entry in temps[name]:
                    if 'Package' in entry.label: return entry.current
                return temps[name][0].current
        return None
    except:
        return None
#获取启动时间
def get_start_time_info():
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.datetime.fromtimestamp(boot_time_timestamp)
    now = datetime.datetime.now()
    uptime = now - bt
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_str = f"{days}天" if days > 0 else ""
    uptime_str += f"{hours}小时{minutes}分"
    
    return(
        f"  ⏱️ 启动时间: {bt.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"  ⌛ 已运行: {uptime_str}\n"
    )

#获取CPU使用率
def get_cpu_info():
    temp = get_cpu_temp()
    temp_str = f" | 🌡️ {temp}°C" if temp is not None else ""
    return(
        f"  🧠 CPU: {get_cpu_name()} ({psutil.cpu_count(logical=False)}C/{psutil.cpu_count(logical=True)}T)\n"
        f"  📊 使用: {psutil.cpu_percent(interval=1)}%{temp_str}\n"
    )

def bytes_to_gb(bytes_value):
    return round(bytes_value / (1024 ** 3), 2)

#获取内存使用详情
def get_mem_info():
    mem = psutil.virtual_memory()
    return(
        f"  🐏 内存使用: {bytes_to_gb(mem.used)}/{bytes_to_gb(mem.total)} GB ({mem.percent}%)\n"
    )
    
    
#获取硬盘信息
def get_disk_info():
    partitions = psutil.disk_partitions()
    disk_info=""
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_info += f"  💿 {partition.device} [{partition.fstype}] {bytes_to_gb(usage.used)}/{bytes_to_gb(usage.total)} GB ({usage.percent}%)\n"
        except PermissionError:
            pass
    return disk_info

def get_all_info():
    all_info = "✨ 系统概览 ✨\n"
    all_info += get_system_info()
    all_info += get_start_time_info()
    all_info += "\n📈 资源监控\n"
    all_info += get_cpu_info()
    all_info += get_mem_info()
    all_info += "\n💾 存储空间\n"
    all_info += get_disk_info()
    return all_info