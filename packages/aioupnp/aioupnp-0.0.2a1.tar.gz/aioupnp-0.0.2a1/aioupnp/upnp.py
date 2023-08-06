import os
import logging
import json
import asyncio
import functools
from aioupnp.fault import UPnPError
from aioupnp.gateway import Gateway
from aioupnp.constants import UPNP_ORG_IGD
from aioupnp.util import get_gateway_and_lan_addresses
from aioupnp.protocols.ssdp import m_search

log = logging.getLogger(__name__)


def cli(format_result=None):
    def _cli(fn):
        @functools.wraps(fn)
        async def _inner(*args, **kwargs):
            result = await fn(*args, **kwargs)
            if not format_result or not result or not isinstance(result, (list, dict, tuple)):
                return result
            self = args[0]
            return {k: v for k, v in zip(getattr(self.gateway.commands, format_result).return_order, result)}
        f = _inner
        f._cli = True
        return f
    return _cli


def _encode(x):
    if isinstance(x, bytes):
        return x.decode()
    elif isinstance(x, Exception):
        return str(x)
    return x


class UPnP:
    def __init__(self, lan_address: str, gateway_address: str, gateway: Gateway):
        self.lan_address = lan_address
        self.gateway_address = gateway_address
        self.gateway = gateway

    @classmethod
    def get_lan_and_gateway(cls, lan_address: str = '', gateway_address: str = '',
                            interface_name: str = 'default') -> (str, str):
        if not lan_address or not gateway_address:
            gateway_addr, lan_addr = get_gateway_and_lan_addresses(interface_name)
            lan_address = lan_address or lan_addr
            gateway_address = gateway_address or gateway_addr
        return lan_address, gateway_address

    @classmethod
    async def discover(cls, lan_address: str = '', gateway_address: str = '', timeout: int = 1,
                       service: str = UPNP_ORG_IGD, interface_name: str = 'default'):
        try:
            lan_address, gateway_address = cls.get_lan_and_gateway(lan_address, gateway_address, interface_name)
        except Exception as err:
            raise UPnPError("failed to get lan and gateway addresses: %s" % str(err))
        gateway = await Gateway.discover_gateway(lan_address, gateway_address, timeout, service)
        return cls(lan_address, gateway_address, gateway)

    @classmethod
    @cli()
    async def m_search(cls, lan_address: str = '', gateway_address: str = '', timeout: int = 1,
                       service: str = UPNP_ORG_IGD, interface_name: str = 'default') -> dict:
        lan_address, gateway_address = cls.get_lan_and_gateway(lan_address, gateway_address, interface_name)
        datagram = await m_search(lan_address, gateway_address, timeout, service)
        return {
            'lan_address': lan_address,
            'gateway_address': gateway_address,
            'discover_reply': datagram.as_dict()
        }

    @cli()
    async def get_external_ip(self) -> str:
        return await self.gateway.commands.GetExternalIPAddress()

    @cli("AddPortMapping")
    async def add_port_mapping(self, external_port: int, protocol: str, internal_port, lan_address: str,
                         description: str) -> None:
        return await self.gateway.commands.AddPortMapping(
            NewRemoteHost="", NewExternalPort=external_port, NewProtocol=protocol,
            NewInternalPort=internal_port, NewInternalClient=lan_address,
            NewEnabled=1, NewPortMappingDescription=description, NewLeaseDuration=""
        )

    @cli("GetGenericPortMappingEntry")
    async def get_port_mapping_by_index(self, index: int) -> dict:
        return await self._get_port_mapping_by_index(index)

    async def _get_port_mapping_by_index(self, index: int) -> (str, int, str, int, str, bool, str, int):
        try:
            redirect = await self.gateway.commands.GetGenericPortMappingEntry(NewPortMappingIndex=index)
            return redirect
        except UPnPError:
            return

    @cli()
    async def get_redirects(self) -> list:
        redirects = []
        cnt = 0
        redirect = await self.get_port_mapping_by_index(cnt)
        while redirect:
            redirects.append(redirect)
            cnt += 1
            redirect = await self.get_port_mapping_by_index(cnt)
        return redirects

    @cli("GetSpecificPortMappingEntry")
    async def get_specific_port_mapping(self, external_port: int, protocol: str):
        """
        :param external_port: (int) external port to listen on
        :param protocol:      (str) 'UDP' | 'TCP'
        :return: (int) <internal port>, (str) <lan ip>, (bool) <enabled>, (str) <description>, (int) <lease time>
        """

        try:
            return await self.gateway.commands.GetSpecificPortMappingEntry(
                NewRemoteHost=None, NewExternalPort=external_port, NewProtocol=protocol
            )
        except UPnPError:
            return

    @cli()
    async def delete_port_mapping(self, external_port: int, protocol: str) -> None:
        """
        :param external_port: (int) external port to listen on
        :param protocol:      (str) 'UDP' | 'TCP'
        :return: None
        """
        return await self.gateway.commands.DeletePortMapping(
            NewRemoteHost="", NewExternalPort=external_port, NewProtocol=protocol
        )

    @cli("AddPortMapping")
    async def get_next_mapping(self, port: int, protocol: str, description: str, internal_port: int=None) -> int:
        if protocol not in ["UDP", "TCP"]:
            raise UPnPError("unsupported protocol: {}".format(protocol))
        internal_port = internal_port or port
        redirect_tups = []
        cnt = 0
        port = int(port)
        internal_port = int(internal_port)
        redirect = await self._get_port_mapping_by_index(cnt)
        while redirect:
            redirect_tups.append(redirect)
            cnt += 1
            redirect = await self._get_port_mapping_by_index(cnt)

        redirects = {
            "%i:%s" % (ext_port, proto): (int_host, int_port, desc)
            for (ext_host, ext_port, proto, int_port, int_host, enabled, desc, lease) in redirect_tups
        }
        while ("%i:%s" % (port, protocol)) in redirects:
            int_host, int_port, _ = redirects["%i:%s" % (port, protocol)]
            if int_host == self.lan_address and int_port == internal_port:
                break
            port += 1

        await self.add_port_mapping(  # set one up
                port, protocol, internal_port, self.lan_address, description
        )
        return port

    @cli()
    async def get_soap_commands(self) -> dict:
        return {
            'supported': list(self.gateway._registered_commands.keys()),
            'unsupported': self.gateway._unsupported_actions
        }

    @cli()
    async def generate_test_data(self):
        external_ip = await self.get_external_ip()
        redirects = await self.get_redirects()
        ext_port = await self.get_next_mapping(4567, "UDP", "aioupnp test mapping")
        delete = await self.delete_port_mapping(ext_port, "UDP")
        after_delete = await self.get_specific_port_mapping(ext_port, "UDP")

        commands_test_case = (
            ("get_external_ip", (), "1.2.3.4"),
            ("get_redirects", (), redirects),
            ("get_next_mapping", (4567, "UDP", "aioupnp test mapping"), ext_port),
            ("delete_port_mapping", (ext_port, "UDP"), delete),
            ("get_specific_port_mapping", (ext_port, "UDP"), after_delete),
        )

        gateway = self.gateway
        device = list(gateway.devices.values())[0]
        assert device.manufacturer and device.modelName
        device_path = os.path.join(os.getcwd(), "%s %s" % (device.manufacturer, device.modelName))
        commands = gateway.debug_commands()
        with open(device_path, "w") as f:
            f.write(json.dumps({
                "router_address": self.gateway_address,
                "client_address": self.lan_address,
                "port": gateway.port,
                "gateway_dict": gateway.gateway_descriptor(),
                'expected_devices': [
                    {
                        'cache_control': 'max-age=1800',
                        'location': gateway.location,
                        'server': gateway.server,
                        'st': gateway.urn,
                        'usn': gateway.usn
                    }
                ],
                'commands': commands,
                # 'ssdp': u.sspd_factory.get_ssdp_packet_replay(),
                # 'scpd': gateway.requester.dump_packets(),
                'soap': commands_test_case
            }, default=_encode, indent=2).replace(external_ip, "1.2.3.4"))
        return "Generated test data! -> %s" % device_path

    @classmethod
    def run_cli(cls, method, lan_address: str = '', gateway_address: str = '', timeout: int = 60,
                          service: str = UPNP_ORG_IGD, interface_name: str = 'default',
                kwargs: dict = None):
        kwargs = kwargs or {}

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        fut = asyncio.Future()

        async def wrapper():
            if method == 'm_search':
                fn = lambda *_a, **_kw: cls.m_search(lan_address, gateway_address, timeout, service, interface_name)
            else:
                u = await cls.discover(
                    lan_address, gateway_address, timeout, service, interface_name
                )
                if hasattr(u, method) and hasattr(getattr(u, method), "_cli"):
                    fn = getattr(u, method)
                else:
                    fut.set_exception(UPnPError("\"%s\" is not a recognized command" % method))
                    return
            try:
                result = await fn(**kwargs)
                fut.set_result(result)
            except UPnPError as err:
                fut.set_exception(err)
            except Exception as err:
                log.exception("uncaught error")
                fut.set_exception(UPnPError("uncaught error: %s" % str(err)))

        asyncio.run(wrapper())
        try:
            result = fut.result()
        except UPnPError as err:
            print("error: %s" % str(err))
            return

        if isinstance(result, (list, tuple, dict)):
            print(json.dumps(result, indent=2, default=_encode))
        else:
            print(result)
