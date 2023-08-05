from hwt.hdl.typeShortcuts import hInt
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import BIT
from hwt.serializer.ip_packager.exprSerializer import \
    VivadoTclExpressionSerializer
from hwt.serializer.ip_packager.helpers import appendSpiElem, \
    mkSpiElm
from hwt.serializer.vhdl.serializer import VhdlSerializer
from hwt.synthesizer.param import evalParam
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class WireTypeDef():
    _requiredVal = ["typeName"]

    # @classmethod
    # def fromElem(cls, elm):
    #     self = cls()
    #     for s in cls._requiredVal:
    #         setattr(self, s, findS(elm, s).text)
    #     self.viewNameRefs = []
    #     for r in elm.findall("spirit:viewNameRef", ns):
    #         self.viewNameRefs.append(r.text)
    #     return self

    def asElem(self):
        e = mkSpiElm("wireTypeDef")
        for s in self._requiredVal:
            appendSpiElem(e, s).text = getattr(self, s)
        for r in self.viewNameRefs:
            appendSpiElem(e, "viewNameRef").text = r
        return e


class Port():

    # @classmethod
    # def fromElem(cls, elm):
    #     self = cls()
    #     self.name = findS(elm, "name").text
    #     vec = findS(elm, "vector")
    #     if vec is not None:
    #         self.vector = [findS(vec, "left").text, findS(vec, "right").text]
    #     else:
    #         self.vector = None
    #
    #     wire = findS(elm, "wire")
    #     self.direction = findS(wire, "direction").text
    #     self.type = WireTypeDef.fromElem(findS(findS(wire, "wireTypeDefs"),
    #                                            "wiretypedef"))
    #     return self

    @staticmethod
    def _entPort2CompPort(e, p):
        port = Port()
        port.name = p.name
        port.direction = p.direction.name.lower()
        port.type = WireTypeDef()
        t = port.type
        dt = p._dtype

        t.typeName = VhdlSerializer.HdlType(
            dt, VhdlSerializer.getBaseContext())
        try:
            t.typeName = t.typeName[:t.typeName.index('(')]
        except ValueError:
            pass

        if dt == BIT:
            port.vector = False
        elif isinstance(dt, Bits):
            port.vector = [evalParam(dt.width) - 1, hInt(0)]
        t.viewNameRefs = ["xilinx_vhdlsynthesis",
                          "xilinx_vhdlbehavioralsimulation"]
        return port

    def asElem(self):
        e = mkSpiElm("port")
        appendSpiElem(e, "name").text = self.name
        w = appendSpiElem(e, "wire")
        appendSpiElem(w, "direction").text = self.direction
        if self.vector:
            v = appendSpiElem(w, "vector")

            def mkBoundry(name, val):
                if isinstance(val, int):
                    val = hInt(val)
                d = appendSpiElem(v, name)

                d.attrib["spirit:format"] = "long"
                if isinstance(val, RtlSignalBase):
                    # value is simple type and does not contains generic etc...
                    resolve = 'dependent'
                    d.attrib["spirit:dependency"] = "(%s)" %\
                        VivadoTclExpressionSerializer.asHdl(val)
                    d.text = VivadoTclExpressionSerializer.asHdl(
                        val.staticEval())
                else:
                    resolve = "immediate"
                    d.text = VivadoTclExpressionSerializer.asHdl(val, None)
                d.attrib["spirit:resolve"] = resolve
            mkBoundry("left", self.vector[0])
            mkBoundry("right", self.vector[1])
        td = appendSpiElem(w, "wireTypeDefs")
        td.append(self.type.asElem())
        return e
