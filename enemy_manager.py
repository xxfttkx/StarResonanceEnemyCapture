import threading
from fastapi import FastAPI
import uvicorn
from logging_config import get_logger


logger = get_logger(__name__)


class EnemyManager:
    """EnemyManager"""

    def __init__(self):
        self.logger = logger
        self.enemies = {}
        self.app = FastAPI()
        host="127.0.0.1"
        port=1289

        # 注册路由
        @self.app.get("/enemies")
        def list_enemies():
            return self.enemies

        @self.app.get("/enemies/{enemy_name}")
        def get_enemy(enemy_name: str):
            for enemy_uuid, enemy in self.enemies.items():
                if enemy.get('name') == enemy_name:
                    return enemy
            return {}

        # 后台启动 API
        thread = threading.Thread(
            target=lambda: uvicorn.run(
                self.app, host=host, port=port, log_level="info"
            ),
            daemon=True
        )
        thread.start()
    
    def sync_enemy(self, id, name, hp, max_hp):
        """敌人管理器 + API 服务"""
        if not id:
            return
        enemy = self.enemies.get(id, {})
        if name:
            enemy['name'] = name
        if hp:
            enemy['hp'] = hp
        if max_hp:
            enemy['max_hp'] = max_hp
        self.enemies[id] = enemy
        if 'name' in enemy and 'hp' in enemy and 'max_hp' in enemy:
            monsters = {"丛林哥布林战士"}
            if enemy['name'] in monsters:
                self.logger.info(f"同步敌人数据: {id} -> {enemy['name']}, HP: {enemy['hp']}/{enemy['max_hp']}")