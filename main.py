"""
主程序入口
"""

import json
import logging
import sys
import time
import threading
import argparse
import os
import multiprocessing as mp
from typing import Dict, List, Optional, Any
from enemy_manager import EnemyManager
from logging_config import setup_logging, get_logger
from packet_capture import PacketCapture
from network_interface_util import get_network_interfaces, select_network_interface
from packet_parser import PacketParser

# 多进程保护
_is_main_process = mp.current_process().name == 'MainProcess'

# 获取日志器
logger = get_logger(__name__) if _is_main_process else None


class StarResonanceMonitor:
    """星痕共鸣监控器"""
    
    def __init__(self, interface_index: int = None):
        """
        初始化监控器
        
        Args:
            interface_index: 网络接口索引
        """
        self.interface_index = interface_index
        self.is_running = False
        
        # 获取网络接口信息
        self.interfaces = get_network_interfaces()
        if interface_index is not None and 0 <= interface_index < len(self.interfaces):
            self.selected_interface = self.interfaces[interface_index]
        else:
            self.selected_interface = None
            
        # 初始化组件
        interface_name = self.selected_interface['name'] if self.selected_interface else None
        self.packet_capture = PacketCapture(interface_name)
        self.packet_parser = PacketParser(self._on_callback)
        self.enemy_manager = EnemyManager()
        # 统计数据
        self.stats = {
            'total_packets': 0,
            'sync_container_packets': 0,
            'parsed_modules': 0,
            'players_found': 0,
            'start_time': None
        }
        
        # 存储解析结果
        self.player_modules = {}  # 玩家UID -> 模组列表
        self.module_history = []  # 模组历史记录
        
    def start_monitoring(self):
        """开始监控"""
        self.is_running = True
        self.stats['start_time'] = time.time()
        
        logger.info("=== 星痕共鸣监控器启动 ===")
        if self.selected_interface:
            logger.info(f"网络接口: {self.interface_index} - {self.selected_interface['description']}")
            logger.info(f"接口名称: {self.selected_interface['name']}")
            addresses = [addr['addr'] for addr in self.selected_interface['addresses']]
            logger.info(f"接口地址: {', '.join(addresses)}")
        else:
            logger.info("网络接口: 自动")
        
        # 启动抓包
        self.packet_capture.start_capture(self._on_callback)
        
        
        logger.info("监控已启动")
        
    def stop_monitoring(self):
        """停止监控"""
        self.is_running = False
        self.packet_capture.stop_capture()
        
        logger.info("=== 监控已停止 ===")

    def _on_callback(self, data: Dict[str, Any]):
        try:
            if "SyncNearDeltaInfo" in data:
                sync_data = data["SyncNearDeltaInfo"]
                self.packet_parser.parse_SyncNearDeltaInfo(sync_data)
            if "SyncNearEntities" in data:
                sync_data = data["SyncNearEntities"]
                self.packet_parser.parse_SyncNearEntities(sync_data)
            if "server_change" in data:
                self.packet_capture.src_servers = {}
                # self.packet_capture._clear_tcp_cache()
                self.enemy_manager.clearAll()
            enemy_uid = data.get('enemy_uid')
            enemy_name = data.get('enemy_name')
            enemy_hp = data.get('enemy_hp')
            enemy_max_hp = data.get('enemy_max_hp')
            if enemy_uid:
                self.enemy_manager.sync_enemy(
                    id=enemy_uid,
                    name=enemy_name,
                    hp=enemy_hp,
                    max_hp=enemy_max_hp
                )
        except Exception as e:
            logger.error(f"Exception: {e}")

def main():
    """主函数"""
    
    parser = argparse.ArgumentParser(description='星痕共鸣模组筛选器')
    parser.add_argument('--interface', '-i', type=int, help='网络接口索引')
    parser.add_argument('--debug', '-d', action='store_true', help='启用调试模式')
    parser.add_argument('--auto', '-a', action='store_true', help='自动检测默认网络接口')
    parser.add_argument('--list', '-l', action='store_true', help='列出所有网络接口')

    args = parser.parse_args()
    
    # 设置日志系统
    setup_logging(debug_mode=args.debug)
        
    # 获取网络接口列表
    interfaces = get_network_interfaces()
    
    if not interfaces:
        logger.error("未找到可用的网络接口!")
        return
        
    # 列出网络接口
    if args.list:
        print("=== 可用的网络接口 ===")
        for i, interface in enumerate(interfaces):
            name = interface['name']
            description = interface.get('description', name)
            is_up = "✓" if interface.get('is_up', False) else "✗"
            addresses = [addr['addr'] for addr in interface['addresses']]
            addr_str = ", ".join(addresses) if addresses else "无IP地址"
            
            print(f"  {i:2d}. {is_up} {description}")
            print(f"      地址: {addr_str}")
            print(f"      名称: {name}")
            print()
        return
        
    # 确定要使用的接口
    interface_index = None
    
    if args.auto:
        # 自动检测默认接口
        print("自动检测默认网络接口...")
        interface_index = select_network_interface(interfaces, auto_detect=True)
        if interface_index is None:
            logger.error("未找到默认网络接口!")
            return
    elif args.interface is not None:
        # 使用指定的接口索引
        if 0 <= args.interface < len(interfaces):
            interface_index = args.interface
        else:
            logger.error(f"无效的接口索引: {args.interface}")
            return
    else:
        # 交互式选择
        print("星痕共鸣喵喵喵!")
        print("版本: V1.0")
        print("GitHub: https://github.com/fudiyangjin/StarResonanceAutoMod")
        print()
        
        interface_index = select_network_interface(interfaces)
        if interface_index is None:
            logger.error("未选择网络接口!")
            return
            
    # 创建监控器
    monitor = StarResonanceMonitor(
        interface_index=interface_index
    )
    
    try:
        # 启动监控
        monitor.start_monitoring()
        
        # 等待模组解析完成
        logger.info("开始监控喵~")

        # 启动后台线程
        def periodic_task():
            while True:
                time.sleep(30)
                logger.info("定时输出：30 秒过去了喵~")
                for server, count in monitor.packet_capture.src_servers.items():
                    if count>10:
                        logger.info(f"服务器 {server} - 捕获数据包数: {count}")
        t = threading.Thread(target=periodic_task, daemon=True)
        t.start()
        
        while monitor.is_running:
            time.sleep(0.1)  # 更频繁的检查，减少延迟
            
    except KeyboardInterrupt:
        logger.info("收到停止信号")
    finally:
        if monitor.is_running:
            monitor.stop_monitoring()


if __name__ == "__main__":
    # 多进程打包支持
    mp.freeze_support()
    sys.stdout.reconfigure(encoding='utf-8')
    main() 