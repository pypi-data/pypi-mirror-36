"""
Devices.
"""

import attr
from functools import partial

from .event import DeviceLocated, DeviceNotFound
from .error import IsDirError

import logging
logger = logging.getLogger(__name__)

__all__ = ["Device"]


@attr.s
class NoLocationKnown(RuntimeError):
    device = attr.ib()


@attr.s
class NotADevice(RuntimeError):
    id = attr.ib()


dev_classes = dict()


def register(cls):
    dev_classes[cls.family] = cls


def split_id(id):
    try:
        a, b, c = (int(x, 16) for x in id.split('.'))
    except ValueError:
        raise NotADevice(id)
    return a, b, c

@attr.s
class SimpleGetter:
    path = attr.ib()
    typ = attr.ib()

    async def __get__(slf, self, cls):
        res = await self.dev.attr_get(*slf.path)
        if slf.typ in {'f', 'g', 'p', 't'}:
            res = float(res)
        elif slf.typ in {'i', 'u'}:
            res = int(res)
        elif slf.typ == 'y':
            res = bool(int(res))
        elif slf.typ == 'b':
            pass
        else:
            res = res.decode('utf-8')
        return res

@attr.s
class SimpleSetter:
    path = attr.ib()
    typ = attr.ib()

    def __get__(slf, self, cls):
        async def setter(val):
            if slf.typ == 'b':
                pass
            elif slf.typ == 'y':
                val = b'1' if val else b'0'
            else:
                val = str(val).encode("utf-8")
            await self.dev.attr_set(*slf.path, value=val)

        return setter

@attr.s
class ArrayGetter:
    path = attr.ib()
    typ = attr.ib()
    num = attr.ib()

    def __get__(slf, self, cls):
        class IdxObj:
            async def __getitem__(sl, idx):
                if slf.num:
                    idx = str(idx)
                else:
                    idx = chr(ord('A')+idx)
                p = slf.path[:-1] + (slf.path[-1]+'.'+idx,)
                res = await self.dev.attr_get(*p)
                if slf.typ in {'f', 'g', 'p', 't'}:
                    res = float(res)
                elif slf.typ in {'i', 'u'}:
                    res = int(res)
                elif slf.typ == 'y':
                    res = bool(int(res))
                elif slf.typ == 'b':
                    pass
                else:
                    res = res.decode('utf-8')
                return res
        return IdxObj()

@attr.s
class ArraySetter:
    path = attr.ib()
    typ = attr.ib()
    num = attr.ib()

    def __get__(slf, self, cls):
        async def setter(idx, val):
            if slf.num:
                idx = str(idx)
            else:
                idx = chr(ord('A')+idx)
            p = slf.path[:-1] + (slf.path[-1]+'.'+idx,)
            if slf.typ == 'b':
                pass
            elif slf.typ == 'y':
                val = b'1' if val else b'0'
            else:
                val = str(val).encode("utf-8")
            await self.dev.attr_set(*p, value=val)
        return setter

class SubDir:
    _subdirs = set()
    # dev = None  # needs to be filled by subclass
    def __getattr__(self, name):
        if name not in self._subdirs:
            return super().__getattribute__(name)
        c = getattr(self,'_cls_'+name)(self)
        c.dev = self.dev
        return c

async def setup_accessors(server, cls, typ, *subdir):
    for d in await server.dir("structure", typ, *subdir):
        dd = subdir + (d,)
        try:
            v = await server.attr_get("structure", typ, *dd)
        except IsDirError:

            t = typ
            class SubPath(SubDir):
                typ = t
                subdir = dd
                def __init__(self, base):
                    self.base = base
                def __repr__(self):
                    return "<%s %s %s>" % (self.__class__.__name, self.base, self.subdir)
                def __get__(self, obj, cls):
                    if obj is None:
                        return cls
                    try:
                        return getattr(obj,"_"+self.dd[-1])
                    except AttributeError:
                        c = getattr(cls, '_cls_'+d)()
                        setattr(obj,"_"+self.dd[-1], c)
                        import pdb;pdb.set_trace()
                        c.dev = obj.dev
                        return c

            SubPath.__name__ = '_cls_'+d
            setattr(cls, '_cls_'+d, SubPath)
            cls._subdirs.add(d)
            await setup_accessors(server, SubPath, typ, *dd)
            
        else:
            v = v.decode("utf-8").split(",")
            v[1] = int(v[1])
            v[2] = int(v[2])
            v[4] = int(v[4])
            if v[1] == 0:
                if d.endswith('.0'):
                    num = True
                elif d.endswith('.A'):
                    num = False
                else:
                    num = None

                if num is None:
                    if v[3] in {'ro', 'rw'}:
                        setattr(cls, d, SimpleGetter(dd, v[0]))
                    if v[3] in {'wo', 'rw'}:
                        setattr(cls, 'set_' + d, SimpleSetter(dd, v[0]))
                else:
                    d = d[:-2]
                    dd = subdir + (d,)
                    if v[3] in {'ro', 'rw'}:
                        setattr(cls, d, ArrayGetter(dd, v[0], num))
                    if v[3] in {'wo', 'rw'}:
                        setattr(cls, 'set_' + d, ArraySetter(dd, v[0], num))



class Device(SubDir):
    """Base class for devices.

    A device may or may not have a known location.
    """
    _did_setup = False

    def __init__(self, service, id):
        logger.debug("NewDev %s", id)

    @property
    def dev(self):
        return self

    def __new__(cls, service, id):
        family_id, code, chksum = split_id(id)

        cls = dev_classes.get(family_id)
        if cls is None:

            class cls(Device):
                family = family_id

            cls.__name__ = "Device_%02x" % (family_id,)
            dev_classes[family_id] = cls

        self = object.__new__(cls)

        self.id = id.upper()
        self.family = family_id
        self.code = code
        self.chksum = chksum

        self.service = service
        self.bus = None

        self._unseen = 0

        return self

    @classmethod
    async def setup_struct(cls, server):
        """Read the device's structural data from OWFS
        and add methods to access the fields"""

        if cls._did_setup is not False:
            return
        cls._did_setup = None

        try:
            fc = "%02X" % (cls.family)
            await setup_accessors(server, cls, fc)

        except BaseException:
            cls._did_setup = False
            raise
        else:
            cls._did_setup = True

    def __eq__(self, x):
        x = getattr(x, 'id', x)
        return self.id == x

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return "<%s:%s @ %s>" % (self.__class__.__name__, self.id, self.bus)

    def buses(self):
        return set()

    def locate(self, bus):
        """The device has been seen here."""
        if self.bus is bus:
            return
        self.bus = bus
        self.service.push_event(DeviceLocated(self))

    def delocate(self, bus):
        """The device is no longer located here."""
        if self.bus is bus:
            self._delocate()

    def _delocate(self):
        self.bus._del_device(self)
        self.bus = None
        self.service.push_event(DeviceNotFound(self))

    async def attr_get(self, *attr):
        """Read this attribute"""
        if self.bus is None:
            raise NoLocationKnown(self)
        return await self.bus.attr_get(*((self.id,) + attr))

    async def attr_set(self, *attr, value):
        """Write this attribute"""
        if self.bus is None:
            raise NoLocationKnown(self)
        return await self.bus.attr_set(*((self.id,) + attr), value=value)


@register
class SwitchDevice(Device):
    family = 0x1F

    def buses(self):
        b = []
        b.append((self.id, "main"))
        b.append((self.id, "aux"))
        return b


@register
class TemperatureDevice(Device):
    family = 0x10

    async def stop_alarm(self):
        t = await self.latesttemp
        if t > (await self.temphigh):
            await self.set_temphigh(int(t + 2))
        if t < (await self.templow):
            await self.set_templow(int(t - 1))
