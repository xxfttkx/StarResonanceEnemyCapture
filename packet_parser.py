"""
模组解析器
"""

import json
import logging
from typing import Dict, List, Optional, Any
from logging_config import get_logger
from star_pb2 import AttrIdValue

# 获取日志器
logger = get_logger(__name__)
AttrType = {
    "AttrName": 0x01,
    "AttrId": 0x0a,
    "AttrProfessionId": 0xdc,
    "AttrFightPoint": 0x272e,
    "AttrLevel": 0x2710,
    "AttrRankLevel": 0x274c,
    "AttrCri": 0x2b66,
    "AttrLucky": 0x2b7a,
    "AttrHp": 0x2c2e,
    "AttrMaxHp": 0x2c38,
    "AttrElementFlag": 0x646d6c,
    "AttrReductionLevel": 0x64696d,
    "AttrReduntionId": 0x6f6c65,
    "AttrEnergyFlag": 0x543cd3c6,
}

def print_proto(obj, indent=0):
    prefix = "  " * indent
    for field, value in obj.ListFields():  # proto对象提供 ListFields() 列出已设置的字段
        if field.type == field.TYPE_MESSAGE:
            print(f"{prefix}{field.name}:")
            if field.label == field.LABEL_REPEATED:
                for i, v in enumerate(value):
                    print(f"{prefix}  [{i}]")
                    print_proto(v, indent + 2)
            else:
                print_proto(value, indent + 1)
        else:
            print(f"{prefix}{field.name}: {value}")

def read_varint(data: bytes) -> int:
    result, shift = 0, 0
    for b in data:
        result |= (b & 0x7F) << shift
        if not (b & 0x80):
            return result
        shift += 7
    raise ValueError("Invalid varint")

def read_string(data: bytes) -> str:
    length = read_varint(data)
    return data[1:1+length].decode("utf-8", errors="ignore")

class PacketParser:
    """模组解析器"""
    
    def __init__(self, callback):
        self.logger = logger
        self.monster_names = {}
        self.callback = callback
        with open("monster_names.json", "r", encoding="utf-8") as f:
            self.monster_names = json.load(f)

    


    
    def parse_module_info(self, v_data: Any): #CharSerialize
        """
        解析模组信息

        Args:
            v_data: VData数据
        """
        self.logger.info("开始解析模组")
        
        mod_infos = v_data.Mod.ModInfos

    def parse_SyncNearEntities(self, data):
        for entity in data.Appear:
            self.parse_AoiSyncDelta(entity)

    def parse_SyncNearDeltaInfo(self, data):
        for delta in data.DeltaInfos:
            self.parse_AoiSyncDelta(delta)
    
    def parse_AoiSyncDelta(self, aoiSyncDelta):
        uuid = aoiSyncDelta.Uuid
        def is_uuid_monster(uuid: int) -> bool:
            return (int(uuid) & 0xffff) == 64
        if is_uuid_monster(uuid):
            attrCollection = aoiSyncDelta.Attrs.Attrs
            self._process_enemy_attrs(uuid, attrCollection)
    
    def _process_enemy_attrs(self, enemy_uid, attrs):
        for attr in attrs:
            attr_id = getattr(attr, "Id", None)
            raw_data = getattr(attr, "RawData", None)
            if not attr_id or not raw_data:
                continue

            # 这里 raw_data 是 bytes
            reader = memoryview(raw_data)
            self.logger.debug(f"Found attrId {attr_id} for E{enemy_uid} {raw_data.hex()}")

            if attr_id == AttrType["AttrName"]:
                # 假设 RawData 是 UTF-8 string
                enemy_name = raw_data.decode("utf-8", errors="ignore")
                # self.userDataManager.enemyCache.name[enemy_uid] = enemy_name
                self.logger.info(f"Found monster name {enemy_name} for id {enemy_uid}")

            elif attr_id == AttrType["AttrId"]:
                # 简单示例：取前 4 字节当 int32
                attr_val = int.from_bytes(raw_data[:4], "little", signed=True)
                # attr_val = AttrIdValue()
                # attr_val.ParseFromString(raw_data)
                attr_val = read_varint(raw_data)
                name = self.monster_names.get(str(attr_val))
                # self.logger.info(f"Found monster name {name} for monster id {attr_val}")
                self.callback({"enemy_uid": enemy_uid, "enemy_name": name})
                # name = monsterNames.get(attr_val)
                # if name:
                #     self.logger.info(f"Found monster name {name} for id {enemy_uid}")
                #     self.userDataManager.enemyCache.name[enemy_uid] = name

            elif attr_id == AttrType["AttrHp"]:
                enemy_hp = int.from_bytes(raw_data[:4], "little", signed=True)
                enemy_hp = read_varint(raw_data)
                # self.logger.info(f"Found monster hp {enemy_hp} for id {enemy_uid}")
                self.callback({"enemy_uid": enemy_uid, "enemy_hp": enemy_hp})
                # self.userDataManager.enemyCache.hp[enemy_uid] = enemy_hp

            elif attr_id == AttrType["AttrMaxHp"]:
                enemy_max_hp = int.from_bytes(raw_data[:4], "little", signed=True)
                enemy_max_hp = read_varint(raw_data)
                # self.logger.info(f"Found monster max hp {enemy_max_hp} for id {enemy_uid}")
                self.callback({"enemy_uid": enemy_uid, "enemy_max_hp": enemy_max_hp})
                # self.userDataManager.enemyCache.maxHp[enemy_uid] = enemy_max_hp

            else:
                # self.logger.debug(f"Found unknown attrId {attr_id} for E{enemy_uid} {raw_data.hex()}")
                pass



