import aiohttp
import json
from datetime import datetime
from enum import Enum

from src.core import settings
from src.shared import get_unique_id


class RemarkEnum(Enum):
    OWNERS = 'OWNERS'
    SUBSCRIPTIONS = 'SUBSCRIPTIONS'
    TEMPORARY = 'TEMPORARY'


class XUIApi:
    def __init__(self):
        self.panel_ip = settings.panel_ip
        self.panel_port = settings.panel_port
        self.panel_username = settings.panel_username
        self.panel_password = settings.panel_password
        self.panel_path = settings.panel_path
        self.panel_session_id = settings.panel_session_id
        
        self.base_url = f'http://{self.panel_ip}:{self.panel_port}/{self.panel_path}'
        
        self.cookies = {'3x-ui': self.panel_session_id}

    async def _make_request(self, method: str, endpoint: str, data: dict = None, json: dict = None, auth: bool = False):
        async with aiohttp.ClientSession() as session:
            url = f'{self.base_url}/{endpoint}'
            async with session.request(
                method=method,
                url=url,
                data=data,
                json=json,
                cookies=self.cookies if auth else None
            ) as response:
                if response.status == 404:
                    raise ValueError(f"Error 404: {url} not found")
                try:
                    response_json = await response.json()
                except aiohttp.ContentTypeError:
                    response_text = await response.text()
                    raise ValueError(f"Expected JSON, got: {response_text[:200]}")
                return response_json, response.cookies

    async def get_session_id(self) -> str:
        method = 'POST'
        endpoint = 'login'
        payload = {
            'username': self.panel_username,
            'password': self.panel_password
        }
        
        _, cookies = await self._make_request(method=method, endpoint=endpoint, json=payload)
        session_id = cookies.get('3x-ui')
        if session_id:
            self.cookies['3x-ui'] = session_id.value
            return session_id.value
        raise ValueError("Failed to retrieve session ID")

    async def _get_inbounds(self) -> list:
        method = 'GET'
        endpoint = 'panel/api/inbounds/list'
        
        response_json, _ = await self._make_request(method=method, endpoint=endpoint, auth=True)
        return response_json.get('obj', [])
    
    async def _get_inbound_by_id(self, inbound_id: int) -> dict: 
        for inbound in await self._get_inbounds():
            if inbound['id'] == inbound_id:
                return inbound

    async def _get_inbound_id_by_remark(self, remark: str) -> int:
        inbounds = await self._get_inbounds()
        for inbound in inbounds:
            if inbound.get('remark') == remark:
                return inbound['id']
        raise ValueError(f"No inbound found with remark: {remark}")

    async def _form_client_information(self, remark: RemarkEnum, expire_time: int) -> tuple:
        inbound_id = await self._get_inbound_id_by_remark(remark=remark.value)
        
        total_gb = 32212254720 if remark == RemarkEnum.TEMPORARY else 0
        
        client_id = get_unique_id()
        email = get_unique_id()
        subscribe_id = get_unique_id()
        expire_time_ms = int(datetime.now().timestamp() * 1000 + expire_time * 1000)
        
        return inbound_id, client_id, email, subscribe_id, total_gb, expire_time_ms

    async def _form_client_data(self, remark: RemarkEnum, expire_time: int, chat_id: int) -> dict:
        inbound_id, client_id, email, subscribe_id, total_gb, expire_time_ms = await self._form_client_information(
            remark=remark, expire_time=expire_time
        )
        
        data = {
            'id': inbound_id,
            'settings': json.dumps({
                'clients': [{
                    'id': client_id,
                    'flow': '',
                    'email': email,
                    'limitIp': 0,
                    'totalGB': total_gb,
                    'expiryTime': expire_time_ms,
                    'enable': True,
                    'tgId': chat_id,
                    'subId': subscribe_id,
                    'reset': 0
                }]
            })
        }

        return data, inbound_id, client_id, email
    
    def _form_config_key(self, inbound: dict, client_id: str) -> str:
        port = inbound['port']
        
        spx = f'%2F#✨RADJAVPN-{client_id[:8]}'
        
        stream_settings = inbound['streamSettings']
        
        stream_settings = json.loads(stream_settings)
        
        transmission_protocol = stream_settings['network']
        security = stream_settings['security']
        
        reality_settings = stream_settings['realitySettings']
        general_reality_settings = reality_settings['settings']
        
        server_name = reality_settings['serverNames'][0]
        sid = reality_settings['shortIds'][0]
        public_key = general_reality_settings['publicKey']
        fingerprint = general_reality_settings['fingerprint']
        
        config_key = (f'vless://{client_id}@{self.panel_ip}:{port}?type={transmission_protocol}&security={security}'
                      f'&pbk={public_key}&fp={fingerprint}&sni={server_name}&sid={sid}&spx={spx}')
                      
        return config_key

    async def add_client(self, remark: RemarkEnum, expire_time: int, chat_id: int) -> dict:
        if not isinstance(remark, RemarkEnum):
            raise ValueError(f'Invalid remark: {remark}. Expected an instance of RemarkEnum.')

        method = 'POST'
        endpoint = 'panel/api/inbounds/addClient'
        data, inbound_id, client_id, email= await self._form_client_data(remark=remark, expire_time=expire_time, chat_id=chat_id)
        
        inbound = await self._get_inbound_by_id(inbound_id=inbound_id)
        
        config_key = self._form_config_key(inbound=inbound, client_id=client_id)
        
        _, _ = await self._make_request(method=method, endpoint=endpoint, data=data, auth=True)
        
        return config_key, client_id, email
        