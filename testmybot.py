from telegram import *
from telegram.ext import *
from telegram.constants import *
import random
import asyncio
import time
import copy
import re
import os 
from html import escape 
from pymongo import *

app = ApplicationBuilder().token('8192198859:AAEjumdnoYl2Q3xfREpynM3RRIWaJs8bMwo').build()


ADMINS = [ 6590055256 , 1428143946] 

uri = 'mongodb://pratham82007:ILUVINDIA.8@ac-rl6xcgx-shard-00-00.lyxdumr.mongodb.net:27017,ac-rl6xcgx-shard-00-01.lyxdumr.mongodb.net:27017,ac-rl6xcgx-shard-00-02.lyxdumr.mongodb.net:27017/?ssl=true&replicaSet=atlas-13ain9-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0'
#init_user
client = MongoClient(uri)
db = client['mydatabase']
users = db['users']

def init_user(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id):
    username = update.effective_user.username or update.effective_user.first_name
    
    user_info = users.find_one({"user_id": user_id})
    
    if user_info is None:
        user_info = {
            'user_id': user_id,
            'username': username,
            'level': 1,
            'xp': 0,
            'coins': 1000,
            'essences': 0,
            'moonshards': 0,
            'max_xp': 100,
            'explores_won': 0,
            'explores_lost': 0,
            'explores_played': 0,
            'power': 50,
            'max_power': 50,
            'max_hp': 250,
            'hp': 250,
            'agility': 200,
            'max_agility': 200,
            'resistance': 20,
            'max_resistance': 20,
            'battles_played': 0,
            'battles_won': 0,
            'battles_lost': 0,
            'user_weapons': {},
            'equiped_weapon': None,
            'magical_items': []
        }
        users.insert_one(user_info)  # insert into collection
    
    return user_info

def add_field_to_all_users(field_name, default_value):
    users.update_many(
        {field_name: {"$exists": False}}, 
        {"$set": {field_name: default_value}}
    )
  
def add_field_to_all_user_weapons(weapon_name, field, value):
    users.update_many(
        {f"user_weapons.{weapon_name}": {"$exists": True}},
        {"$set": {f"user_weapons.{weapon_name}.{field}": value}}
    )

def add_ability_to_all_user_weapons(weapon_name, ability, ability_name, ability_data):
    users.update_many(
        {f"user_weapons.{weapon_name}": {"$exists": True}},
        {"$set": {f"user_weapons.{weapon_name}.{ability}.{ability_name}": ability_data}}
    )
      
def remove_ability_from_all_users(weapon_name, ability_type, ability_name):
    users.update_many(
        {f"user_weapons.{weapon_name}.{ability_type}.{ability_name}": {"$exists": True}},  
        {"$unset": {f"user_weapons.{weapon_name}.{ability_type}.{ability_name}": ""}}
    )

monsters = db['monsters']

monster_list = [
  {'name': 'lasher', 'hp': 300, 'dmg': 100, 'agility': 300, 'photo': 'AgACAgUAAxkBAAINfmiV-8k3XKyDaBEh2IpWWyv-Pk0qAAKXxjEbdoyxVEdHn_YxLf4pAQADAgADeQADNgQ', 'monster_id': 10001}, 
  {'name': 'slayer', 'hp': 150, 'dmg': 90, 'agility': 260, 'photo': 'AgACAgUAAxkBAAINf2iV-8kXZj7um1j_sZBco8BWji03AAKYxjEbdoyxVAxhQ1-X5-AhAQADAgADeQADNgQ', 'monster_id': 10002}, 
  {'name': 'gloam', 'hp': 230, 'dmg': 90, 'agility': 210, 'photo': 'AgACAgUAAxkBAAINgGiV-8nQxkd2bUwJecopBB6iXYoDAAKZxjEbdoyxVLuVEDkg189iAQADAgADeQADNgQ', 'monster_id': 10003}, 
  {'name': 'razorbeak', 'hp': 190, 'dmg': 90, 'agility': 240, 'photo': 'AgACAgUAAxkBAAINgWiV-8lElhjVKwPmCjVmh5lMg345AAKaxjEbdoyxVF1wBfcmGhN3AQADAgADeAADNgQ', 'monster_id': 10004}, 
  {'name': 'blightborn', 'hp': 120, 'dmg': 50, 'agility': 150, 'photo': 'AgACAgUAAxkBAAINgmiV-8mSo4DBhhjPhGJXrQie0nJ8AAKbxjEbdoyxVPAm76E_YObYAQADAgADeQADNgQ', 'monster_id': 10005}, 
  {'name': 'shadefang', 'hp': 130, 'dmg': 50, 'agility': 170, 'photo': 'AgACAgUAAxkBAAINg2iV-8l1BwvKyjCL4L7tKROpIMvqAAKexjEbdoyxVBvB4eUZo6KKAQADAgADeQADNgQ', 'monster_id': 10006}, 
  {'name': 'duskmaw', 'hp': 160, 'dmg': 60, 'agility': 160, 'photo': 'AgACAgUAAxkBAAINhGiV-8kAAeytiXeU21wRv5xa_-n1HgACn8YxG3aMsVTgRAgO89dufgEAAwIAA3kAAzYE', 'monster_id': 10007}, 
  {'name': 'hollowroot', 'hp': 110, 'dmg': 70, 'agility': 150, 'photo': 'AgACAgUAAxkBAAINhWiV-8nALq4cH4ltO8zZr1GKXogHAAKgxjEbdoyxVBPCqXnhr2k_AQADAgADeAADNgQ', 'monster_id': 10008}, 
  {'name': 'vilethorn', 'hp': 180, 'dmg': 80, 'agility': 165, 'photo': 'AgACAgUAAxkBAAINhmiV-8lcxBmij39Ut0N7WbuICwbVAAKhxjEbdoyxVBTBrYof85srAQADAgADeQADNgQ', 'monster_id': 10009}, 
  {'name': 'embergut', 'hp': 230, 'dmg': 75, 'agility': 175, 'photo': 'AgACAgUAAxkBAAINh2iV-8nOKrlknIfAgPeLpJyG5WQAA6TGMRt2jLFUjjODUhhGY9cBAAMCAAN5AAM2BA', 'monster_id': 10010}, 
  {'name': 'doomcaller', 'hp': 210, 'dmg': 45, 'agility': 170, 'photo': 'AgACAgUAAxkBAAINiGiV-8nwXWbRGvL0Vln4fYZJxjVhAAKlxjEbdoyxVHP_wG3Tc-qwAQADAgADeQADNgQ', 'monster_id': 10011}, 
  {'name': 'rotclaw', 'hp': 100, 'dmg': 30, 'agility': 135, 'photo': 'AgACAgUAAxkBAAINiWiV-8m_p_K_lyWFQUrxT_DAt55YAAKmxjEbdoyxVKBT_bN8PPphAQADAgADeAADNgQ', 'monster_id': 10012}, 
  {'name': 'ashen_wyrm', 'hp': 260, 'dmg': 40, 'agility': 160, 'photo': 'AgACAgUAAxkBAAINimiV-8kobB-FsztMEEoLPXLIpuU_AAKnxjEbdoyxVC64FTmHN2xQAQADAgADeAADNgQ', 'monster_id': 10013}, 
  {'name': 'blackvein', 'hp': 170, 'dmg': 35, 'agility': 150, 'photo': 'AgACAgUAAxkBAAINi2iV-8nxncjEJAYjHH-Srv1Eid0uAAKoxjEbdoyxVOWvG8_fEMOfAQADAgADeAADNgQ', 'monster_id': 10014}, 
  {'name': 'soulgnaw', 'hp': 140, 'dmg': 30, 'agility': 125, 'photo': 'AgACAgUAAxkBAAINjGiV-8ndgtf5IKqnKgfCKm5f7w_nAAKpxjEbdoyxVFDClP7XytlEAQADAgADeQADNgQ', 'monster_id': 10015}, 
  {'name': 'thornfiend', 'hp': 170, 'dmg': 65, 'agility': 145, 'photo': 'AgACAgUAAxkBAAINjWiV-8mdsoO7e6pCATXudUAYSn_lAAKqxjEbdoyxVHQiW9zfwJvYAQADAgADeAADNgQ', 'monster_id': 10016}, 
  {'name': 'voidlurker', 'hp': 250, 'dmg': 110, 'agility': 195, 'photo': 'AgACAgUAAxkBAAINjmiV-8m9tSa6z9gr4yB9Xg92St_WAAKsxjEbdoyxVA7TtZyIF4GXAQADAgADeQADNgQ', 'monster_id': 10017}, 
  {'name': 'nethermaw', 'hp': 300, 'dmg': 85, 'agility': 185, 'photo': 'AgACAgUAAxkBAAINj2iV-8kGpxysKWBZYJkAAVvuGt0qnQACrcYxG3aMsVSeRKlUTIREewEAAwIAA3gAAzYE', 'monster_id': 10018}, 
  {'name': 'cragjaw', 'hp': 160, 'dmg': 45, 'agility': 115, 'photo': 'AgACAgUAAxkBAAINkGiV-8ntOsj6T6DG7IgUG5vGQ8MjAAKuxjEbdoyxVAE7aSVD2V2XAQADAgADeQADNgQ', 'monster_id': 10019}, 
  {'name': 'stormhide', 'hp': 130, 'dmg': 95, 'agility': 200, 'photo': 'AgACAgUAAxkBAAINkWiV-8kLxR9TyhJJMovs7RVH9jKcAAKwxjEbdoyxVL6AgFWi5JSOAQADAgADeAADNgQ', 'monster_id': 10020}, 
  {'name': 'skyripper', 'hp': 120, 'dmg': 60, 'agility': 200, 'photo': 'AgACAgUAAxkBAAINkmiV-8n5UCPhLD4VtOyhHyIm4FHjAAKyxjEbdoyxVJIsS33zoo-wAQADAgADeQADNgQ', 'monster_id': 10021}, 
  {'name': 'deathbloom', 'hp': 180, 'dmg': 75, 'agility': 210, 'photo': 'AgACAgUAAxkBAAINk2iV-8lIEi635A6ilNIfA79RUcnnAAKzxjEbdoyxVAuBViFY2YbqAQADAgADeAADNgQ', 'monster_id': 10022}, 
  {'name': 'pyrelord', 'hp': 160, 'dmg': 120, 'agility': 240, 'photo': 'AgACAgUAAxkBAAINlGiV-8mbOejOOtA56mV39tfxLyheAAK1xjEbdoyxVO2RCH7tETBCAQADAgADeQADNgQ', 'monster_id': 10023}, 
  {'name': 'glarefang', 'hp': 240, 'dmg': 100, 'agility': 420, 'photo': 'AgACAgUAAxkBAAINlWiV-8ljphR7pzWTtFIi8u8GRCnXAAK4xjEbdoyxVMIp2AGB2zKbAQADAgADeAADNgQ', 'monster_id': 10024},
  {'name': 'timbergnash', 'hp': 320, 'dmg': 55, 'agility': 300, 'photo': 'AgACAgUAAxkBAAINlmiV-8neiS7joBQpHVdVr64FY-kuAAK5xjEbdoyxVCfLYl6YKDXaAQADAgADeQADNgQ', 'monster_id': 10025}]


monsters.insert_many(monster_list)


def init_monster(update: Update, context: ContextTypes.DEFAULT_TYPE, monster_id: int):
    monster_info = monsters.find_one({"monster_id": monster_id}, {"_id": 0})  
    return monster_info
  

weapon_list = {
    'Bronze Sword': {
        'name': 'Bronze Sword',
        'bonus_power': 10,
        'bonus_hp': 30,
        'base_power': 10,
        'base_hp': 30,
        'base_agility': 50,
        'base_resistance':5,
        'bonus_resistance':5,
        'price': 1,
        'rarity': 'Common',
        'bonus_agility': 50,
        'weapon_level': 1,
        'weapon_xp': 0,
        'weapon_max_xp': 150,
        'photo':"AgACAgUAAxkBAAINR2iV5xqtiKk7dUCyX_Fe-g7m5_6DAAKmyjEbsDKwVPy0UV1aOCAXAQADAgADeQADNgQ",
        'abilities':{},
        'activeabilities':{},
        'passiveabilities':{},
    },
    'Iron Blade': {
        'name': 'Iron Blade',
        'bonus_power': 20,
        'bonus_hp': 50,
        'base_power': 20,
        'base_hp': 50,
        'base_agility': 120,
        'base_resistance':10,
        'bonus_resistance':10,
        'price': 5,
        'rarity': 'Uncommon',
        'bonus_agility': 120,
        'weapon_level': 1,
        'weapon_xp': 0,
        'weapon_max_xp': 150,
        'photo':"AgACAgUAAxkBAAINQ2iV5xWGX5YHGPSAbkS68hVlrsv2AAKqyjEbsDKwVAoh22qI3RGlAQADAgADeQADNgQ",
        'abilities':{
          'momentum':{
            'name': 'Momentum 🌀',
            'description':'If Player\'s agility more than enemy\'s agility , Increase player power by 80% for the rest of the match.'
          }
        },
        'activeabilities':{},
        'passiveabilities':{},
    },
    'Crystal Lance': {
    'name': 'Crystal Lance',
    'bonus_power': 30,
    'bonus_hp': 80,
    'bonus_agility': 100,
    'base_power': 30,
    'base_hp': 80,
    'base_agility': 100,
    'base_resistance':15,
    'bonus_resistance':15,
    'price': 15,
    'rarity': 'Rare',
    'weapon_level': 1,
    'weapon_xp': 0,
    'weapon_max_xp': 150,
    'photo': "AgACAgUAAxkBAAINQWiV5xOqqIqJCpsX9dG3hN2AOncGAAKoyjEbsDKwVA9o3H25EL4aAQADAgADeQADNgQ",
    'abilities': {},
    'passiveabilities': {
      'more_power':{
        'name': 'More Power 💪',
        'description':'40% chance to boost weapon power by 50% for the rest of the battle.'
      }
    },
    'activeabilities': {}
      }
    }
  
all_weapon_list = {
    'Bronze Sword': {
        'name': 'Bronze Sword',
        'bonus_power': 10,
        'bonus_hp': 30,
        'base_power': 10,
        'base_hp': 30,
        'base_agility': 50,
        'price': 1,
        'rarity': 'Common',
        'bonus_agility': 50,
        'base_resistance':5,
        'bonus_resistance':5,
        'weapon_level': 1,
        'weapon_xp': 0,
        'weapon_max_xp': 150,
        'photo':"AgACAgUAAxkBAAINR2iV5xqtiKk7dUCyX_Fe-g7m5_6DAAKmyjEbsDKwVPy0UV1aOCAXAQADAgADeQADNgQ",
        'abilities':{},
        'activeabilities':{},
        'passiveabilities':{},
    },
    'Iron Blade': {
        'name': 'Iron Blade',
        'bonus_power': 20,
        'bonus_hp': 50,
        'base_power': 20,
        'base_hp': 50,
        'base_agility': 120,
        'base_resistance':10,
        'bonus_resistance':10,
        'price': 5,
        'rarity': 'Uncommon',
        'bonus_agility': 120,
        'weapon_level': 1,
        'weapon_xp': 0,
        'weapon_max_xp': 150,
        'photo':"AgACAgUAAxkBAAINQ2iV5xWGX5YHGPSAbkS68hVlrsv2AAKqyjEbsDKwVAoh22qI3RGlAQADAgADeQADNgQ",
        'abilities':{
          'momentum':{
            'name': 'Momentum 🌀',
            'description':'If Player\'s agility more than enemy\'s agility , Increase player power by 80% for the rest of the match.'
          }
        },
        'activeabilities':{},
        'passiveabilities':{},
    },
    'Crystal Lance': {
    'name': 'Crystal Lance',
    'bonus_power': 30,
    'bonus_hp': 80,
    'bonus_agility': 100,
    'base_power': 30,
    'base_hp': 80,
    'base_agility': 100,
    'base_resistance':15,
    'bonus_resistance':15,
    'price': 15,
    'rarity': 'Rare',
    'weapon_level': 1,
    'weapon_xp': 0,
    'weapon_max_xp': 150,
    'photo': "AgACAgUAAxkBAAINQWiV5xOqqIqJCpsX9dG3hN2AOncGAAKoyjEbsDKwVA9o3H25EL4aAQADAgADeQADNgQ",
    'abilities': {},
    'passiveabilities': {
      'more_power':{
        'name': 'More Power 💪',
        'description':'40% chance to boost weapon power by 50% for the rest of the battle.'
      }
    },
    'activeabilities': {}
      },
      
    'Void Edge': {
        'name': 'Void Edge',
        'bonus_power': 50,
        'bonus_hp': 120,
        'base_power': 50,
        'base_hp': 120,
        'base_agility': 200,
        'price': 35,
        'rarity': 'Epic',
        'bonus_agility': 200,
        'base_resistance':25,
        'bonus_resistance':25,
        'weapon_level': 1,
        'weapon_xp': 0,
        'weapon_max_xp': 150,
        'photo':"AgACAgUAAxkBAAINRWiV5xgjov4p49ex0UOUD40-MJErAAKpyjEbsDKwVPTgPUSRux_yAQADAgADeAADNgQ",
        'abilities':{},
        'activeabilities':{},
        'passiveabilities':{},
        },
    'Infernal Aegis': {
        'name': 'Infernal Aegis',
        'bonus_power': 60,
        'bonus_hp': 100,
        'bonus_agility': 210,
        'bonus_resistance':20,
        'base_power': 60,
        'base_hp': 100,
        'base_agility': 210,
        'base_resistance':20,
        'price': 30,
        'rarity': 'Epic',
        'weapon_level': 1,
        'weapon_xp': 0,
        'weapon_max_xp': 150,
        'photo': 'https://files.catbox.moe/eme34z.jpg',
        'abilities':{},
        'activeabilities':{
          'scorching_brand':{
            'name':'🔥 Scorching Brand',
            'description':'Burn damage equal to 2 times of weapon’s HP bonus'}
        },
        'passiveabilities':{},
        
      },
    'Bonecutter':{
      'name':'Bonecutter',
      'bonus_power': 80,
      'bonus_hp': 150,
      'bonus_agility': 100,
      'bonus_resistance':40,
      'base_power': 80,
      'base_hp': 150,
      'base_agility': 100,
      'base_resistance':40,
      'price': 50,
      'rarity': 'Elite',
      'weapon_level': 1,
      'weapon_xp': 0,
      'weapon_max_xp': 150,
      'photo': 'https://files.catbox.moe/nr1bwe.jpg',
      'abilities':{
        'brutal':{
          'name':'Brutal',
          'description':'Immune to enemy resistance'
        }
      },
      'activeabilities':{
        'butcher':{
          'name':'Butcher 🔪',
          'description':'When activated, the target’s HP is instantly reduced to 1'
        }
      },
      'passiveabilities':{},
      }
    }
    
async def activate_pre_battle_ability(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id, activity_type):
  
  user_info = users.find_one({"user_id": user_id})
  user_data = context.user_data
  chat_data = context.chat_data
  message_id = update.effective_message.id

  if not user_info:
      return  

  equiped_weapon = user_info.get("equiped_weapon")
  user_weapons = user_info.get("user_weapons", {})

  if not equiped_weapon or equiped_weapon not in user_weapons:
    return
  
  weapon = user_weapons[equiped_weapon]

  # Handle battle case
  if activity_type == 'battle':
    data_type = context.chat_data[message_id]

    if user_id == context.chat_data[message_id]['player1']:
      player_hp = 'hp_player1'
      player_power = 'power_player1'
      player_agility = 'agility_player1'
      player_resistance = 'resistance_player1'
      passive_activation = 'passive_activation_player1'
      enemy_hp = 'hp_player2'
      enemy_power = 'power_player2'
      enemy_agility = 'agility_player2'
      enemy_resistance = 'resistance_player2'
      log_type = 'battle_log'

    elif user_id == context.chat_data[message_id]['player2']:
      player_hp = 'hp_player2'
      player_power = 'power_player2'
      player_agility = 'agility_player2'
      player_resistance = 'resistance_player2'
      passive_activation = 'passive_activation_player2'
      enemy_hp = 'hp_player1'
      enemy_power = 'power_player1'
      enemy_agility = 'agility_player1'
      enemy_resistance = 'resistance_player1'
      log_type = 'battle_log'

  
  elif activity_type == 'explore':
    data_type = context.user_data
    player_hp = 'hp_player1'
    player_power = 'power_player1'
    player_agility = 'agility_player1'
    player_resistance = 'resistance_player1'
    passive_activation = 'passive_activation_player1'
    enemy_hp = 'hp_player2'
    enemy_power = 'power_player2'
    enemy_agility = 'agility_player2'
    enemy_resistance = 'resistance_player2'
    log_type = 'explore_log'

  if 'abilities' in weapon:
    
    if 'momentum' in weapon['abilities']:
      await momentum(update, context, user_id, data_type,player_power, player_agility, enemy_agility,log_type, passive_activation)

    if 'brutal' in weapon['abilities']:
      await brutal(update, context, user_id, data_type,player_power, enemy_resistance,log_type, passive_activation)
      
      
async def activate_passive_ability(update:Update, context:ContextTypes.DEFAULT_TYPE,user_id,activity_type):
  
  user_info = users.find_one({"user_id": user_id})
  user_data = context.user_data
  chat_data = context.chat_data
  equiped_weapon = user_info['equiped_weapon']
  weapon = user_info['user_weapons'][equiped_weapon]
  message_id = update.effective_message.id
  
  if activity_type == 'battle':
    data_type = context.chat_data[message_id]
    if user_id == context.chat_data[message_id]['player1']:
      player_hp = 'hp_player1'
      player_power = 'power_player1'
      player_agility = 'agility_player1'
      player_resistance = 'resistance_player1'
      passive_activation = 'passive_activation_player1'
      enemy_hp = 'hp_player2'
      enemy_power = 'power_player2'
      enemy_agility = 'agility_player2'
      enemy_resistance = 'resistance_player2'
      log_type = 'battle_log'
      
    elif user_id == context.chat_data[message_id]['player2']:
      player_hp = 'hp_player2'
      player_power = 'power_player2'
      player_agility = 'agility_player2'
      player_resistance = 'resistance_player2'
      passive_activation = 'passive_activation_player2'
      enemy_hp = 'hp_player1'
      enemy_power = 'power_player1'
      enemy_agility = 'agility_player1'
      enemy_resistance = 'resistance_player1'
      log_type = 'battle_log'
  
  if activity_type == 'explore':
    data_type = context.user_data
    player_hp = 'hp_player1'
    player_power = 'power_player1'
    player_agility = 'agility_player1'
    player_resistance = 'resistance_player1'
    passive_activation = 'passive_activation_player1'
    enemy_hp = 'hp_player2'
    enemy_power = 'power_player2'
    enemy_agility = 'agility_player2'
    enemy_resistance = 'resistance_player2'
    log_type = 'explore_log'
  
  if not equiped_weapon or equiped_weapon not in user_info['user_weapons']:
    return
  
  elif equiped_weapon:
    
    if 'life_steal' in weapon['passiveabilities'].keys():
      await life_steal(update,context,user_id,data_type,player_hp,enemy_hp,log_type,passive_activation)
        
    if 'more_power' in weapon['passiveabilities'].keys():
      await more_power(update,context,user_id,data_type,player_power,log_type,passive_activation)
        
        
  
async def activate_active_ability(update:Update, context:ContextTypes.DEFAULT_TYPE,user_id,answer,activity_type,data_type):
  
  user_info = users.find_one({'user_id':user_id})
  user_data = context.user_data
  chat_data = context.chat_data
  equiped_weapon = user_info['equiped_weapon']
  weapon = user_info['user_weapons'][equiped_weapon]
  message_id = update.effective_message.id
  
  if activity_type == 'battle':
    if user_id == context.chat_data[message_id]['player1']:
      player_hp = 'hp_player1'
      player_power = 'power_player1'
      player_agility = 'agility_player1'
      player_resistance = 'resistance_player1'
      passive_activation = 'passive_activation_player1'
      enemy_hp = 'hp_player2'
      enemy_power = 'power_player2'
      enemy_agility = 'agility_player2'
      enemy_resistance = 'resistance_player2'
      log_type = 'battle_log'
      
    elif user_id == context.chat_data[message_id]['player2']:
      player_hp = 'hp_player2'
      player_power = 'power_player2'
      player_agility = 'agility_player2'
      player_resistance = 'resistance_player2'
      passive_activation = 'passive_activation_player2'
      enemy_hp = 'hp_player1'
      enemy_power = 'power_player1'
      enemy_agility = 'agility_player1'
      enemy_resistance = 'resistance_player1'
      log_type = 'battle_log'
  
  if activity_type == 'explore':
    player_hp = 'hp_player1'
    player_power = 'power_player1'
    player_agility = 'agility_player1'
    player_resistance = 'resistance_player1'
    passive_activation = 'passive_activation_player1'
    enemy_hp = 'hp_player2'
    enemy_power = 'power_player2'
    enemy_agility = 'agility_player2'
    enemy_resistance = 'resistance_player2'
    log_type = 'explore_log'
  
  actives_activate = {
  'scorching_brand': lambda:scorching_brand(update,context,user_id,equiped_weapon,data_type,enemy_hp,enemy_resistance,log_type),
  'butcher': lambda:butcher(update,context,user_id,equiped_weapon,data_type,enemy_hp,log_type)
}

  if not equiped_weapon or equiped_weapon not in user_info['user_weapons']:
    return
  
  elif equiped_weapon:
    
    if answer in actives_activate.keys():
      await actives_activate[answer]()
    
async def scorching_brand(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id, equiped_weapon, data_type, enemy_hp, enemy_resistance, log_type):
  
  user_info = users.find_one({"user_id": user_id})
  if not user_info:
      return
  
  username = user_info['username']
  equiped_weapon_data = user_info['user_weapons'].get(equiped_weapon, {})
  scorch_power = int(2 * equiped_weapon_data.get('bonus_hp', 0))

  users.update_one(
      {"user_id": user_id},
      {"$addToSet": {"used_abilities": "scorching_brand"}}
  )

  damage = int(scorch_power - min(data_type[enemy_resistance], (scorch_power * 0.5)))
  data_type[enemy_hp] -= damage

  data_type[log_type] += (
      f"<b>{username}</b> used <b>🔥 Scorching Brand</b> and <b>burnt</b> "
      f"the enemy with {damage} power."
  )

  chat_id = update.effective_chat.id
  await context.bot.send_message(
      chat_id=chat_id,
      text=f"""🔥 {username} unleashes the Scorching Brand! 🔥
<blockquote>🌋 Flames erupt from their weapon, searing through the battlefield!
💥 Enemies are engulfed in blazing heat, suffering intense burns.</blockquote>""",
      parse_mode="HTML"
  )


async def life_steal(update:Update, context:ContextTypes.DEFAULT_TYPE,user_id,data_type,player_hp,enemy_hp,log_type,activation):
  
  user_info = users.find_one({'user_id':user_id})
  username = user_info['username']
  user_data = context.user_data
  chat_data = context.chat_data
  
  if data_type[activation] == True:
    return
  
  taken_hp = int( 0.3 * data_type[enemy_hp])
  healed_hp = int( 0.1 * data_type[player_hp])
  
  data_type[enemy_hp] -= int( 0.3 * data_type[enemy_hp])
  data_type[player_hp] += int( 0.1 * data_type[player_hp])
  
  data_type[log_type] += f'<b>{username}</b> slashed the enemy and drained { taken_hp } HP, restoring { healed_hp } HP back ..\n\n'
  
async def more_power(update:Update, context:ContextTypes.DEFAULT_TYPE,user_id,data_type,player_power,log_type,activation):
  
  user_info = users.find_one({'user_id':user_id})
  username = user_info['username']
  user_data = context.user_data
  chat_data = context.chat_data
  
  if data_type[activation] == True:
    return
  
  if random.random() <= 0.40:
    boosted_power = int(0.5 * data_type[player_power])
    data_type[player_power] += boosted_power
    
    data_type[log_type] += f"<b>{username}</b> your weapon  activated More Power 💪! Weapon power increased by 50% !\n\n"
  
async def momentum(update:Update, context:ContextTypes.DEFAULT_TYPE,user_id,data_type,player_power,player_agility,enemy_agility,log_type,activation):
  
  user_info = users.find_one({'user_id':user_id})
  username = user_info['username']
  user_data = context.user_data
  chat_data = context.chat_data
  
  if data_type[activation] == True:
    return
  
  if data_type[player_agility] > data_type[enemy_agility]:
    boosted_power = int(0.8 * data_type[player_power])
    data_type[player_power] += boosted_power
    
    data_type[log_type] += f"<b>{username}</b> has greater <b>agility</b>.\nMomentum 🌀 activated.. Boosted <b>power</b> by 80%.!\n\n"
    
async def brutal(update:Update, context:ContextTypes.DEFAULT_TYPE,user_id,data_type,player_power,enemy_resistance,log_type,activation):
  
  user_info = users.find_one({'user_id':user_id})
  username = user_info['username']
  user_data = context.user_data
  chat_data = context.chat_data
  
  if data_type[activation] == True:
    return
  
  data_type[player_power] += int(min(data_type[enemy_resistance],(data_type[player_power])))
  data_type[log_type] += f'<b>{username}</b>, your weapon is immune to enemy resistence.\n\n'
  
async def butcher(update:Update, context:ContextTypes.DEFAULT_TYPE,user_id,equiped_weapon,data_type,enemy_hp,log_type):
  
  user_info = users.find_one({'user_id':user_id})
  user_data = context.user_data
  chat_data = context.chat_data
  username = user_info['username']
  equiped_weapon_data = user_info['user_weapons'][equiped_weapon]
  
  users.update_one(
    {"user_id": user_id},
    {"$addToSet": {"used_abilities": "butcher"}}
)
  
  data_type[enemy_hp] -= data_type[enemy_hp] - 1 
  
  data_type[log_type] += f'<b>{username}</b> used Butcher.\nEnemy HP reduced to {data_type[enemy_hp]}.\n\n'
  
  chat_id = update.effective_chat.id
  msg = await context.bot.send_message(
    chat_id = chat_id,
    text = f'''🔪 {username} butchered the enemy!! 
<blockquote>The Butcher’s strike carves deep — leaving only scraps of life behind!</blockquote>''',
parse_mode = 'HTML')
  

actives = {
  'scorching_brand':scorching_brand,
  'life_steal':life_steal,
  'more_power':more_power,
  'momentum':momentum,
  'brutal':brutal,
  'butcher':butcher,
}


def add_ability_to_all_weapons(weapon_name,ability,ability_name,ability_data):
  weapon = all_weapon_list[weapon_name]
  if weapon:
    weapon[ability][ability_name] = ability_data
    
def add_ability_to_weapons(weapon_name,ability,ability_name,ability_data):
  weapon = weapon_list[weapon_name]
  if weapon:
    weapon[ability][ability_name] = ability_data
    
add_ability_to_all_weapons('Void Edge','passiveabilities','life_steal',{'name': 'Life Steal','description':'Takes opponent\'s 30% HP and heals 10% HP every round.'})


    
#reset_all
async def reset_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_id = update.effective_message.from_user.id

  if user_id not in ADMINS:
      await update.message.reply_text("❌ You are not authorized to use this command.")
      return
    
  users.delete_many({})  

  await update.message.reply_text("✅ All user data has been reset.")


def escape_markdown(text: str) -> str:
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', text) 
  
  
 #players stats 
def get_player_stats(update,context,user_id):
  user_info = users.find_one({'user_id':user_id})
  equiped_weapon = user_info['equiped_weapon']
    
  if not equiped_weapon or equiped_weapon not in user_info['user_weapons']:
    player_stats = {
      'total_hp' : user_info['hp'],
      'user_battle_power' : user_info['power'],
      'user_battle_agility' : user_info['agility'],
      'user_battle_resistance' : user_info['resistance']
    }
    return player_stats
  else:
    player_stats = {
      'total_hp' : user_info['hp'] + user_info['user_weapons'][equiped_weapon]['bonus_hp'],
      'user_battle_power' : user_info['power'] + user_info['user_weapons'][equiped_weapon]['bonus_power'],
      'user_battle_agility' : user_info['agility'] + user_info['user_weapons'][equiped_weapon]['bonus_agility'],
      'user_battle_resistance' : user_info['resistance'] + user_info['user_weapons'][equiped_weapon]['bonus_resistance']
    }
    return player_stats


#reset_user
async def reset_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_id = get_target_user_id(update)
  
  if update.effective_user.id not in ADMINS:
    await update.message.reply_text("❌ You are not authorized to use this command.")
    return

  if not context.args:
    await update.message.reply_text("⚠️ Please give a user ID.\nExample: `/reset_user 123456789`", parse_mode='Markdown')
    return

  try:
    reset_user_id = int(context.args[0]) 
    user_exists = users.find_one({"user_id": reset_user_id})

    if user_exists:
      users.delete_one({"user_id": reset_user_id})
      await update.message.reply_text(
          f"✅ User `{reset_user_id}` has been removed!", parse_mode="Markdown"
      )
    else:
      await update.message.reply_text("⚠️ User not found in database.")

  except Exception as e:
    await update.message.reply_text(f"❌ Invalid ID! Error: `{e}`", parse_mode="Markdown")
        
def get_target_user_id(update):
  if update.message and update.message.reply_to_message:
      return update.message.reply_to_message.from_user.id
  return update.effective_user.id
    
#xp           
async def xp_system(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int, amount: int):
  
  user_info = users.find_one({"user_id": user_id})
  if not user_info:
      return

  username = user_info.get("username", "Unknown")
  leveled_up = False

  if user_info["level"] >= 100:
      return

  user_info["xp"] += amount * user_info["level"]

  while user_info["xp"] >= user_info["max_xp"]:
    user_info["xp"] -= user_info["max_xp"]
    user_info["level"] += 1
    user_info["max_xp"] += 50 * user_info["level"]

    user_info["hp"] += int(user_info["max_hp"] * 0.2)
    user_info["power"] += int(user_info["max_power"] * 0.2)
    user_info["agility"] += int(user_info["max_agility"] * 0.2)
    user_info["resistance"] += int(user_info["max_resistance"] * 0.2)

    leveled_up = True

  users.update_one({"user_id": user_id}, {"$set": user_info})

  if leveled_up:
    await context.bot.send_message(
        chat_id=user_id,
        text=f"""🌟 Level Up! 🌟  
Congratulations, @{username}!

<blockquote>    
🧍 You’ve reached <b>Level {user_info['level']}</b>!  
Keep exploring, battling, and rising to greatness!
</blockquote>""",
        parse_mode=ParseMode.HTML,
    )

async def weapon_xp_system(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int, amount: int):
    # ✅ Fetch user info from MongoDB
  user_info = users.find_one({"user_id": user_id})
  if not user_info:
      return  # no user in DB

  username = user_info.get("username", "Unknown")
  equipped_weapon = user_info.get("equiped_weapon")

  if not equipped_weapon or equipped_weapon not in user_info["user_weapons"]:
      return  # no weapon equipped

  weapon = user_info["user_weapons"][equipped_weapon]

  # ✅ Stop if already max level
  if weapon["weapon_level"] >= 100:
      return

  # ✅ Increase XP (your formula)
  weapon["weapon_xp"] += amount * weapon["weapon_level"]

  # ✅ Level-up loop
  leveled_up = False
  while weapon["weapon_xp"] >= weapon["weapon_max_xp"]:
      weapon["weapon_xp"] -= weapon["weapon_max_xp"]
      weapon["weapon_level"] += 1
      weapon["weapon_max_xp"] += 40 * weapon["weapon_level"]
      weapon["bonus_hp"] += int(weapon["base_hp"] * 0.2)
      weapon["bonus_power"] += int(weapon["base_power"] * 0.2)
      weapon["bonus_agility"] += int(weapon["base_agility"] * 0.2)
      weapon["bonus_resistance"] += int(weapon["base_resistance"] * 0.2)
      leveled_up = True


  users.update_one(
      {"user_id": user_id},
      {"$set": {f"user_weapons.{equipped_weapon}": weapon}}
  )
  
  if leveled_up:
    await context.bot.send_message(
      chat_id=user_id,
      text=f'''⚔️✨ Your weapon has leveled up! @{username} ✨⚔️

<blockquote>
🔹 <b>Name:</b> {equipped_weapon}  
🔹 <b>New Level:</b> {weapon["weapon_level"]}
🔹 <b>Weapon XP:</b> {weapon["weapon_xp"]} / {weapon["weapon_max_xp"]}
</blockquote>
🔥 Keep battling to make it even stronger!''',
        parse_mode=ParseMode.HTML
    )
  
#start    

async def start(update:Update, context:ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_info = users.find_one({'user_id':user_id})
    user_data = context.user_data
    username = user_info['username']
    
    images = [
    "https://files.catbox.moe/x4ah5l.jpg",  # Replace with actual file_id or direct URL
    "https://files.catbox.moe/lt70jg.jpg"
]

    chosen_image = random.choice(images)

    caption = f"""
━━━━━━━━━━━━━━━━━━━━━━
🌌 <b>WELCOME TO THE REALM</b> 🌌
━━━━━━━━━━━━━━━━━━━━━━

👤 <b>User:</b> <code>@{username}</code>

<blockquote>
You awaken beneath a fading sky, the scent of old magic thick in the air...
Ancient whispers call your name — the realm has been waiting.

From forgotten ruins to shadowed forests, from arcane towers to cursed seas...
your path is unwritten, your legacy yet to form.

Will you rise as a hero, fall as a legend, or vanish in silence?
</blockquote>
━━━━━━━━━━━━━━━━━━━━━━
📝 <i>The journey begins — may your choices echo through eternity.</i>
━━━━━━━━━━━━━━━━━━━━━━
"""

    await update.message.reply_photo(
    photo=chosen_image,
    caption=caption,
    parse_mode=ParseMode.HTML)
    
    
#help
async def help(update:Update, context:ContextTypes.DEFAULT_TYPE):
    user_id = get_target_user_id(update)
    user_info = users.find_one({'user_id':user_id})
    user_data = context.user_data
    
    await update.message.reply_text(
    """<b>🤖 Bot Command List</b>
━━━━━━━━━━━━━━━━━━━━━━

Here are all your commands:

<blockquote>
• <code>/start</code> – 🌟 <i>Begin your journey!</i>
• <code>/mystats</code> – 🧍‍♂️ <i>View your full character profile</i>
• <code>/explore</code> – 🧭 <i>Go on an adventure and fight monsters</i>
• <code>/guess</code> – 🎯 <i>Play the number guessing game to win coins</i>
• <code>/toss</code> – 🎲 <i>Toss a coin and test your luck</i>
• <code>/shop</code> – 🛒 <i>Buy Essences, weapons, and more</i>
• <code>/weapons</code> – 🛡️ <i>See all available weapons in the shop</i>
• <code>/myinventory</code> – 🎒 <i>Check your collected items</i>
• <code>/mygear</code> – ⚔️ <i>View your equipped battle gear</i>
• <code>/battle</code> – ⚔️ <i>Challenge another player to a PvP battle</i>
• <code>/battle_leaderboard</code> – 🏆 <i>View the top battle players</i>
• <code>/view &lt;weapon&gt;</code> – 🔍 <i>See detailed stats of a weapon</i>
• <code>/give</code> – 🎁 <i>Give an item to another user</i>
• <code>/help</code> – ❓ <i>Show this help message again</i>
</blockquote>
━━━━━━━━━━━━━━━━━━━━━━
<b>✨ Enjoy your adventure, hero!</b>
<i>The realm awaits your next move...</i>
""",
    parse_mode=ParseMode.HTML
)

async def attack_enemy(update:Update, context:ContextTypes.DEFAULT_TYPE,data_type,player_name,enemy_hp,player_power,enemy_resistance,log_type):
  
  user_data = context.user_data
  chat_data = context.chat_data
  
  data_type[enemy_hp] -= int(data_type[player_power] - min(data_type[enemy_resistance],(data_type[player_power] * 0.5)))
  
  data_type[log_type] += f"<b>{data_type[player_name]}</b> dealt <b>{int(data_type[player_power] - min(data_type[enemy_resistance],(data_type[player_power] * 0.5)))}</b> damage!\n\n"
  
#explore 
async def explore(update:Update, context:ContextTypes.DEFAULT_TYPE):
    
    
    user_id = update.effective_message.from_user.id
    user_info = users.find_one({'user_id':user_id})
    user_data = context.user_data
    
    
    if update.message.chat.type != 'private':
        update.message.reply_text("❌ Use this command in DM!")
        return
        
    all_monsters = list(monsters.find({}))
    
    chosen_monster = random.choice(all_monsters) 
    current_monster_id = chosen_monster['monster_id']
    current_monster = chosen_monster['name']
    context.user_data['current_monster'] = current_monster.title()
    context.user_data['current_monster_id'] = current_monster_id
    
    monster_info = init_monster(update,context,current_monster_id)
    
    users.update_one(
    {"user_id": user_id},
    {"$inc": {"explores_played": 1}}  
)
    
    if user_info['level'] <=3 :
      starting_level = 1
    else :
      starting_level = user_info['level'] - 1
      
    
    
    context.user_data['monster_hp'] = monster_info['hp']
    context.user_data['monster_dmg'] = monster_info['dmg']
    context.user_data['monster_agility'] = monster_info['agility']
    monster_photo = monster_info['photo']
    monster_level = random.randint(starting_level,int(user_info['level']))
    context.user_data['monster_level'] = monster_level
    context.user_data['monster_hp'] = int(context.user_data['monster_hp'] * (monster_level * 0.2))
    context.user_data['monster_dmg'] = int(context.user_data['monster_dmg'] * (monster_level * 0.2))
    context.user_data['monster_agility'] = int(context.user_data['monster_agility'] * (0.2 * monster_level))
    keyboard = [
    [InlineKeyboardButton('⚔️ Hunt the Monster', callback_data='hunt')]
]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_photo(
    photo=monster_photo,
    caption=f"""
🌫️ The air thickens with mystery...
⚠️ You feel a powerful presence nearby.

━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
✨ <b>A Wild {current_monster} Has Appeared!</b> ✨
<b>Level:</b> <code>{monster_level}</code>

<b>Monster HP:</b> {context.user_data['monster_hp']}
<b>Monster Power:</b> {context.user_data['monster_dmg']}
<b>Monster Agility:</b> {context.user_data['monster_agility']}

🧝 <b>Brave adventurer</b>, what will you do?
</blockquote>
━━━━━━━━━━━━━━━━━━━━━━
⚔️ <b>Hunt</b> — Face the beast head-on
━━━━━━━━━━━━━━━━━━━━━━
""",
    reply_markup=reply_markup,
    parse_mode=ParseMode.HTML
)
async def explore_button(update:Update, context:ContextTypes.DEFAULT_TYPE):
  user_id = update.effective_user.id
  user_info = init_user(update, context, user_id)
  user_data = context.user_data
  equiped_weapon = user_info['equiped_weapon']
  
  
  query = update.callback_query
  await query.answer()
  if 'current_monster' not in context.user_data:
    await query.answer('The monster fled!', show_alert = False)
    return
  explore_option= query.data
  
  
  
  if explore_option == 'hunt':
    
    current_monster_id = context.user_data['current_monster_id']
    current_monster = context.user_data['current_monster']
    monster_hp = context.user_data['monster_hp']
    monster_dmg = context.user_data['monster_dmg']
    monster_agility = context.user_data['monster_agility']
    
    player_stats = get_player_stats(update,context,user_id)
    total_hp = player_stats['total_hp']
    user_battle_power = player_stats['user_battle_power']
    user_battle_agility = player_stats['user_battle_agility']
    user_battle_resistance =player_stats['user_battle_resistance']
    
    context.user_data.update({
      'player1':user_id,
      'player2':current_monster_id,
      'player1_name':user_info['username'],
      'player2_name':current_monster,
      'hp_player1':total_hp,
      'hp_player2':monster_hp,
      'power_player1':user_battle_power,
      'power_player2':monster_dmg,
      'agility_player1':user_battle_agility,
      'agility_player2':monster_agility,
      'resistance_player1':user_battle_resistance,
      'resistance_player2':0,
      'max_hp_player1':total_hp,
      'max_hp_player2':monster_hp,
      'passive_activation_player1':False,
      'passive_activation_player2':False,
      'explore_log':'',
      'round':0,
      'player1_revived':False,
      'player2_revived':False,
      'player1_weapon':equiped_weapon,
      'player2_weapon':None,
    })
    
    await activate_pre_battle_ability(update,context,user_id,'explore')
    
    await query.edit_message_caption(
      caption = (
      f'''
⚔️─────────────⚔️
        
<b>You chose to attack the {current_monster}!</b>
         
───────────────

<blockquote>👾 <b>Monster HP:</b> {monster_hp}
💥 <b>Monster Damage:</b> {monster_dmg}
⚡ <b>Monster Agility:</b> {monster_agility}
</blockquote>        
───────────────
🔥<b> Prepare for battle!</b>
⚔️ <b>Attack</b> — Face the beast head-on  
🚶 <b>Retreat</b> — Live to fight another day
⚔️─────────────⚔️
    '''),
    parse_mode = ParseMode.HTML,
    reply_markup = get_explore_keyboard(update,context,user_id,equiped_weapon)
  )
        
async def button(update:Update, context:ContextTypes.DEFAULT_TYPE):
  
  user_id = update.effective_user.id
  user_info = users.find_one({'user_id':user_id})
  user_data = context.user_data
  
  
  query = update.callback_query
  await query.answer()
  
  chat_id = query.message.chat_id
  message_id = query.message.message_id
  
  if 'player2_name' not in context.user_data:
    await query.answer('The monster fled')
    return
  
  action = query.data
  parts = action.split('_')
  context.user_data['answer'] = '_'.join(parts[1:])
  answerexplore = context.user_data['answer']
  
  equiped_weapon = context.user_data['player1_weapon']
  
  if answerexplore == 'attack':
    
    if context.user_data['agility_player1'] >= context.user_data['agility_player2']:
      await attack_enemy(update,context,context.user_data,'player1_name','hp_player2','power_player1','resistance_player2','explore_log')
      
      if context.user_data['hp_player2'] > 0:
        await attack_enemy(update,context,context.user_data,'player2_name','hp_player1','power_player2','resistance_player1','explore_log')
          
          
    if context.user_data['agility_player1'] < context.user_data['agility_player2']:
      await attack_enemy(update,context,context.user_data,'player2_name','hp_player1','power_player2','resistance_player1','explore_log')
      
      if context.user_data['hp_player1'] > 0:
        await attack_enemy(update,context,context.user_data,'player1_name','hp_player2','power_player1','resistance_player2','explore_log')
    
    await activate_passive_ability(update,context,user_id,'explore')
    
  elif answerexplore == 'focus':
    
    if context.user_data['agility_player1'] >= context.user_data['agility_player2']:
      context.user_data['resistance_player1'] += int(0.5 * context.user_data['resistance_player1'])
      context.user_data['power_player1'] += int(0.1 * context.user_data['power_player1'])
      
      context.user_data['explore_log'] += f"👤 You used Focus 🛡️ your Resistance and Power is increased !\n"
      
      if context.user_data['hp_player2'] > 0:
        await attack_enemy(update,context,context.user_data,'player2_name','hp_player1','power_player2','resistance_player1','explore_log')
        
        
    if context.user_data['agility_player1'] < context.user_data['agility_player2']:
      await attack_enemy(update,context,context.user_data,'player2_name','hp_player1','power_player2','resistance_player1','explore_log')
      
      if context.user_data['hp_player1'] > 0:
        
        context.user_data['resistance_player1'] += int(0.5 * context.user_data['resistance_player1'])
        context.user_data['power_player1'] += int(0.1 * context.user_data['power_player1'])
      
        context.user_data['explore_log'] += f"👤 You used Focus 🛡️ your Resistance and Power is increased !\n"
    
    
  elif answerexplore == 'retreat':
    await query.edit_message_caption(
      caption =
"""🚶‍♂️ <b>You Chose to Retreat</b>
━━━━━━━━━━━━━━━━━━━━━━  

<blockquote>
Sometimes, retreat is the wisest choice.  
Your journey doesn’t end here...
</blockquote>
📜 <i>Live to fight another day, brave soul.</i>  
━━━━━━━━━━━━━━━━━━━━━━""",
parse_mode=ParseMode.HTML
)
    context.user_data.clear()
    
    db.users.update_one(
    {"user_id": user_id},
    {"$set": {"used_abilities": []}}
)
    return
  
  
  else:
    
    if 'used_abilities' not in user_info.keys():

      users.update_one(
          {"user_id": user_id},
          {"$set": {"used_abilities": []}}
      )
      user_info = users.find_one({"user_id": user_id})
    
    user_info = users.find_one({'user_id':user_id})
    
    
    if context.user_data['agility_player1'] >= context.user_data['agility_player2']:
      await activate_active_ability(update,context,user_id,answerexplore,'explore',context.user_data)
      
      if context.user_data['hp_player2'] > 0:
        await attack_enemy(update,context,context.user_data,'player2_name','hp_player1','power_player2','resistance_player1','explore_log')
        
      user_info = users.find_one({'user_id':user_id})
      
    await activate_passive_ability(update,context,user_id,'explore')
          
    if context.user_data['agility_player1'] < context.user_data['agility_player2']:
      await attack_enemy(update,context,context.user_data,'player2_name','hp_player1','power_player2','resistance_player1','explore_log')
      
      if context.user_data['hp_player1'] > 0:
        await activate_active_ability(update,context,user_id,answerexplore,'explore',context.user_data)
        
      user_info = db.get(UserQuery.user_id == user_id)
      
    await activate_passive_ability(update,context,user_id,'explore')
    
  if context.user_data['hp_player1'] > context.user_data['max_hp_player1']:
    context.user_data['hp_player1'] = context.user_data['max_hp_player1']
  
  if context.user_data['hp_player2'] > context.user_data['max_hp_player2']:
    context.user_data['hp_player2'] = context.user_data['max_hp_player2']
    
  if context.user_data['hp_player2'] <= 0:
    await explore_win_msg(update,context,user_id,chat_id,message_id)
    return 
  
  elif context.user_data['hp_player1'] <= 0:
    
    if not equiped_weapon or equiped_weapon not in user_info['user_weapons']:
      await explore_lose_msg(update,context,user_id,chat_id,message_id)
      return 
    
    else:
      if context.user_data['player1_revived'] == True:
        await explore_lose_msg(update,context,user_id,chat_id,message_id)
        return 
    
      elif context.user_data['player1_revived'] == False:
        context.user_data['hp_player1'] = user_info['hp']
        context.user_data['power_player1'] = user_info['power']
        context.user_data['agility_player1'] = user_info['agility']
        context.user_data['resistance_player1'] = user_info['resistance']
        
        if 'used_abilities' not in user_info.keys():
          db.users.update_one(
            {"user_id": user_id}, 
            {"$set": {"used_abilities": []}}  
        )
        
        db.users.update_one(
          {"user_id": user_id}, 
          {"$push": {"used_abilities": {"$each": list(actives.keys())}}}
      )
        context.user_data['passive_activation_player1'] = True
        
        user_info = users.find_one({'user_id':user_id})
        
        context.user_data['explore_log'] = f'<b>{user_info['username']}</b> your weapon broke !!! \nYou are down to your last remaining power \n\n'
        context.user_data['player1_revived'] = True 
        
        
  
  
  reply_markup5 = get_explore_keyboard(update,context,user_id,context.user_data['player1_weapon'])
  
  await query.edit_message_caption(
    caption =
f"""⚔️ <b>Attack Turn</b>  
━━━━━━━━━━━━━━━━━━━━━━  

{context.user_data['explore_log']}
━━━━━━━━━━━━━━━━━━━━━━  

<blockquote>
📉 <b>{context.user_data['player2_name']}'s HP:</b> <code>{context.user_data['hp_player2']}</code>  
❤️ <b>Your HP:</b> <code>{context.user_data['hp_player1']}</code>
</blockquote>
━━━━━━━━━━━━━━━━━━━━━━""",
reply_markup=reply_markup5,
parse_mode=ParseMode.HTML
)
  context.user_data['explore_log'] = ''

def get_explore_keyboard(update, context, user_id, equiped_weapon):
  
    user_info = users.find_one({'user_id':user_id})
    
    used_abilities = user_info.get('used_abilities', [])
    
    active_buttons = []
    for btn_row in active_ability_keyboard(update, context, user_id, equiped_weapon, 'explore'):
      
        filtered_row = [
            btn for btn in btn_row
            if btn.callback_data.split('_', 1)[1] not in used_abilities
        ]
        if filtered_row:
            active_buttons.append(filtered_row)

    explore_keyboard = [
        [InlineKeyboardButton('⚔️ Attack', callback_data='explore_attack'),InlineKeyboardButton('Focus 🛡️',callback_data='explore_focus')],
        *active_buttons,
        [InlineKeyboardButton('🚶 Retreat Silently', callback_data='explore_retreat')]
    ]

    return InlineKeyboardMarkup(explore_keyboard)     
    
    
async def explore_win_msg(update:Update, context:ContextTypes.DEFAULT_TYPE,user_id,chat_id,message_id):
  
  user_info = db.users.find_one({"user_id": user_id})
  equiped_weapon = user_info.get("equiped_weapon")

  db.users.update_one(
      {"user_id": user_id},
      {
        "$inc": {
            "coins": 20 * context.user_data['monster_level'],
            "explores_won": 1
        },
        "$set": {"used_abilities": []}
      }
  )

  await xp_system(update, context, user_id, 15)
  xp_gained = 15 * user_info['level']

  weapon_xp_msg, weapon_xp_gained = "", ""
  if equiped_weapon and equiped_weapon in user_info.get("user_weapons", {}):
      await weapon_xp_system(update, context, user_id, equiped_weapon, 20)
      weapon_xp_gained = 20*user_info['user_weapons'][equiped_weapon]['weapon_level']
      weapon_xp_msg = f'<b>🗡️ Weapon XP Gained: +</b>'

  await context.bot.edit_message_caption(
      chat_id=chat_id,
      message_id=message_id,
      caption=f"""⚔️ <b>Battle Log</b>  
━━━━━━━━━━━━━━━━━━━━━━  

{context.user_data['explore_log']}

🏆 <b>Victory!</b>  
━━━━━━━━━━━━━━━━━━━━━━  
You defeated <b>{context.user_data['current_monster']}</b> in a fierce battle!

<blockquote>
🪙 <b>Coins Earned:</b> +{20 * user_info['level']}
✨ <b>XP Gained:</b> +{xp_gained}
{weapon_xp_msg}{weapon_xp_gained}
</blockquote>   
━━━━━━━━━━━━━━━━━━━━━━  
🎮 Use /explore to battle more monsters!""",
      parse_mode=ParseMode.HTML
  )

  context.user_data.clear()
  

async def explore_lose_msg(update:Update, context:ContextTypes.DEFAULT_TYPE,user_id,chat_id,message_id):
  
  user_info = db.users.find_one({"user_id": user_id})
  if not user_info:
      return
  
  equiped_weapon = user_info.get("equiped_weapon")

  db.users.update_one(
      {"user_id": user_id},
      {
          "$inc": {"coins": -10, "explores_lost": 1},
          "$set": {"used_abilities": []}
      }
  )


  xp_gained = 5 * user_info["level"]
  await xp_system(update, context, user_id, xp_gained)

  if not equiped_weapon or equiped_weapon not in user_info.get("user_weapons", {}):
      weapon_xp_msg = ""
      weapon_xp_gained = ""
  else:
      await weapon_xp_system(update, context, user_id, 10)
      weapon_xp_msg = "<b>Weapon XP Gained: +</b> "
      weapon_xp_gained = 10 * user_info["user_weapons"][equiped_weapon]["weapon_level"]


  await context.bot.edit_message_caption(
      chat_id=chat_id,
      message_id=message_id,
      caption=f"""⚔️ <b>Battle Log</b>  
━━━━━━━━━━━━━━━━━━━━━━  

{context.user_data['explore_log']}

💀 <b>Defeat...</b>  
━━━━━━━━━━━━━━━━━━━━━━  
You fought bravely, but <b>{context.user_data['current_monster']}</b> was too strong.

<blockquote>
🧍‍♂️ You have fallen in battle.  
🪙 <b>Coins Lost:</b> 10  
✨ <b>XP Gained:</b> +{xp_gained}
{weapon_xp_msg}{weapon_xp_gained}
</blockquote>
━━━━━━━━━━━━━━━━━━━━━━  
🔁 Use /explore to try again and redeem your honor!
""",
      parse_mode=ParseMode.HTML
  )

  context.user_data.clear()
  
  
#inventory
async def inventory(update:Update, context:ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    user_info = init_user(update, context, user_id)
    username = user_info['username'] or user_info['first_name']

    inv_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⚔️ Weapons", callback_data=f'inv_weapons_{user_id}'),
            InlineKeyboardButton("✨ Magical Items", callback_data=f'inv_magic_{user_id}')
        ]
    ])

    await update.message.reply_text(
        f"""<b>👤 Your Inventory</b>

<code>Username:</code> <code>{username}</code>

━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
💰 <b>Coins:</b> {user_info['coins']}
🔮 <b>Essences:</b> {user_info['essences']}
🐚 <b>Moonshards:</b> {user_info['moonshards']}
</blockquote>
━━━━━━━━━━━━━━━━━━━━━━""",
        parse_mode=ParseMode.HTML,
        reply_markup=inv_markup
    )


async def inv_button(update:Update, context:ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data  # e.g. "inv_weapons_123456789"
    parts = data.split('_')

    # Example: parts = ['inv', 'weapons', '123456789']
    if len(parts) < 3:
        await query.answer("Invalid data!", show_alert=True)
        return

    inv_type = parts[1]      # 'weapons' or 'magic' or 'main'
    allowed_user_id = int(parts[2])
    pressing_user = query.from_user.id

    if pressing_user != allowed_user_id:
        await query.answer("Not You!", show_alert=False)
        return

    user_info = init_user(update, context, allowed_user_id)
    username = user_info['username'] or user_info['first_name']

    if inv_type == 'weapons':
        inv_weapons_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📦 Inventory", callback_data=f'inv_main_{allowed_user_id}'),
                InlineKeyboardButton("✨ Magical Items", callback_data=f'inv_magic_{allowed_user_id}')
            ]
        ])

        if not user_info['user_weapons']:
            await query.edit_message_text(
    text='''
⚔️ <b>Weapon Inventory</b>
━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
You open your worn-out satchel... 🧳
<i>It's empty... for now.</i>

You haven’t discovered any weapons yet.
Explore the world or win battles to find powerful gear!
</blockquote>
━━━━━━━━━━━━━━━━━━━━━━
''',
    parse_mode=ParseMode.HTML,
    reply_markup=inv_weapons_markup
)
        else:
            user_wp_list = "\n".join([f"🗡️ {wp}" for wp in user_info["user_weapons"].keys()])
            message = f"""
🧰 <b>YOUR INVENTORY</b>

✨ Here are all your equipped and owned weapons:

━━━━━━━━━━━━━━━━━━━━

<blockquote>
{user_wp_list}
</blockquote>
━━━━━━━━━━━━━━━━━━━━

💡 <b>Tip:</b> Use /mygear to view your equipped weapon!
"""
            await query.edit_message_text(
                message,
                reply_markup=inv_weapons_markup,
                parse_mode=ParseMode.HTML
            )

    elif inv_type == 'magic':
        inv_magic_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📦 Inventory", callback_data=f'inv_main_{allowed_user_id}'),
                InlineKeyboardButton("⚔️ Weapons", callback_data=f'inv_weapons_{allowed_user_id}')
            ]
        ])
        await query.edit_message_text(
            text="""
✨ <b>Magical Items</b>
━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
You gaze into your enchanted pouch... 🔮
<i>But it's silent and empty...</i>

No magical items have been discovered yet.
Seek out mystical places, defeat bosses, or unlock ancient chests!
</blockquote>
━━━━━━━━━━━━━━━━━━━━━━
""",
            parse_mode=ParseMode.HTML,
            reply_markup=inv_magic_markup
        )

    elif inv_type == 'main':
        inv_main_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⚔️ Weapons", callback_data=f'inv_weapons_{allowed_user_id}'),
                InlineKeyboardButton("✨ Magical Items", callback_data=f'inv_magic_{allowed_user_id}')
            ]
        ])
        await query.edit_message_text(
            f"""<b>👤 Your Inventory</b>

<code>Username:</code> <code>{username}</code>

━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
💰 <b>Coins:</b> {user_info['coins']}
🔮 <b>Essences:</b> {user_info['essences']}
🐚 <b>Moonshards:</b> {user_info['moonshards']}
</blockquote>
━━━━━━━━━━━━━━━━━━━━━━""",
            parse_mode=ParseMode.HTML,
            reply_markup=inv_main_markup
        )

    else:
        await query.answer("Unknown command!", show_alert=True)

BUY_WEAPON = range(1)
CHOOSE_QUANTITY = range(1)

async def cancel(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Purchase cancelled. You can /shop again anytime!")
    return ConversationHandler.END
    
#shop
async def shop(update:Update, context:ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_info = init_user(update, context, user_id)
  
    if update.message.chat.type != 'private':
        await update.message.reply_text("❌ Use this command in DM!")
        return
  
    image = "AgACAgUAAxkBAAIPKWiWR8bCk2-C5LXjUr6jLKdjoTnUAAKf0zEb5V-wVFwym1zA70KmAQADAgADeAADNgQ"  # Replace with your image URL or file_id

    caption = f"""
━━━━━━━━━━━━━━━━━━━━━━  
🏪 <b>THE GRAND SHOP</b>  
━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
Step into a world of trades and treasures.  
Choose where you want to browse:
</blockquote>
<blockquote>
🪙 <b>Resource Shop</b>  
Buy <i>Moonshards</i> and rare <i>Essences</i> to boost your power.
</blockquote>
<blockquote>
🗡️ <b>Weapon Shop</b>  
<i>Buy Amazing And powerful Weapons to increase your gear power</i>
</blockquote>
<blockquote>
⭐ <b>Magic Shop</b>  
🔒 Locked — <i>Coming soon...</i>
</blockquote>
━━━━━━━━━━━━━━━━━━━━━━  
<blockquote>
📜 <i>New shops will open as your journey unfolds...</i>
</blockquote>
"""

    keyboard7 = [
    [InlineKeyboardButton("🎒 Resource Shop", callback_data="resource_shop")],
    [InlineKeyboardButton("🛡️ Weapon Shop", callback_data="weapon_shop")],
    [InlineKeyboardButton("🌟 Magic Shop", callback_data="magic_shop")]
    
]

    reply_markup7 = InlineKeyboardMarkup(keyboard7)

    await update.message.reply_photo(
        photo=image,
        caption=caption,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup7
    )

async def button2(update:Update, context:ContextTypes.DEFAULT_TYPE):
    
    user_id = update.effective_user.id
    user_info = init_user(update, context, user_id)
    user_data = context.user_data
    
    query = update.callback_query
    await query.answer()
    context.user_data['chosen_shop'] = query.data
    
    if context.user_data['chosen_shop'] == 'resource_shop':
      keyboard4 = [
        [InlineKeyboardButton('💥 Buy Essences (1000 🪙)', callback_data='essences')],
        [InlineKeyboardButton('🧿 Buy Moonshards (10000 🪙)', callback_data='moonshards')]
    ]
      reply_markup2 = InlineKeyboardMarkup(keyboard4)
      
      await query.edit_message_caption(
      caption = """
🎒 <b>Resource Shop</b>  
━━━━━━━━━━━━━━━━━━━━━━  
Here you'll find rare materials that fuel your journey:  

<blockquote>
🪙 Coins — Common trade currency  
🔮 Essences — Crystallized magical energy  
🐚 Moonshards — Fragments of ancient power
</blockquote>
💡 <i>Spend wisely, traveler. These items are more than they appear...</i>
"""
    ,reply_markup = reply_markup2,
    parse_mode=ParseMode.HTML
)
 
      
      
    elif context.user_data['chosen_shop'] == 'weapon_shop':
      await query.edit_message_caption(
        caption = """
⚔️ <b>Welcome to the Weapon Shop!</b> ⚔️

<blockquote>
Here, you can find powerful weapons to aid you on your adventures. Choose wisely and prepare for battle!
</blockquote>
<blockquote>
Please send the name of the weapon you want to buy.
</blockquote>
<blockquote>
To see the full list of available weapons anytime, just use the command:
/weapons
</blockquote>
━━━━━━━━━━━━━━━━━━━━━━
📝 Use /cancel to cancel the purchase.
""",
parse_mode  = ParseMode.HTML)

      return BUY_WEAPON 
      

    elif context.user_data['chosen_shop'] == 'magic_shop':
      await query.edit_message_caption(
    caption = """
✨ <b>Magic Shop - Not Yet Awakened</b> ✨  
━━━━━━━━━━━━━━━━━━━━━━  

<blockquote>
📦 Enchanted tomes remain sealed...  
🔮 Mystic lights flicker behind dusty shelves...  
🧙‍♂️ The magician has yet to return from his arcane journey.
</blockquote>
📜 <i>Patience, young adventurer — true magic takes time.</i>  
━━━━━━━━━━━━━━━━━━━━━━
""",
    parse_mode=ParseMode.HTML
)

async def button7(update:Update, context:ContextTypes.DEFAULT_TYPE):
  user_id = update.effective_user.id
  user_info = init_user(update, context, user_id)
  user_data = context.user_data
  
  query = update.callback_query
  await query.answer()
  
  context.user_data['item_to_buy'] = query.data
  item_name = context.user_data.get("item_to_buy", "Unknown Item")
  currency_emoji = '🪙'
  item_to_buy = context.user_data['item_to_buy']

  if item_to_buy == "essences":
    item_price = 1000
  elif item_to_buy == "moonshards":
    item_price = 10000
    
  await query.edit_message_caption(
    caption = (f"""
🛒 <b>Purchase Menu</b>  
━━━━━━━━━━━━━━━━━━━━━━  

<blockquote>
✨ You have selected: <b>{item_name}</b>  
💰 <b>Price:</b> {item_price} {currency_emoji} per unit  
📦 <b>Stock:</b> Unlimited
</blockquote>
🧮 <i>How many would you like to buy?</i>  
<b>Send the quantity below.</b>  
<b>Send /cancel to cancel purchase.</b>
━━━━━━━━━━━━━━━━━━━━━━
"""),
parse_mode = ParseMode.HTML
)
  return CHOOSE_QUANTITY
    
async def handle_quantity(update:Update, context:ContextTypes.DEFAULT_TYPE):
    
    user_id = update.effective_user.id
    user_info = init_user(update, context, user_id)
    user_data = context.user_data
    item = context.user_data['item_to_buy']
    
    if not update.effective_user:
      await update.message.reply_text('not you')
    try:
        amount = int(update.message.text)
        if amount <= 0:
            await update.message.reply_text("❌ Please enter a number greater than 0.")
            return CHOOSE_QUANTITY
    except:
        await update.message.reply_text("❌ Please enter a valid number.")
        return CHOOSE_QUANTITY

    if item == 'essences':
      price = 1000
      if user_info['coins'] >= amount * price:
        result = users.update_one(
            {"user_id": user_id},
            {"$inc": {
              "coins": -(amount * price),"essences": amount }
          }
        )
        if result.modified_count > 0:
            await update.message.reply_text(f"✅ Bought {amount} Essences for {amount * price} coins!")
      else:
        await update.message.reply_text("❌ Not enough coins!\n Type /cancel to cancel purchase")
        return CHOOSE_QUANTITY

    elif item == 'moonshards':
      price = 10000
      if user_info['coins'] >= amount * price:
        result = users.update_one(
    {"user_id": user_id},
    {"$inc": 
      {"coins": -(amount*price), "moonshards": amount}
    }
)
        if result.modified_count > 0:
          await update.message.reply_text(
              f"✅ Bought {amount} Moonshards for {cost} coins!")
      else:
        await update.message.reply_text("❌ Not enough coins!\n Type /cancel to cancel purchase")
        return CHOOSE_QUANTITY

    return ConversationHandler.END
    
    
shop_conv = ConversationHandler(
    entry_points=[CallbackQueryHandler(button7, pattern='^(essences|moonshards)$')],
    states={
        CHOOSE_QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_quantity)],
    },
    fallbacks=[CommandHandler('cancel',cancel)],
    per_message = False
)

# yaha tak ho gaya 

    
async def buy_wp(update:Update, context:ContextTypes.DEFAULT_TYPE):
  user_id = update.effective_user.id
  user_info = init_user(update, context, user_id)
  
  user_wp_name = update.message.text.title()
  
  if user_wp_name not in list(weapon_list.keys()):
    await update.message.reply_text(
    "⚠️ *No such weapon found!*\n"
    "Please double-check the name and try again.",
    parse_mode=ParseMode.MARKDOWN
)
    return BUY_WEAPON
    
  if user_wp_name in weapon_list.keys():
    if user_wp_name not in user_info.get("user_weapons", {}):
      
      weapon_price = weapon_list[user_wp_name]["price"]
      if user_info.get("essences", 0) >= weapon_price:
        new_weapon = copy.deepcopy(weapon_list[user_wp_name])

        users.update_one(
          {"user_id": user_id},
          {
            "$set": {f"user_weapons.{user_wp_name}": new_weapon},
            "$inc": {"essences": -weapon_price}
          }
        )

        await update.message.reply_text(
f"""
━━━━━━━━━━━━━━━━━━━━━━  

<blockquote>
✅ You have successfully purchased <code>{user_wp_name}</code>  
💰 Price: {weapon_price} Essences
</blockquote>
━━━━━━━━━━━━━━━━━━━━━━  
🧰 The weapon has been added to your inventory.  
⚙️ Equip it using /mygear to use it in battle!  
━━━━━━━━━━━━━━━━━━━━━━
""",
                parse_mode=ParseMode.HTML
            )
        return ConversationHandler.END
      
      else:
        await update.message.reply_text(
    """
🚫 Not Enough Essences!
━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
You don’t have enough 💠 <b>Essences</b> to buy that weapon.
Keep exploring and defeating monsters to earn more!
</blockquote>
💡 <b>Tip:</b> Stronger monsters drop more essences.
━━━━━━━━━━━━━━━━━━━━━━
""",
    parse_mode=ParseMode.HTML
)
        return ConversationHandler.END

  
    elif user_wp_name in list(user_info['user_weapons'].keys()):
      await update.message.reply_text(
    """
⚠️ You Already Own This Weapon!
━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
You already have this weapon in your inventory.
Check it out using /mygear!
</blockquote>
💡 <b>Tip:</b> You can only buy each weapon once.
━━━━━━━━━━━━━━━━━━━━━━
""",
    parse_mode=ParseMode.HTML
)
      return ConversationHandler.END
  
weapon_conv_handler = ConversationHandler(
      entry_points=[CallbackQueryHandler(button2, pattern='^(weapon_shop)$')],
      states={
          BUY_WEAPON: [MessageHandler(filters.TEXT & ~filters.COMMAND, buy_wp)],
      },
      fallbacks=[CommandHandler('cancel',cancel)],
      per_message = False# No fallback used in your case
  )
    
    
  
guess_num = range(1)
#guess 
async def guess(update:Update, context:ContextTypes.DEFAULT_TYPE):
    
    user_id = update.message.from_user.id
    user_info = init_user(update, context, user_id)
    user_data = context.user_data
    
    if update.message.chat.type != 'private':
        await update.message.reply_text(
    text="""
🕵️‍♂️ *Guessing Game Notice*  
━━━━━━━━━━━━━━━━━━━━━━  
This game can only be played in *private chat* with me.

👤 Tap my profile and type */guess* to begin your challenge!
━━━━━━━━━━━━━━━━━━━━━━  
""",
    parse_mode=ParseMode.MARKDOWN
)
        return
        
    # Check if user is on cooldown
      
    
    now = asyncio.get_event_loop().time()
    cooldown = context.user_data.get('guess_cooldown', 0)
    
    if now < cooldown:
         wait_time = int(cooldown - now)
         await update.message.reply_text(
    text="⏳ *Please wait!* \n\nYou're on cooldown. Try again in *{} seconds*!".format(wait_time),
    parse_mode=ParseMode.MARKDOWN
)
         return ConversationHandler.END
    
        # Set new cooldown (60 seconds from now)
    context.user_data['guess_cooldown'] = now + 60
    
    
    context.user_data['number']= random.randint(1,100)
    
    keyboard2 = [
    [InlineKeyboardButton("✅ Yes! Let's Play", callback_data='yes')],
    [InlineKeyboardButton("❌ No, Maybe Later", callback_data='no')]
]
    
    reply_markup3 = InlineKeyboardMarkup(keyboard2)
    
    await update.message.reply_text(
    """
🎯 <b>Welcome to the Number Guessing Game!</b>
━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
🔢 A number between <b>1 and 100</b> has been chosen...
❓ Can you guess it right?
</blockquote>
🏆 <b>Reward:</b> +100 Coins
⏱️ <b>Note:</b> Play once every 1 minute.
━━━━━━━━━━━━━━━━━━━━━━
""",
    parse_mode=ParseMode.HTML,
    reply_markup=reply_markup3
)
    
async def button3(update:Update, context:ContextTypes.DEFAULT_TYPE):
    
    
    
    user_id = update.effective_user.id
    user_info = init_user(update, context, user_id)
    user_data = context.user_data
    
    query=update.callback_query
    await query.answer()
    
    user_choice = query.data
    
    
    if user_choice == 'yes':
        context.user_data['guesses'] = 10
        context.user_data['guesses_used'] = 0
        await query.edit_message_text(
    text="""
🎯 <b>Great!</b> Let's begin the challenge!  
━━━━━━━━━━━━━━━━━━━━━━  

<blockquote>
📨 Send me a number between <b>1 and 100</b> to make your guess.  

You have 10 guesses to guess correctly.
</blockquote>
💡 Trust your instincts and take a shot!  
━━━━━━━━━━━━━━━━━━━━━━
""",
    parse_mode=ParseMode.HTML
)
        return guess_num
        
    elif user_choice == 'no':
        await query.edit_message_text(
    text="""
🚪 <b>You chose to walk away...</b>  
━━━━━━━━━━━━━━━━━━━━━━  

<blockquote>
Sometimes, a wise retreat is better than a risky gamble.  
🎲 Come back anytime to test your luck again! 😉
</blockquote>
━━━━━━━━━━━━━━━━━━━━━━
""",
    parse_mode=ParseMode.HTML
)
        return ConversationHandler.END
        
async def guess_numb(update:Update, context:ContextTypes.DEFAULT_TYPE):
     
        user_id = update.message.from_user.id
        user_info = init_user(update, context, user_id)
        user_data = context.user_data
        
        
        user_ans = int(update.message.text)
        correct_ans = int(context.user_data['number'])
            
        context.user_data.get('guesses',0)
        context.user_data.get('guesses_used',0) 
        
        if context.user_data['guesses']<=1:
          coins_lost = 50
          users.update_one(
            {'user_id':user_id},
            {'$inc':{'coins':-coins_lost}
          }
        )
          context.user_data['guesses_used']+=1
          del context.user_data['number']
          del context.user_data['guesses']
          
          await update.message.reply_text(
          f"""
<b>You lost the game!</b> 
━━━━━━━━━━━━━━━━━━━━━━  

<blockquote>
💰 <b>Coins deducted:</b> {coins_lost}
▪︎  <b>Guesses used:</b>{context.user_data['guesses_used']}
</blockquote>
━━━━━━━━━━━━━━━━━━━━━━  
You can do better! 
""",
    parse_mode=ParseMode.HTML
)        
          del context.user_data['guesses_used']  
          return ConversationHandler.END
          
          
        if user_ans == correct_ans:
            coins_gained = 50*user_info['level']
            users.update_one(
              {'user_id':user_id},
              {'$inc':{'coins':coins_gained}}
            )
            context.user_data['guesses_used'] += 1
            del context.user_data['number']
            del context.user_data['guesses']
            xp_gained = 15*user_info['level']
            await xp_system(update,context,user_id,xp_gained)
            await update.message.reply_text(
    f"""
🎉 <b>You guessed it right!</b> 🎯  
━━━━━━━━━━━━━━━━━━━━━━  

<blockquote>
💰 <b>Reward:</b> {coins_gained}
✨ <b>XP Gained:</b> {xp_gained}
▪︎  <b>Guesses used:</b>{context.user_data['guesses_used']}
</blockquote>
━━━━━━━━━━━━━━━━━━━━━━  
Keep it up, champion! 🧠🔥
""",
    parse_mode=ParseMode.HTML
)
            del context.user_data['guesses_used']
            return ConversationHandler.END
            
        elif user_ans >= correct_ans:
            context.user_data['guesses']-=1
            context.user_data['guesses_used']+=1
            await update.message.reply_text(
    f"❌ *Wrong answer!*\nYour guess is *too high* 📈\nYou have *{context.user_data['guesses']}* tries left!\nTry a smaller number!",
    parse_mode=ParseMode.MARKDOWN
)
            return guess_num
            
            
        elif user_ans <= correct_ans:
            context.user_data['guesses']-=1
            context.user_data['guesses_used']+=1
            await update.message.reply_text(
    f"❌ *Wrong answer!*\nYour guess is *too low* 📉\nYou have *{context.user_data['guesses']}* tries left!\nTry a bigger number!",
    parse_mode=ParseMode.MARKDOWN
)
            return guess_num
            
conv_handler = ConversationHandler(
  entry_points =[CallbackQueryHandler(button3,pattern='^yes|no$')],
  states = {
    guess_num: [MessageHandler(filters.TEXT & ~filters.COMMAND , guess_numb )]
    },
  fallbacks = [CommandHandler('cancel',cancel)],
  per_message = False)        
   
   
#toss
async def toss(update:Update, context:ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    user_info = init_user(update, context, user_id)
    
    now = asyncio.get_event_loop().time()
    cooldown = context.user_data.get('toss_cooldown', 0)
    if now < cooldown:
        wait_time = int(cooldown - now)
        await update.message.reply_text(
            text=f"⏳ *Whoa there!* You just tossed the magical coin!\n\n🪙 Please wait *{wait_time} seconds* before trying again!",
            parse_mode=ParseMode.MARKDOWN
        )
        return
    
    context.user_data['toss_cooldown'] = now + 30
    
    two_option = ['🔥 𝕊𝕠𝕝𝕒𝕣𝕒 ☀','❄️ 𝕃𝕦𝕟𝕒𝕣𝕒 🌙']
    bot_option = random.choice(two_option)
    context.user_data['bot_option'] = bot_option
    
    # Add user_id in callback_data so you can check later
    keyboard3 = [
        [
            InlineKeyboardButton("🔥 𝕊𝕠𝕝𝕒𝕣𝕒 ☀", callback_data=f'coin_🔥 𝕊𝕠𝕝𝕒𝕣𝕒 ☀_{user_id}'),
            InlineKeyboardButton("❄️ 𝕃𝕦𝕟𝕒𝕣𝕒 🌙", callback_data=f'coin_❄️ 𝕃𝕦𝕟𝕒𝕣𝕒 🌙_{user_id}')
        ]
    ]
    reply_markup4 = InlineKeyboardMarkup(keyboard3)
    
    await update.message.reply_text(
        """
🪙 <b>Time to Toss the Magical Coin!</b> 🎯  
━━━━━━━━━━━━━━━━━━━━━━  

<blockquote>
Choose your side wisely:  
🔥 𝕊𝕠𝕝𝕒𝕣𝕒 ☀ or ❄️ 𝕃𝕦𝕟𝕒𝕣𝕒 🌙? 🤔
</blockquote>
""",
        reply_markup=reply_markup4,
        parse_mode=ParseMode.HTML
    )


async def button4(update:Update, context:ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data  # like 'coin_heads_123456789'
    parts = data.split('_')
    
    if len(parts) < 3:
        await query.answer("Invalid button!", show_alert=False)
        return
    
    chosen_option = parts[1]  # 'heads' or 'tails'
    allowed_user_id = int(parts[2])
    pressing_user = query.from_user.id
    
    if pressing_user != allowed_user_id:
        await query.answer("Not You!",show_alert=False)
        return
    
    user_info = init_user(update, context, allowed_user_id)
    
    if chosen_option == context.user_data.get('bot_option'):
        await query.edit_message_text(
            text=f"""
🪙 <b>Magical Coin Toss Result!</b> 🎯
━━━━━━━━━━━━━━━━━━━━━━

🎉 The magical coin landed on: <b>{context.user_data['bot_option']}</b>

<blockquote>
✅ <b>You won the toss!</b>
🪙 <b>Reward:</b> +20 Coins
✨ <b>XP Gained:</b> +15
</blockquote>
""",
            parse_mode=ParseMode.HTML
        )
        users.update_one(
          {'user_id':allowed_user_id},
          {'$inc':{'coins':20}}
          )
        await xp_system(update, context, allowed_user_id,15)
    else:
        await query.edit_message_text(
            text=f"""
🪙 <b>Magical Coin Toss Result!</b> 🎯
━━━━━━━━━━━━━━━━━━━━━━

😢 The magical coin landed on: <b>{context.user_data['bot_option']}</b>

<blockquote>
❌ <b>You lost the toss!</b>
💸 <b>Penalty:</b> -10 Coins
</blockquote>
""",
            parse_mode=ParseMode.HTML
        )
        users.update_one(
          {'user_id':allowed_user_id},
          {'$inc':{'coins':-10}}
          )
        
#stats      
async def stats(update:Update, context:ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    user_info = init_user(update, context, user_id)
    
    username = user_info["username"]
    hp = user_info["hp"]
    max_hp = user_info["hp"]
    power = user_info["power"]
    level = user_info["level"]
    agility = user_info["agility"]
    resistance = user_info['resistance']
    xp = user_info["xp"]
    max_xp = user_info["max_xp"]
    coins = user_info["coins"]
    moonshards = user_info["moonshards"]
    essences = user_info["essences"]
    equiped_weapon = user_info['equiped_weapon'] or 'No weapons or not equiped one'

    if not equiped_weapon or equiped_weapon not in user_info['user_weapons']:
        bonus_hp = 0
        bonus_power = 0
        bonus_agility = 0
        bonus_resistance = 0
    else:
        bonus_hp = user_info['user_weapons'][equiped_weapon].get('bonus_hp', 0)
        bonus_power = user_info['user_weapons'][equiped_weapon].get('bonus_power', 0)
        bonus_agility = user_info['user_weapons'][equiped_weapon].get('bonus_agility', 0)
        bonus_resistance = user_info['user_weapons'][equiped_weapon].get('bonus_resistance', 0)

    stats_message = f"""
━━━━━ ✨<u><b>CHARACTER PROFILE</b></u> ✨ ━━━━━ 

<blockquote>
👤 <b>Username:</b> <code>@{username}</code>
</blockquote>

⚔️ <u><b>LEVEL & XP</b></u>  
<blockquote>
🎚️ <b>Level:</b> <b>{level}</b>  
📊 <b>XP:</b> <b>{xp}</b> / <b>{max_xp}</b>
</blockquote>

❤️ <u><b>STATS</b></u>
<blockquote>
💖 <b>HP:</b> <b>{hp}</b> <i>(+{bonus_hp})</i>  
💪 <b>Power:</b> <b>{power}</b> <i>(+{bonus_power})</i>  
⚡ <b>Agility:</b> <b>{agility}</b> <i>(+{bonus_agility})</i> 
🛡️ <b>Resitance:</b> <b>{resistance}</b>  <i>(+{bonus_resistance})</i> 

🗡️ <b>Weapon:</b> <b>{equiped_weapon}</b>
</blockquote>

📝 <i>Play more to grow stronger — the realm remembers those who act.</i>  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    # Add user_id to callback_data!
    keyboard6 = [
        [
            InlineKeyboardButton("⚔️ Battle Stats", callback_data=f"battle_stats_{user_id}"),
            InlineKeyboardButton("🧭 Explore Stats", callback_data=f"stats_explore_{user_id}")
        ]
    ]

    reply_markup6 = InlineKeyboardMarkup(keyboard6)

    await update.message.reply_text(
        stats_message,
        reply_markup=reply_markup6,
        parse_mode=ParseMode.HTML
    )


async def button6(update:Update, context:ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data  # e.g. 'battle_stats_123456789'
    parts = data.split('_')
    
    if len(parts) < 3:
        query.answer("Invalid data!", show_alert=True)
        return

    chosen_stats = parts[0] + '_' + parts[1]
    
    allowed_user_id = int(parts[2])
    pressing_user = query.from_user.id

    if pressing_user != allowed_user_id:
        await query.answer("Not You!", show_alert=False)  
        return

    user_info = init_user(update, context, allowed_user_id)

    if chosen_stats == 'battle_stats':
        battles_played = user_info.get('battles_played', 0)
        battles_won = user_info.get('battles_won', 0)
        battles_lost = user_info.get('battles_lost', 0)

        battle_text = f"""
━━━━━━━━━━━━━━━━━━━━━━  
<u><b>BATTLE STATS</b></u>
━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
Battles Played: <code>{battles_played}</code>  
Battles Won: <code>{battles_won}</code>  
Battles Lost: <code>{battles_lost}</code>
</blockquote>
<i>Keep fighting, warrior!</i>
━━━━━━━━━━━━━━━━━━━━━━
"""
        reply_markup7 = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🎯 My Stats", callback_data=f"my_stats_{allowed_user_id}"),
                InlineKeyboardButton("🧭 Explore Stats", callback_data=f"stats_explore_{allowed_user_id}")
            ]
        ])

        await query.edit_message_text(
            battle_text,
            reply_markup=reply_markup7,
            parse_mode=ParseMode.HTML
        )

    elif chosen_stats == 'stats_explore':
        explores_played = user_info.get('explores_played', 0)
        explores_won = user_info.get('explores_won', 0)
        explores_lost = user_info.get('explores_lost', 0)

        explore_text = f"""
━━━━━━━━━━━━━━━━━━━━━━
<u><b>EXPLORE STATS</b></u>
━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
Explores Done: <code>{explores_played}</code>  
Victories: <code>{explores_won}</code>  
Defeats: <code>{explores_lost}</code>  
</blockquote>
<i>Keep exploring, adventurer!</i>
━━━━━━━━━━━━━━━━━━━━━━
"""
        reply_markup8 = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🎯 My Stats", callback_data=f"my_stats_{allowed_user_id}"),
                InlineKeyboardButton("⚔️ Battle Stats", callback_data=f"battle_stats_{allowed_user_id}")
            ]
        ])

        await query.edit_message_text(
            explore_text,
            reply_markup=reply_markup8,
            parse_mode=ParseMode.HTML
        )

    elif chosen_stats == 'my_stats':
        username = user_info.get("username")
        hp = user_info.get("hp")
        max_hp = user_info.get("hp")
        power = user_info.get("power")
        level = user_info.get("level")
        agility = user_info.get("agility")
        resistance = user_info.get('resistance')
        xp = user_info.get('xp')
        max_xp = user_info.get('max_xp')
        coins = user_info.get("coins")
        moonshards = user_info.get("moonshards")
        essences = user_info.get("essences")
        equiped_weapon = user_info.get('equiped_weapon') or 'No weapons or not equiped one'

        if not equiped_weapon or equiped_weapon not in user_info['user_weapons']:
            bonus_hp = 0
            bonus_power = 0
            bonus_agility = 0
            bonus_resistance = 0
        else:
            bonus_hp = user_info['user_weapons'][equiped_weapon].get('bonus_hp', 0)
            bonus_power = user_info['user_weapons'][equiped_weapon].get('bonus_power', 0)
            bonus_agility = user_info['user_weapons'][equiped_weapon].get('bonus_agility', 0)
            bonus_resistance = user_info['user_weapons'][equiped_weapon].get('bonus_resistance', 0)

        stats_message = f"""
━━━━━ ✨ <u><b>CHARACTER PROFILE</b></u> ✨ ━━━━━ 

<blockquote>
👤 <b>Username:</b> <code>@{username}</code>
</blockquote>

⚔️ <u><b>LEVEL & XP</b></u> 
<blockquote>
🎚️ <b>Level:</b> <b>{level}</b>  
📊 <b>XP:</b> <b>{xp}</b> / <b>{max_xp}</b>
</blockquote>

❤️ <u><b>STATS</b> </u> 
<blockquote>
💖 <b>HP:</b> <b>{hp}</b> <i>(+{bonus_hp})</i>  
💪 <b>Power:</b> <b>{power}</b> <i>(+{bonus_power})</i>  
⚡ <b>Agility:</b> <b>{agility}</b> <i>(+{bonus_agility})</i> 
🛡️ <b>Resitance:</b> <b>{resistance}</b> <i>(+{bonus_resistance})</i> 

🗡️ <b>Weapon:</b> <b>{equiped_weapon}</b>
</blockquote>

📝 <i>Play more to grow stronger — the realm remembers those who act.</i>  
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

        keyboard6 = [
            [
                InlineKeyboardButton("⚔️ Battle Stats", callback_data=f"battle_stats_{allowed_user_id}"),
                InlineKeyboardButton("🧭 Explore Stats", callback_data=f"stats_explore_{allowed_user_id}")
            ]
        ]
        reply_markup6 = InlineKeyboardMarkup(keyboard6)

        await query.edit_message_text(
            text=stats_message,
            reply_markup=reply_markup6,
            parse_mode=ParseMode.HTML
        )
#add 
async def add(update:Update, context:ContextTypes.DEFAULT_TYPE):
  user_id = update.message.from_user.id
  user_info = init_user(update, context, user_id)
  if user_id not in ADMINS:
    await update.message.reply_text('You are not authorized for this cmd ')
    return
  if update.message.reply_to_message:
        # Reply-to-user method: /add <item> <amount>
        target = update.message.reply_to_message.from_user
        target_userid = target.id
        target_name = target.username or target.first_name

        if len(context.args) < 2:
            await update.message.reply_text(
                "Usage (reply): `/add <item> <amount>`",
                parse_mode="Markdown"
            )
            return
        target_user_item = context.args[0]
        try:
            item_amount = int(context.args[1])
        except ValueError:
            await update.message.reply_text("❌ Invalid amount.")
            return
  else:  
    if  len(context.args) < 3:
      await update.message.reply_text(
      """
  <b>Please provide</b>
  
  <blockquote>
  <b>Username</b> :- <i>The user to which you want item to add</i>
  <b>Item</b> :- <i>The item you want to add</i>
  <b>Amount</b> :- <i>How much you want to add</i>
  </blockquote>
  """,
      parse_mode='HTML'
  )
      return
    try: 
      target_userid = int(context.args[0])
      target_user_item = context.args[1]
      item_amount = int(context.args[2])
      target_user_item = target_user_item
    except ValueError:
      await update.message.reply_text("❌ Invalid arguments.")
      return
  
  user_data = users.find_one({"user_id": target_userid})

  if not user_data:
    await update.message.reply_text(f'No user with {target_userid} found. ')
    return 
  
  new_value = user_data.get(target_user_item,0) + item_amount
  users.update_one(
    {"user_id": target_userid}, 
    {"$inc": {target_user_item: item_amount}}, 
    upsert=True 
)
  
  await update.message.reply_text(f"""
🎁 <b>Item Successfully Added!</b>

━━━━━━━━━━━━━━━━━━━━

<blockquote>
👤 <b>User:</b> <code>{target_userid}</code>
📦 <b>Item:</b> <code>{target_user_item}</code>
➕ <b>Amount Added:</b> <code>{item_amount}</code>
📊 <b>New Total:</b> <code>{new_value}</code>
</blockquote>
━━━━━━━━━━━━━━━━━━━━
""", parse_mode="HTML")

  try:
          await context.bot.send_message(
              chat_id=target_userid,
              text=f"""
💰 <b>An admin has added an item to your account!</b>

━━━━━━━━━━━━━━━━━━━━

<blockquote>
📦 <b>Item:</b> <code>{target_user_item}</code>
➕ <b>Amount Added:</b> <code>{item_amount}</code>
📊 <b>Your New Total:</b> <code>{new_value}</code>
</blockquote>
━━━━━━━━━━━━━━━━━━━━
""",
              parse_mode="HTML"
          )
  except:
          pass  # Ignore if recipient can't be messaged
#remove 
async def remove(update:Update, context:ContextTypes.DEFAULT_TYPE):
  user_id = update.message.from_user.id
  user_info = init_user(update, context, user_id)
  if user_id not in ADMINS:
    await update.message.reply_text('You are not authorized for this cmd ')
    return
  if update.message.reply_to_message:
        # Reply-to-user method: /add <item> <amount>
        target = update.message.reply_to_message.from_user
        target_userid = target.id
        target_name = target.username or target.first_name

        if len(context.args) < 2:
            await update.message.reply_text(
                "Usage (reply): `/remove <item> <amount>`",
                parse_mode="Markdown"
            )
            return
        target_user_item = context.args[0]
        try:
            item_amount = int(context.args[1])
        except ValueError:
            await update.message.reply_text("❌ Invalid amount.")
            return
  else:  
    if  len(context.args) < 3:
      await update.message.reply_text(
      """
  <b>Please provide</b>
  
  <blockquote>
  <b>Username</b> :- <i>The user to which you want item to add</i>
  <b>Item</b> :- <i>The item you want to add</i>
  <b>Amount</b> :- <i>How much you want to remove</i>
  </blockquote>
  """,
      parse_mode='HTML'
  )
      return
    try: 
      target_userid = int(context.args[0])
      target_user_item = context.args[1]
      item_amount = int(context.args[2])
      target_user_item = target_user_item
    except ValueError:
      await update.message.reply_text("❌ Invalid arguments.")
      return
  
  user_data = users.find_one({"user_id": target_userid})
  
  
      
  if not user_data:
    await update.message.reply_text(f'No user with {target_userid} found. ')
    return 
  
  
  new_value = user_data.get(target_user_item,0) - item_amount
  users.update_one(
    {"user_id": target_userid}, 
    {"$inc": {target_user_item:-item_amount}}, 
    upsert=True 
)
  
  
  await update.message.reply_text(f"""
🎁 <b>Item Successfully Removed!</b>

━━━━━━━━━━━━━━━━━━━━

<blockquote>
👤 <b>User:</b> <code>{target_userid}</code>
📦 <b>Item:</b> <code>{target_user_item}</code>
➕ <b>Amount  Removed</b> <code>{item_amount}</code>
📊 <b>New Total:</b> <code>{new_value}</code>
</blockquote>
━━━━━━━━━━━━━━━━━━━━
""", parse_mode="HTML")

  try:
          await context.bot.send_message(
              chat_id=target_userid,
              text=f"""
💰 <b>An admin has removed an item to your account!</b>

━━━━━━━━━━━━━━━━━━━━

<blockquote>
📦 <b>Item:</b> <code>{target_user_item}</code>
➕ <b>Amount Removed</b> <code>{item_amount}</code>
📊 <b>Your New Total:</b> <code>{new_value}</code>
</blockquote>
━━━━━━━━━━━━━━━━━━━━
""",
              parse_mode="HTML"
          )
  except:
          pass  # Ignore if recipient can't be messaged


EQUIP_WEAPON = range(0)

async def weapons(update:Update, context:ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_info = init_user(update, context, user_id)
    
    if update.effective_chat.type != 'private':
      await update.message.reply_text('''
      
<blockquote><b>Please view all available weapons list in Private only.</b></blockquote>''',parse_mode='HTML')
      return 
      
    weapons_section = ''
    
    # Loop over weapon_list items (name and info)
    for weapon_name, weapon_info in weapon_list.items():
        if weapon_info and isinstance(weapon_info, dict):
            weapons_section += f'''
<blockquote><b>{weapon_name.title()}</b>
<b>💰 Price:</b> {weapon_info.get('price', 'Unknown')}
<b>🎖️ Rarity:</b> <i>{weapon_info.get('rarity', 'Unknown')}</i></blockquote>
'''
    
    await update.message.reply_text(f'''
━━━━━━━━━━━━━━━━━━━━━━  
🛡️ <b>Available Weapons:</b>
━━━━━━━━━━━━━━━━━━━━━━    
{weapons_section}
━━━━━━━━━━━━━━━━━━━━━━  
<blockquote>🗡️ Check out the legendary weapons waiting for you!

🔥 To get your favorite, just grind hard to be worthy to wield it.

📜 Need to see the full weapon list again? Use the command /weapons anytime!
</blockquote>
''', parse_mode='HTML')


#my_gear
async def my_gear(update:Update, context:ContextTypes.DEFAULT_TYPE):
  user_id = update.effective_user.id
  chat_type = update.effective_chat.type
  user_info = init_user(update, context, user_id)
  user_data = context.user_data
  
  if chat_type in ['group','supergroup']:
    await update.message.reply_text(
f"""
🛡️ <b>Your Battle Gear</b>

━━━━<b> Your equiped weapon </b>━━━━

<blockquote>🔹 <b>Equipped Weapon:</b> {user_info['equiped_weapon']}</blockquote>

━━━━ 🧪 <b>Magical Items </b>🧪 ━━━━

<blockquote><i>Coming Soon...</i></blockquote>

━━━━━━━━━━━━━━━━━━━━
<b> Use /mygear in DM to edit your gear </b>

""",
      parse_mode=ParseMode.HTML
  )
  
  
  else:
    
    my_gear_keyboard = [
      [InlineKeyboardButton("🗡️ Equip Weapon", callback_data='equip_weapon')],
      [InlineKeyboardButton("🧪 Edit Magical Items", callback_data='edit_magic')]
  ]
  
    my_gear_markup = InlineKeyboardMarkup(my_gear_keyboard)
    
    await update.message.reply_text(
f"""
🛡️ <b>Your Battle Gear</b>

━━━━ <b>Your equipped Weapon</b> ━━━━

<blockquote>🔹 <b>Equipped Weapon:</b> {user_info['equiped_weapon']}</blockquote>

━━━━ 🧪 <b>Magical Items</b> 🧪 ━━━━

<blockquote><i>Coming Soon...</i></blockquote>

━━━━━━━━━━━━━━━━━━━━
""",
    parse_mode="HTML",
    reply_markup=my_gear_markup
)
    return ConversationHandler.END

async def my_gear_button(update:Update, context:ContextTypes.DEFAULT_TYPE):
  user_id = update.effective_user.id
  user_info = init_user(update, context, user_id)
  
  query = update.callback_query
  await query.answer()
  
  my_gear_option = query.data
  
  if my_gear_option == 'edit_magic':
    await query.edit_message_text(
    """
🧪 <b>Edit Magical Items</b>

━━━━━━━━━━━━━━━━━━━━
<blockquote>✨ This feature is <i>coming soon</i>...
Get ready to enhance your powers!
</blockquote>
━━━━━━━━━━━━━━━━━━━━
""",
    parse_mode="HTML"
)

  elif my_gear_option == 'equip_weapon':
    user_weapons = user_info['user_weapons']
    weapons_list = '\n'.join([f"🔸 <code>{w}</code>" for w in user_weapons])  # Replace `user_weapons` with your weapon list variable

    await query.edit_message_text(
    f"""
🗡️ <b>Equip Weapon</b>

━━━━━━━━━━━━━━━━━━━━
Here are your available weapons:

<blockquote>{weapons_list if weapons_list else "You have no weapons yet."}
</blockquote>
━━━━━━━━━━━━━━━━━━━━
📤 Send the <b>weapon name</b> to equip it.
━━━━━━━━━━━━━━━━━━━━
""",
    parse_mode="HTML"
)
    return EQUIP_WEAPON
#equip weapon
async def equip_weapon(update:Update, context:ContextTypes.DEFAULT_TYPE):
  user_id = update.effective_message.from_user.id
  sent_weapon_name = update.message.text.title()
  user_info = init_user(update, context, user_id)
  
  if sent_weapon_name in list(all_weapon_list.keys()):
    if sent_weapon_name not in list(user_info['user_weapons'].keys()):
      await update.message.reply_text(
    """
🚫 Oops!

━━━━━━━━━━━━━━━━━━━━
You do not own this weapon.

<blockquote>
Please check your inventory and try again with a valid weapon name.
</blockquote>
━━━━━━━━━━━━━━━━━━━━
""",
    parse_mode="HTML"
)
      return EQUIP_WEAPON
    
    else:
      users.update_one(
        {'user_id':user_id},
        {'$set':{'equiped_weapon':sent_weapon_name}}
        )
      await update.message.reply_text(
    f"""
✅ <b>Weapon Equipped!</b>

━━━━━━━━━━━━━━━━━━━━
<blockquote>
You have successfully equipped the weapon:  
🗡️ <b>{sent_weapon_name.title()}</b>
</blockquote>
Get ready for battle, warrior!

━━━━━━━━━━━━━━━━━━━━
""",
    parse_mode="HTML"
)
      return ConversationHandler.END
      
  else:
    await update.message.reply_text(
    f"""
❌ <b>Invalid Weapon Name!</b>

━━━━━━━━━━━━━━━━━━━━
<blockquote>
There is no such weapon.  
Please double-check and send the correct weapon name.
</blockquote>
━━━━━━━━━━━━━━━━━━━━
""",
    parse_mode="HTML"
)
    return EQUIP_WEAPON
    
    

gear_conv_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(my_gear_button, pattern='^(equip_weapon)$')
    ],
    states={
        EQUIP_WEAPON: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, equip_weapon)
        ],
    },
    fallbacks=[
        CommandHandler('cancel', cancel)
    ],
    per_message = False
)
  


def _format_ability_section(title, emoji, abilities_dict):
    """Return one formatted section or '' if empty."""
    if not abilities_dict:
        return ""
    lines = []
    for key, info in abilities_dict.items():
        # Fallbacks: use key prettified if 'name' missing
        name = escape(info.get('name', key.replace('_', ' ').title()))
        desc = escape(info.get('description', ''))
        lines.append(f">》 <b>{name}</b>: {desc}")
    body = "\n".join(lines)
    return f"""
━━ {emoji} <b>{title}</b> {emoji} ━━

<blockquote>
{body}
</blockquote>
"""

async def show_weapon_abilities(update:Update, context:ContextTypes.DEFAULT_TYPE, user_id, item_to_view, all_weapon_list):
    user_info = init_user(update, context, user_id)

    # Pick the correct source (owned vs global list)
    if item_to_view in user_info.get('user_weapons', {}):
        weapon_data = user_info['user_weapons'][item_to_view]
    else:
        weapon_data = all_weapon_list[item_to_view]

    # Build each section from the new nested dicts
    abilities_section = _format_ability_section("Abilities", "✨", weapon_data.get('abilities', {}))
    passive_abilities_section= _format_ability_section("Passive Abilities","🛡️", weapon_data.get('passiveabilities', {}))
    active_abilities_section = _format_ability_section("Active Abilities","🌟", weapon_data.get('activeabilities', {}))


    full_abilities_info = f"{abilities_section}{passive_abilities_section}{active_abilities_section}".strip()

    if not full_abilities_info:
        full_abilities_info = """
━━ 📜 <b>Abilities</b> ━━

<blockquote>
No abilities available for this weapon yet.
</blockquote>
""".strip()

    item_keyboard_markup = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            'Weapon Stats',
            callback_data=f'weaponstats_{user_id}_{item_to_view.replace(" ", "_")}'
        )
    ]])

    await update.effective_message.edit_caption(
    caption=full_abilities_info,
    parse_mode='HTML',
    reply_markup=item_keyboard_markup
)
  
#view  
async def view(update:Update, context:ContextTypes.DEFAULT_TYPE):
  user_id = update.message.from_user.id
  user_info = init_user(update, context, user_id)
  
  
  
  if len(context.args)<1:
    await update.message.reply_text(
    """
🚫 <b>Oops! You're not using this command correctly.</b>

<blockquote>
📌 Here's how to use it:  
<code>/view &lt;weapon&gt;</code>

🧪 <b>Example:</b>  
<code>/view Bronze Sword</code>
</blockquote>
Try again using the correct format! 😊
""",
    parse_mode="HTML"
)
    return 
  item_to_view = ' '.join(context.args).title()
  context.user_data['item_to_view'] = item_to_view
  
  
  if item_to_view not in list(all_weapon_list.keys()):
    await update.message.reply_text(
    """
❌ <b>Invalid Weapon Name!</b>

━━━━━━━━━━━━━━━━━━━━

<blockquote>
It seems like the item you're trying to view doesn't exist.
</blockquote>
🧠 <b>Tip:</b> Use the command like this:  
<code>/view Bronze Sword</code>
━━━━━━━━━━━━━━━━━━━━
""",
    parse_mode="HTML"
)
  else:
    if item_to_view not in list(user_info['user_weapons'].keys()):
      weapon_hp = all_weapon_list[item_to_view]['bonus_hp']
      weapon_power = all_weapon_list[item_to_view]['bonus_power']
      weapon_resitance = all_weapon_list[item_to_view]['bonus_resistance']
      weapon_agility=all_weapon_list[item_to_view]['bonus_agility']
      weapon_rarity = all_weapon_list[item_to_view]['rarity']
      weapon_photo = all_weapon_list[item_to_view]['photo']
      
      abilities_keyboard_markup = InlineKeyboardMarkup([[
    InlineKeyboardButton(
        "✨ abilities ✨", 
        callback_data=f'abilities_{user_id}_{item_to_view.replace(" ", "_")}'
    )
]])
          
      await update.message.reply_photo(
    photo=weapon_photo,
    caption=f"""
🗡️ <b>Item Info</b>

━━━━━━━━━━━━━━━━━━━━

<blockquote>
🔹 <b>Item:</b> <code>{item_to_view}</code>
🌟 <b>Rarity:</b> <code>{all_weapon_list[item_to_view]["rarity"].title()}</code>
</blockquote>
━━ ⚔️ <b>Weapon Stats</b> ⚔️ ━━

<blockquote>
💥 <b>Power:</b> <code>{all_weapon_list[item_to_view]["bonus_power"]}</code>
❤️ <b>HP:</b> <code>{all_weapon_list[item_to_view]["bonus_hp"]}</code>
🏃 <b>Agility:</b> <code>{all_weapon_list[item_to_view]["bonus_agility"]}</code>
🛡️ <b>Resitance:</b> <code>{all_weapon_list[item_to_view]["bonus_resistance"]}</code>
</blockquote>
━━━━━━━━━━━━━━━━━━━━
""",
    parse_mode="HTML",
    reply_markup = abilities_keyboard_markup
)
    else :
      weapon_photo = all_weapon_list[item_to_view]['photo']
      user_weapon_data = user_info["user_weapons"].get(item_to_view)
  
      abilities_keyboard_markup = InlineKeyboardMarkup([[
    InlineKeyboardButton(
        "✨ abilities ✨", 
        callback_data=f'abilities_{user_id}_{item_to_view.replace(" ", "_")}'
    )
]])
      
      await update.message.reply_photo(
    photo=weapon_photo,
    caption = f"""
🗡️ <b>Item Info</b>

━━━━━━━━━━━━━━━━━━━━

<blockquote>
🔹 <b>Item:</b> {item_to_view}  
🌟 <b>Rarity:</b> {all_weapon_list[item_to_view]["rarity"].title()}
</blockquote>
━━ ⚔️ <b>Weapon Stats</b> ⚔️ ━━

<blockquote>
💥 <b>Power:</b> {user_info['user_weapons'][item_to_view]["bonus_power"]}  
❤️ <b>HP:</b> {user_info['user_weapons'][item_to_view]["bonus_hp"]}  
🏃 <b>Agility:</b> {user_info['user_weapons'][item_to_view]["bonus_agility"]}
🛡️ <b>Resitance:</b> {user_info['user_weapons'][item_to_view]["bonus_resistance"]}
</blockquote>
━━ 🧪 <b>Progress Stats</b> 🧪 ━━

<blockquote>
📈 <b>Level:</b> {user_info['user_weapons'][item_to_view]["weapon_level"]}  
🔸 <b>XP:</b> {user_info['user_weapons'][item_to_view]["weapon_xp"]}/{user_info['user_weapons'][item_to_view]["weapon_max_xp"]}
</blockquote>
━━━━━━━━━━━━━━━━━━━━
""",
    parse_mode="HTML",
    reply_markup = abilities_keyboard_markup
)


async def abilities_button(update:Update, context:ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  data = query.data 
  parts = data.split('_')
  user_data = context.user_data
  
  if len(parts)<2:
    await query.answer('Invalid',show_alert=False)
    
  action = parts[0]
  user_id = int(parts[1])
  presser_id = query.from_user.id 
  user_info = init_user(update,context,user_id)
  item_to_view = "_".join(parts[2:]).replace("_", " ")

  
  if presser_id != user_id:
    await query.answer('Not you!')
    return
    
  if action == 'abilities':
    await show_weapon_abilities(update, context, user_id, item_to_view, all_weapon_list)
        
  elif action == 'weaponstats':
    
    if item_to_view not in list(user_info['user_weapons'].keys()):
      weapon_hp = all_weapon_list[item_to_view]['bonus_hp']
      weapon_power = all_weapon_list[item_to_view]['bonus_power']
      weapon_agility=all_weapon_list[item_to_view]['bonus_agility']
      weapon_resitance=all_weapon_list[item_to_view]['bonus_resistance']
      weapon_rarity = all_weapon_list[item_to_view]['rarity']
      
      abilities_keyboard_markup = InlineKeyboardMarkup([[
    InlineKeyboardButton(
        "✨ abilities ✨", 
        callback_data=f'abilities_{user_id}_{item_to_view.replace(" ", "_")}'
    )
]])
          
      await query.edit_message_caption(
    
    caption=f"""
🗡️ <b>Item Info</b>

━━━━━━━━━━━━━━━━━━━━

<blockquote>
🔹 <b>Item:</b> <code>{item_to_view}</code>
🌟 <b>Rarity:</b> <code>{all_weapon_list[item_to_view]["rarity"].title()}</code>
</blockquote>
━━ ⚔️ <b>Weapon Stats</b> ⚔️ ━━

<blockquote>
💥 <b>Power:</b> <code>{all_weapon_list[item_to_view]["bonus_power"]}</code>
❤️ <b>HP:</b> <code>{all_weapon_list[item_to_view]["bonus_hp"]}</code>
🏃 <b>Agility:</b> <code>{all_weapon_list[item_to_view]["bonus_agility"]}</code>
🛡️ <b>Resitance:</b> <code>{all_weapon_list[item_to_view]["bonus_resistance"]}</code>
</blockquote>
━━━━━━━━━━━━━━━━━━━━
""",
    parse_mode="HTML",
    reply_markup = abilities_keyboard_markup
)
    else :
      
      user_weapon_data = user_info["user_weapons"].get(item_to_view)
  
      abilities_keyboard_markup = InlineKeyboardMarkup([[
    InlineKeyboardButton(
        "✨ abilities ✨", 
        callback_data=f'abilities_{user_id}_{item_to_view.replace(" ", "_")}'
    )
]])
      
      await query.edit_message_caption(
    
    caption = f"""
🗡️ <b>Item Info</b>

━━━━━━━━━━━━━━━━━━━━

<blockquote>
🔹 <b>Item:</b> {item_to_view}  
🌟 <b>Rarity:</b> {all_weapon_list[item_to_view]["rarity"].title()}
</blockquote>
━━ ⚔️ <b>Weapon Stats</b> ⚔️ ━━

<blockquote>
💥 <b>Power:</b> {user_info['user_weapons'][item_to_view]["bonus_power"]}  
❤️ <b>HP:</b> {user_info['user_weapons'][item_to_view]["bonus_hp"]}  
🏃 <b>Agility:</b> {user_info['user_weapons'][item_to_view]["bonus_agility"]}
🛡️ <b>Resitance:</b> {user_info['user_weapons'][item_to_view]["bonus_resistance"]}
</blockquote>
━━ 🧪 <b>Progress Stats</b> 🧪 ━━

<blockquote>
📈 <b>Level:</b> {user_info['user_weapons'][item_to_view]["weapon_level"]}  
🔸 <b>XP:</b> {user_info['user_weapons'][item_to_view]["weapon_xp"]}/{user_info['user_weapons'][item_to_view]["weapon_max_xp"]}
</blockquote>
━━━━━━━━━━━━━━━━━━━━
""",
    parse_mode="HTML",
    reply_markup = abilities_keyboard_markup
)
  
  
  
#give     
async def give(update:Update, context:ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_info = init_user(update, context, user_id)
   
    if len(context.args) < 2:
        await update.message.reply_text(
            '''❌ **Oops! You used the command the wrong way.**  
To give an item, please use this format:  
➡️ /give item amount  

For example: /give essences 3  

Try again! ''')
        return
  
    if not update.message.reply_to_message:
        await update.message.reply_text(
            '''You didn’t reply to anyone’s message.
Please reply to a message to use this command!''')
        return
  
    taker = update.message.reply_to_message.from_user
    giver = update.effective_user
    taker_name = taker.username
    taker_data = users.find_one({'user_id':taker.id})
    if not taker_data:
        await update.message.reply_text(
            '''The user you replied to has not started the bot yet!
Please reply to a person who has started the bot.''')
        return
    
    item_to_give = context.args[0]
    if item_to_give not in ['essences', 'essence', 'moonshard', 'moonshards', 'coins', 'coin']:
      await update.message.reply_text('You cannot give this item!')
      return

    if item_to_give in ['essence', 'moonshard', 'coin']:
      item_to_give += 's'
      pass
    try:
        amount_to_give = int(context.args[1])  
        
    except ValueError:
        await update.message.reply_text("❌ The amount must be a number!")
        return
    if amount_to_give<=0:
      await update.message.reply_text(f'You can not give {amount_to_give} {item_to_give} to @{taker_name}')
      return

    if user_info.get(item_to_give, 0) < amount_to_give:
        await update.message.reply_text(
            f'''You do not have enough {item_to_give}''')
        return
    
    users.update_one(
    {"user_id": user_id},
    {"$inc": {item_to_give: -amount_to_give}}
)
    

    users.update_one(
    {"user_id": taker_id},
    {"$inc": {item_to_give: amount_to_give}},
    upsert=True
)

    await update.message.reply_text(
        f'Sent {amount_to_give} {item_to_give} to {taker.first_name}!')
# photo works
async def get_file_id(update:Update, context:ContextTypes.DEFAULT_TYPE):
  
    photo = update.message.photo[-1]  
    file_id = photo.file_id
    await update.message.reply_text(f"File ID: <code>{file_id}</code>",parse_mode=ParseMode.HTML)
    
#open keyboard
async def open_keyboard(update:Update, context:ContextTypes.DEFAULT_TYPE):
    # One persistent button
    explore_button = [[KeyboardButton("/explore")],[KeyboardButton("/mygear"),KeyboardButton("/close")]]
    
    open_markup = ReplyKeyboardMarkup(
        explore_button, 
        resize_keyboard=True,
        one_time_keyboard=False
    )
    
    await update.message.reply_text(
        "Opened keyboard!",
        reply_markup=open_markup
    )


#remove keyboard
async def remove_keyboard(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Keyboard removed ✅",
        reply_markup=ReplyKeyboardRemove()
    )

def get_agi(user):
  eq = user.get('equiped_weapon')
  bonus = 0
  if eq and eq in user.get('user_weapons', {}):
      bonus = user['user_weapons'][eq].get('bonus_agility', 0)
  return user.get('agility', 200) + bonus

      
#battle
async def battle(update:Update, context:ContextTypes.DEFAULT_TYPE):
  
  user = update.message.from_user
  user_id = update.message.from_user.id
  user_info = users.find_one({'user_id':user_id})
  user_name = user.username or user.first_name
  
  if not user_info:
    await update.message.reply_text('You have not started the bot yet ')
    return
  if not update.message.reply_to_message:
    await update.message.reply_text('Please reply to a user')
    return
  
  target = update.message.reply_to_message.from_user
  target_id = target.id
  target_info = users.find_one({'user_id':target.id})
  target_name = target.username or target.first_name
  
  if not target_info:
    await update.message.reply_text(f'@{target_name} has not started the bot yet ')
    return
  
  if target_id == user_id:
    await update.message.reply_text("❌ You can't challenge yourself!")
    return
  
  battle_accept_keyboard = [[
        InlineKeyboardButton("✅ Accept", callback_data=f"pvp_accept_{user_id}_{target_id}")],[
        InlineKeyboardButton("❌ Reject", callback_data=f"pvp_reject_{user_id}_{target_id}")
    ]]
  battle_accept_markup = InlineKeyboardMarkup(battle_accept_keyboard)
  
  text = f'''
🏟 <b>THE ARENA CALLS!</b>

━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
⚔️ <b>{user.first_name}</b> has challenged <b>{target.first_name}</b> to an epic duel!  
</blockquote>
<i>Only one will emerge victorious...</i>

━━━━━━━━━━━━━━━━━━━━━━

<b>{target.first_name}</b>, will you accept?
'''

  await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=battle_accept_markup,
        parse_mode=ParseMode.HTML
    )  
    
    
async def handle_group_pvp(update, context):
  
  query = update.callback_query
  parts = query.data.split("_")
  
  if len(parts) < 4:
    await query.answer("Invalid PvP command.", show_alert=True)
    return
  
  action = parts[1]
  user_id = int(parts[2])
  target_id = int(parts[3])
  clicker = query.from_user.id
  
  if clicker != target_id:
    await query.answer("❌ You are not the challenged player!", show_alert=True)
    return
  
  if action == "accept":
    
    player1_info = users.find_one({'user_id':user_id})
    player2_info = users.find_one({'user_id':target_id})
    
    player1_stats = get_player_stats(update,context,user_id)
    player2_stats = get_player_stats(update,context,target_id)
    
    hp_player1 = player1_stats['total_hp']
    hp_player2 = player2_stats['total_hp']
    
    power_player1 = player1_stats['user_battle_power']
    power_player2 = player2_stats['user_battle_power']
    
    player1_agility = player1_stats['user_battle_agility']
    player2_agility = player2_stats['user_battle_agility']
    
    resistance_player1 = player1_stats['user_battle_resistance']
    resistance_player2 = player1_stats['user_battle_resistance']
    
    player1_weapon = player1_info['equiped_weapon']
    player2_weapon = player2_info['equiped_weapon']
    
    message_id = update.effective_message.id
    
    context.chat_data[message_id] = {
      'player1': user_id,
      'player2': target_id,
      'player1_name':player1_info['username'],
      'player2_name':player2_info['username'],
      'player1_revived':False,
      'player2_revived':False,
      'battle_log':'',
      'round': 1,
      'hp_player1':hp_player1 ,
      'hp_player2': hp_player2,
      'max_hp_player1':hp_player1,
      'max_hp_player2':hp_player2,
      'power_player1':power_player1,
      'power_player2':power_player2,
      'agility_player1':player1_agility,
      'agility_player2':player2_agility,
      'resistance_player1':resistance_player1,
      'resistance_player2':resistance_player2,
      'passive_activation_player1':False,
      'passive_activation_player2':False,
      'player1_weapon':player1_weapon,
      'player2_weapon':player2_weapon
        }
        
    if player1_agility > player2_agility:
      first_player = user_id
      first_name = player1_info.get('username') 
      first_player_weapon = player1_info.get('equiped_weapon',None)
      
    elif player2_agility > player1_agility:
      first_player = target_id
      first_name = player2_info.get('username')
      first_player_weapon = player2_info.get('equiped_weapon',None)
      
    else:
      first_player = random.choice([user_id, target_id])
      
      if first_player == user_id:
        first_name = player1_info.get('username')
        first_player_weapon = player1_info.get('equiped_weapon',None)
      else:
        first_name = player2_info.get('username')
        first_player_weapon = player2_info.get('equiped_weapon',None)
  
  
  
    context.chat_data[message_id]['turn'] = int(first_player)
      
    player1_name = player1_info.get('username') 
    player2_name = player2_info.get('username') 
    
    await activate_pre_battle_ability(update,context,context.chat_data[message_id]['player1'],'battle')
    await activate_pre_battle_ability(update,context,context.chat_data[message_id]['player2'],'battle')
    
    battle_start_msg = f"""
🔥 <b>CHALLENGE ACCEPTED!</b> 🔥

🏟 <b>The Arena Roars to Life!</b>  
━━━━━━━━━━━━━━━━━━━━━━  
<blockquote>
🥊 <b>Battle:</b> <b>{player1_name}</b> ⚔️ <b>{player2_name}</b> 
</blockquote>
━━━━━━━━━━━━━━━━━━━━━━  

⚡ <b>Agility Showdown:</b>  
<code>{player1_agility}</code> vs <code>{player2_agility}</code>  
━━━━━━━━━━━━━━━━━━━━━━  

🏃‍♂️ <b>First Move:</b> <b>{first_name}</b>  
<i>{'Same agility – fate decides the first strike!' if player1_agility == player2_agility else 'Higher agility seizes the advantage!'}</i>  

━━━━━━━━━━━━━━━━━━━━━━  
<i>Let the clash of steel and willpower begin!</i>
"""

    player_keyboard_markup = get_battle_keyboard(update,context,int(first_player),first_player_weapon)  
    
    await query.edit_message_text(
      battle_start_msg,
      reply_markup=player_keyboard_markup,
      parse_mode="HTML"
        )
  
  elif action == "reject":
    await query.edit_message_text(
        '''❌ <b>Challenge Rejected</b>
    ━━━━━━━━━━━━━━━━━━━━━━
    <blockquote>
    🚪 The duel has been called off.
    <i>Perhaps another time, warrior...</i>
    </blockquote>
    
    ''',
    parse_mode="HTML"
)

def get_battle_keyboard(update:Update, context:ContextTypes.DEFAULT_TYPE,user_id,equiped_weapon):
  
  user_info = users.find_one({'user_id':user_id})
  used_abilities = user_info.get('used_abilities', [])

  active_buttons = []
  for btn_row in active_ability_keyboard(update, context, user_id, equiped_weapon, 'pvp'):
      # Keep only buttons in this row that are NOT used
      filtered_row = [
          btn for btn in btn_row
          if btn.callback_data.split('_', 1)[1] not in used_abilities
      ]
      # Add row only if there's something left
      if filtered_row:
          active_buttons.append(filtered_row)
            
  battle_keyboard = [
    [InlineKeyboardButton('⚔️ Attack',callback_data='pvp_attack'),InlineKeyboardButton('🛡 Focus',callback_data = 'pvp_focus')],
    *active_buttons
    ]
  
  battle_keyboard_markup = InlineKeyboardMarkup(battle_keyboard)
  
  return battle_keyboard_markup
  
async def pvp_attack_button(update:Update, context:ContextTypes.DEFAULT_TYPE):
  
  query = update.callback_query
  await query.answer()
  
  presser_id = query.from_user.id
  message_id = update.effective_message.id
  
  data = query.data
  parts = data.split('_',1)
  answerbattle = parts[1] if len(parts)>1 else ""
  
  if message_id not in context.chat_data:
      await query.answer("No active PvP battle!", show_alert=True)
      return

  battle = context.chat_data[message_id]
  
  if presser_id != battle['turn']:
    await query.answer("Wait for your turn!", show_alert=True)
    return
  
  if presser_id == battle['player1']:
    my_label, enemy_id = 'player1', battle['player2']
    
  elif presser_id == battle['player2']:
    my_label, enemy_id = 'player2', battle['player1']
    
  else:
    await query.answer("You're not in this battle!", show_alert=True)
    return
  
  player1_info = users.find_one({'user_id':battle['player1']})
  player2_info = users.find_one({'user_id':battle['player2']})
  
  presser_info = users.find_one({'user_id':presser_id})
  opponent_info = users.find_one({'user_id':enemy_id})
  
  presser_equiped_weapon = presser_info['equiped_weapon']
  
  presser_name = presser_info.get('username') 
  opponent_name = opponent_info.get('username')
  
  if answerbattle == 'attack':
    
    if my_label == 'player1':
      await attack_enemy(update,context,battle,'player1_name','hp_player2','power_player1','resistance_player2','battle_log')
      
    else:
      await attack_enemy(update,context,battle,'player2_name','hp_player1','power_player2','resistance_player1','battle_log')
      
    
    await activate_passive_ability(update,context,presser_id,'battle')
    
    if battle['hp_player1'] > battle['max_hp_player1']:
      battle['hp_player1'] = battle['max_hp_player1']
      
    if battle['hp_player2'] > battle['max_hp_player2']:
      battle['hp_player2'] = battle['max_hp_player2']
      
      
  elif answerbattle == 'focus':
    
    if my_label == 'player1':
      battle['resistance_player1'] += int(battle['resistance_player1'] * 0.5)
      battle['power_player1'] += int(battle['power_player1'] * 0.1)
      
    else:
      battle['resistance_player2'] += int(battle['resistance_player2'] * 0.5)
      battle['power_player2'] += int(battle['power_player2'] * 0.1)
      
    battle['battle_log'] += f'''{presser_name} uses Focus 🛡️
Resistance increased by 50% ,
Power increased by 10% .'''
      
    if battle['hp_player1'] > battle['max_hp_player1']:
      battle['hp_player1'] = battle['max_hp_player1']
      
    if battle['hp_player2'] > battle['max_hp_player2']:
      battle['hp_player2'] = battle['max_hp_player2']
      
  else:
    
    if 'used_abilities' not in presser_info.keys():
        users.update_one(
          {'user_id':presser_id},
          {'$set':{'used_abilities':[]}})
    
    presser_info = users.find_one({'user_id':presser_id})
    
    if my_label == 'player1':
      await activate_active_ability(update,context,presser_id,answerbattle,'battle',battle)
    else:
      await activate_active_ability(update,contest,presser_id,answerbattle,'battle',battle)
      
      
    await activate_passive_ability(update,context,presser_id,'battle')
    
    if battle['hp_player1'] > battle['max_hp_player1']:
      battle['hp_player1'] = battle['max_hp_player1']
      
    if battle['hp_player2'] > battle['max_hp_player2']:
      battle['hp_player2'] = battle['max_hp_player2']
      
      
  player1_name = player1_info.get('username')
  player2_name = player2_info.get('username')
      
  def create_hp_bar(current_hp, max_hp, length=15):
        import math
        filled = math.ceil((current_hp / max_hp) * length) if max_hp > 0 else 0
        empty = length - filled
        return "█" * filled + "░" * empty
        
  
  hp_bar_player1 = create_hp_bar(battle['hp_player1'], battle['max_hp_player1'], 15)
  hp_bar_player2 = create_hp_bar(battle['hp_player2'], battle['max_hp_player2'], 15)
  
  
  if battle['hp_player1'] <= 0:
    
    if not battle['player1_weapon']:
      winner_id, loser_id = battle['player2'], battle['player1']
      await battle_victory_msg(update,context,winner_id,loser_id)
      return
      
    else:
      if battle['player1_revived'] == True:
        winner_id, loser_id = battle['player2'], battle['player1']
        await battle_victory_msg(update,context,winner_id,loser_id)
        return
        
      elif battle['player1_revived'] == False:
        
        battle['hp_player1'] = player1_info['hp']
        battle['power_player1'] = player1_info['power']
        battle['agility_player2'] = player1_info['agility']
        battle['max_hp_player1'] = player1_info['hp']
        battle['player1_revived'] = True 
        battle['passive_activation_player1'] = True
        
        if 'used_abilities' not in player1_info.keys():
          users.update_one(
          {'user_id':battle['player1']},
          {'$set':{'used_abilities':[]}})
      
        users.update_one(
          {"user_id": battle['player1']},
          {"$push": {"used_abilities": {"$each": list(actives.keys())}}}
        )
        player1_info = users.find_one({'user_id':battle['player1']})
        
        battle['battle_log'] = f"<b>{player1_info['username']}</b> your weapon broke !!! \nYou are down to your last remaining power "
        
  elif battle['hp_player2'] <= 0:
    
    if not battle['player2_weapon']:
      winner_id, loser_id = battle['player1'], battle['player2']
      await battle_victory_msg(update,context,winner_id,loser_id)
      return
      
    else:
      if battle['player2_revived'] == True:
        winner_id, loser_id = battle['player1'], battle['player2']
        await battle_victory_msg(update,context,winner_id,loser_id)
        return
        
      elif battle['player2_revived'] == False:
        battle['hp_player2'] = player2_info['hp']
        battle['power_player2'] = player2_info['power']
        battle['agility_player2'] = player2_info['agility']
        battle['max_hp_player2'] = player2_info['hp']
        battle['player2_revived'] = True 
        battle['passive_activation_player2'] = True
        
        if 'used_abilities' not in player2_info.keys():
          users.update_one(
          {'user_id':battle['player2']},
          {'$set':{'used_abilities':[]}})
      
        users.update_one(
          {"user_id": battle['player2']},
          {"$push": {"used_abilities": {"$each": list(actives.keys())}}}
        )
        player1_info = users.find_one({'user_id':battle['player2']})
        
        battle['battle_log'] = f"<b>{player2_info['username']}</b> your weapon broke !!! \nYou are down to your last remaining power "
  
  
  
  battle_msg = f"""
⚔️ <b>{presser_name}</b> strikes!
━━━━━━━━━━━━━━━━━━━━━━
<blockquote>{battle['battle_log']}</blockquote>

<blockquote>❤️ <b>{player1_name}'s HP:</b> {battle['hp_player1']}/{battle['max_hp_player1']}  
{hp_bar_player1} 
</blockquote>
<blockquote>❤️ <b>{player2_name}'s HP:</b> {battle['hp_player2']}/{battle['max_hp_player2']}  
{hp_bar_player2} 
</blockquote>
━━━━━━━━━━━━━━━━━━━━━━
🔥 <b>Next Turn:</b> {opponent_name} prepares to attack!
"""
  
  battle['turn'] = enemy_id
  battle['battle_log'] = ''
  enemy_info = init_user(update,context,enemy_id)
  enemy_weapon = enemy_info.get('equiped_weapon',None)
  
  reply_markup = get_battle_keyboard(update,context,enemy_id,enemy_weapon)
  
  await query.edit_message_text(battle_msg, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
  


async def battle_victory_msg(update:Update,context:ContextTypes.DEFAULT_TYPE,winner_id,loser_id):
  
  chat_id = update.effective_chat.id
  message_id = update.effective_message.id
  
  winner_info = users.find_one({'user_id':winner_id})
  loser_info = users.find_one({'user_id':loser_id})
  
  winner = winner_info.get('username') 
  loser = loser_info.get('username') 
  
  win_xp =30
  lose_xp = 10
  
  win_coins = 40*winner_info['level']
  lose_coins= 20*loser_info['level']
  
  update_battle_results(winner_id, loser_id,win_coins, lose_coins)
  
  await xp_system(update, context, winner_id,win_xp)
  await xp_system(update, context, loser_id,lose_xp)
  
  if winner_info.get('equiped_weapon'):
    await weapon_xp_system(update,context,winner_id,30)
    winner_weapon_xp_msg = '🪙 Weapon XP: +'
    winner_xp_gained = 30*winner_info['level']
  else:
    winner_weapon_xp_msg = ''
    winner_xp_gained = ''
    
    
  if loser_info.get('equiped_weapon'):
    await weapon_xp_system(update,context,loser_id,5)
    loser_weapon_xp_msg = '🪙 Weapon XP: +'
    loser_xp_gained = 5*loser_info['level']
  else:
    loser_weapon_xp_msg = '' 
    loser_xp_gained = ''
    
    
  
  victory_msg = f"""
🏆 <b>Victory!</b> 🎉
━━━━━━━━━━━━━━━━━━━━━━
<blockquote>
🥇 <b>Winner:</b> {winner}
💰 Coins: +{win_coins}
✨ XP: +{win_xp}
{winner_weapon_xp_msg}{winner_xp_gained}
</blockquote>

<blockquote>
🥈 <b>Loser:</b> {loser}
💰 Coins: +{lose_coins}
✨ XP: +{lose_xp}
{loser_weapon_xp_msg}{loser_xp_gained}
</blockquote>
━━━━━━━━━━━━━━━━━━━━━━
<blockquote>
⚔️ A fierce battle has ended...  
Only one stands victorious this day.
</blockquote>
━━━━━━━━━━━━━━━━━━━━━━
"""
  await context.bot.edit_message_text(
    chat_id = chat_id,
    message_id = message_id,
    text = victory_msg, 
    parse_mode="HTML")
  
  del context.chat_data[message_id]
  return 
  
def update_battle_results(winner_id, loser_id,win_coins, lose_coins):
    # --- Update Winner ---
    # Fetch winner first
  winner_info = users.find_one({"user_id": winner_id})
  if winner_info:
    users.update_one(
      {"user_id": winner_id},
      { "$set": {"used_abilities": []},
        "$inc": {
          "coins": win_coins,
          "battles_won": 1,
          "battles_played": 1
          }
        }
      )

    # --- Update Loser ---
  loser_info = users.find_one({"user_id": loser_id})
  if loser_info:
    users.update_one(
      {"user_id": loser_id},
      { "$set": {"used_abilities": []},
        "$inc": {
          "coins": lose_coins,
          "battles_lost": 1,
          "battles_played": 1
          }
        }
      )
     
  winner_info = users.find_one({"user_id": winner_id})
  loser_info = users.find_one({"user_id": loser_id})

async def battle_leaderboard(update:Update, context:ContextTypes.DEFAULT_TYPE):
    users = list(users.find({}))

    top = sorted(users, key=lambda u: u.get('battles_won', 0), reverse=True)[:10]

    medals = ["🥇", "🥈", "🥉"]  # For top 3 ranks
    msg = "<b>🏆 Battle Leaderboard — Most Wins 🏆</b>\n\n"
    msg += "<blockquote>\n"

    if not top or all(u.get('battles_won', 0) == 0 for u in top):
        msg += "🛡️ <i>No battles fought yet.</i>"
    else:
        for i, u in enumerate(top, 1):
            wins = u.get('battles_won', 0)
            if wins == 0:
                break

            username = u.get('username') or u.get('first_name', 'Unknown')
            medal = medals[i-1] if i <= 3 else "•"  # Medal for top 3, bullet for others
            msg += f"{medal} <b>{username}</b> — <i>{wins} wins</i>\n"

    msg += "</blockquote>"

    await update.message.reply_text(msg, parse_mode="HTML")


def active_ability_keyboard(update, context, user_id, equiped_weapon,types):
    user_info = init_user(update, context, user_id)
    equiped_weapon = user_info['equiped_weapon']
    

    if not equiped_weapon:
        return [] 

    weapon_data = user_info['user_weapons'][equiped_weapon]
    active_ability_data = weapon_data['activeabilities']
    keyboard = []
    row = []

    for active_ability, active_ability_info in active_ability_data.items():
        if active_ability and isinstance(active_ability_info, dict):
            row.append(InlineKeyboardButton(f"{active_ability_info['name']}", callback_data=f'{types}_{active_ability}'))
            
            if len(row) == 2:
                keyboard.append(row)
                row = []
    if row:
        keyboard.append(row)

    return keyboard
  
def rune_orders(update:Update,context:ContextTypes.DEFAULT_TYPE):
  
  
  pass
  
#Handlers
app.add_handler(CommandHandler('reset_user',reset_user))
app.add_handler(CommandHandler('reset_all',reset_all))
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('help', help))
app.add_handler(CommandHandler('explore', explore))
app.add_handler(CommandHandler('shop', shop))
app.add_handler(CommandHandler('guess',guess))
app.add_handler(CommandHandler('toss',toss))
app.add_handler(CommandHandler('mystats',stats))
app.add_handler(CommandHandler('myinventory',inventory))
app.add_handler(CommandHandler('add',add))
app.add_handler(CommandHandler('remove',remove))
app.add_handler(CommandHandler('view',view))
app.add_handler(CommandHandler('weapons',weapons))
app.add_handler(CommandHandler('mygear',my_gear))
app.add_handler(MessageHandler(filters.PHOTO, get_file_id))
app.add_handler(CommandHandler("open", open_keyboard))
app.add_handler(CommandHandler("close",remove_keyboard))
app.add_handler(CommandHandler('battle', battle))
app.add_handler(CommandHandler('give',give))
app.add_handler(CommandHandler('battle_leaderboard',battle_leaderboard))
app.add_handler(conv_handler)
app.add_handler(shop_conv)
app.add_handler(weapon_conv_handler)
app.add_handler(gear_conv_handler)
app.add_handler(CallbackQueryHandler(inv_button, pattern=r'^inv_'))
app.add_handler(CallbackQueryHandler(button2,pattern='^(resource_shop|weapon_shop|magic_shop)$'))  
app.add_handler(CallbackQueryHandler(button,pattern='^explore_'))  
app.add_handler(CallbackQueryHandler(explore_button,pattern='^(hunt)$'))
app.add_handler(CallbackQueryHandler(button4, pattern=r'^coin_'))
app.add_handler(CallbackQueryHandler(button6, pattern=r'^(battle_stats|stats_explore|my_stats)'))
app.add_handler(CallbackQueryHandler(my_gear_button,pattern='^(equip_weapon|edit_magic)$'))
app.add_handler(CallbackQueryHandler(handle_group_pvp, pattern=r'^pvp_(accept|reject)_'))
app.add_handler(CallbackQueryHandler(pvp_attack_button, pattern='^pvp_'))
app.add_handler(CallbackQueryHandler(
    abilities_button,
    pattern=r'^(abilities|weaponstats)_[0-9]+_.+'
))


app.run_polling()
