﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
from pullenti.unisharp.Utils import Utils
from pullenti.ner.Referent import Referent
from pullenti.ner.transport.TransportKind import TransportKind
from pullenti.morph.LanguageHelper import LanguageHelper


class TransportReferent(Referent):
    
    def __init__(self) -> None:
        from pullenti.ner.transport.internal.MetaTransport import MetaTransport
        super().__init__(TransportReferent.OBJ_TYPENAME)
        self.instance_of = MetaTransport._global_meta
    
    OBJ_TYPENAME = "TRANSPORT"
    
    ATTR_TYPE = "TYPE"
    
    ATTR_BRAND = "BRAND"
    
    ATTR_MODEL = "MODEL"
    
    ATTR_CLASS = "CLASS"
    
    ATTR_NAME = "NAME"
    
    ATTR_NUMBER = "NUMBER"
    
    ATTR_NUMBER_REGION = "NUMBER_REG"
    
    ATTR_KIND = "KIND"
    
    ATTR_STATE = "STATE"
    
    ATTR_ORG = "ORG"
    
    ATTR_DATE = "DATE"
    
    ATTR_ROUTEPOINT = "ROUTEPOINT"
    
    def to_string(self, short_variant : bool, lang : 'MorphLang', lev : int=0) -> str:
        from pullenti.ner.core.MiscHelper import MiscHelper
        res = io.StringIO()
        str0_ = None
        for s in self.slots: 
            if (s.type_name == TransportReferent.ATTR_TYPE): 
                n = s.value
                if (str0_ is None or (len(n) < len(str0_))): 
                    str0_ = n
        if (str0_ is not None): 
            print(str0_, end="", file=res)
        elif (self.kind == TransportKind.AUTO): 
            print("автомобиль", end="", file=res)
        elif (self.kind == TransportKind.FLY): 
            print("самолет", end="", file=res)
        elif (self.kind == TransportKind.SHIP): 
            print("судно", end="", file=res)
        elif (self.kind == TransportKind.SPACE): 
            print("космический корабль", end="", file=res)
        else: 
            print(Utils.enumToString(self.kind), end="", file=res)
        str0_ = self.get_string_value(TransportReferent.ATTR_BRAND)
        if ((str0_) is not None): 
            print(" {0}".format(MiscHelper.convert_first_char_upper_and_other_lower(str0_)), end="", file=res, flush=True)
        str0_ = self.get_string_value(TransportReferent.ATTR_MODEL)
        if ((str0_) is not None): 
            print(" {0}".format(MiscHelper.convert_first_char_upper_and_other_lower(str0_)), end="", file=res, flush=True)
        str0_ = self.get_string_value(TransportReferent.ATTR_NAME)
        if ((str0_) is not None): 
            print(" \"{0}\"".format(MiscHelper.convert_first_char_upper_and_other_lower(str0_)), end="", file=res, flush=True)
            for s in self.slots: 
                if (s.type_name == TransportReferent.ATTR_NAME and str0_ != (s.value)): 
                    if (LanguageHelper.is_cyrillic_char(str0_[0]) != LanguageHelper.is_cyrillic_char((s.value)[0])): 
                        print(" ({0})".format(MiscHelper.convert_first_char_upper_and_other_lower(s.value)), end="", file=res, flush=True)
                        break
        str0_ = self.get_string_value(TransportReferent.ATTR_CLASS)
        if ((str0_) is not None): 
            print(" класса \"{0}\"".format(MiscHelper.convert_first_char_upper_and_other_lower(str0_)), end="", file=res, flush=True)
        str0_ = self.get_string_value(TransportReferent.ATTR_NUMBER)
        if ((str0_) is not None): 
            print(", номер {0}".format(str0_), end="", file=res, flush=True)
            str0_ = self.get_string_value(TransportReferent.ATTR_NUMBER_REGION)
            if ((str0_) is not None): 
                print(str0_, end="", file=res)
        if (self.find_slot(TransportReferent.ATTR_ROUTEPOINT, None, True) is not None): 
            print(" (".format(), end="", file=res, flush=True)
            fi = True
            for s in self.slots: 
                if (s.type_name == TransportReferent.ATTR_ROUTEPOINT): 
                    if (fi): 
                        fi = False
                    else: 
                        print(" - ", end="", file=res)
                    if (isinstance(s.value, Referent)): 
                        print((s.value if isinstance(s.value, Referent) else None).to_string(True, lang, 0), end="", file=res)
                    else: 
                        print(s.value, end="", file=res)
            print(")", end="", file=res)
        if (not short_variant): 
            str0_ = self.get_string_value(TransportReferent.ATTR_STATE)
            if ((str0_) is not None): 
                print("; {0}".format(str0_), end="", file=res, flush=True)
            str0_ = self.get_string_value(TransportReferent.ATTR_ORG)
            if ((str0_) is not None): 
                print("; {0}".format(str0_), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @property
    def kind(self) -> 'TransportKind':
        """ Класс сущности (авто, авиа, аква ...) """
        return self.__get_kind(self.get_string_value(TransportReferent.ATTR_KIND))
    
    @kind.setter
    def kind(self, value) -> 'TransportKind':
        if (value != TransportKind.UNDEFINED): 
            self.add_slot(TransportReferent.ATTR_KIND, Utils.enumToString(value), True, 0)
        return value
    
    def __get_kind(self, s : str) -> 'TransportKind':
        if (s is None): 
            return TransportKind.UNDEFINED
        try: 
            res = Utils.valToEnum(s, TransportKind)
            if (isinstance(res, TransportKind)): 
                return Utils.valToEnum(res, TransportKind)
        except Exception as ex2527: 
            pass
        return TransportKind.UNDEFINED
    
    def _add_geo(self, r : object) -> None:
        from pullenti.ner.geo.GeoReferent import GeoReferent
        from pullenti.ner.ReferentToken import ReferentToken
        if (isinstance(r, GeoReferent)): 
            self.add_slot(TransportReferent.ATTR_STATE, r, False, 0)
        elif (isinstance(r, ReferentToken)): 
            if (isinstance((r if isinstance(r, ReferentToken) else None).get_referent(), GeoReferent)): 
                self.add_slot(TransportReferent.ATTR_STATE, (r if isinstance(r, ReferentToken) else None).get_referent(), True, 0)
                self.add_ext_referent(r if isinstance(r, ReferentToken) else None)
    
    def can_be_equals(self, obj : 'Referent', typ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
        tr = (obj if isinstance(obj, TransportReferent) else None)
        if (tr is None): 
            return False
        k1 = self.kind
        k2 = tr.kind
        if (k1 != k2): 
            if (k1 == TransportKind.SPACE and tr.find_slot(TransportReferent.ATTR_TYPE, "КОРАБЛЬ", True) is not None): 
                pass
            elif (k2 == TransportKind.SPACE and self.find_slot(TransportReferent.ATTR_TYPE, "КОРАБЛЬ", True) is not None): 
                k1 = TransportKind.SPACE
            else: 
                return False
        sl = self.find_slot(TransportReferent.ATTR_ORG, None, True)
        if (sl is not None and tr.find_slot(TransportReferent.ATTR_ORG, None, True) is not None): 
            if (tr.find_slot(TransportReferent.ATTR_ORG, sl.value, False) is None): 
                return False
        sl = self.find_slot(TransportReferent.ATTR_STATE, None, True)
        if (sl is not None and tr.find_slot(TransportReferent.ATTR_STATE, None, True) is not None): 
            if (tr.find_slot(TransportReferent.ATTR_STATE, sl.value, True) is None): 
                return False
        s1 = self.get_string_value(TransportReferent.ATTR_NUMBER)
        s2 = tr.get_string_value(TransportReferent.ATTR_NUMBER)
        if (s1 is not None or s2 is not None): 
            if (s1 is None or s2 is None): 
                if (typ == Referent.EqualType.DIFFERENTTEXTS): 
                    return False
            else: 
                if (s1 != s2): 
                    return False
                s1 = self.get_string_value(TransportReferent.ATTR_NUMBER_REGION)
                s2 = tr.get_string_value(TransportReferent.ATTR_NUMBER_REGION)
                if (s1 is not None or s2 is not None): 
                    if (s1 is None or s2 is None): 
                        if (typ == Referent.EqualType.DIFFERENTTEXTS): 
                            return False
                    elif (s1 != s2): 
                        return False
                return True
        s1 = self.get_string_value(TransportReferent.ATTR_BRAND)
        s2 = tr.get_string_value(TransportReferent.ATTR_BRAND)
        if (s1 is not None or s2 is not None): 
            if (s1 is None or s2 is None): 
                if (typ == Referent.EqualType.DIFFERENTTEXTS): 
                    return False
            elif (s1 != s2): 
                return False
        s1 = self.get_string_value(TransportReferent.ATTR_MODEL)
        s2 = tr.get_string_value(TransportReferent.ATTR_MODEL)
        if (s1 is not None or s2 is not None): 
            if (s1 is None or s2 is None): 
                if (typ == Referent.EqualType.DIFFERENTTEXTS): 
                    return False
            elif (s1 != s2): 
                return False
        for s in self.slots: 
            if (s.type_name == TransportReferent.ATTR_NAME): 
                if (tr.find_slot(TransportReferent.ATTR_NAME, s.value, True) is not None): 
                    return True
        if (s1 is not None and s2 is not None): 
            return True
        return False
    
    def merge_slots(self, obj : 'Referent', merge_statistic : bool=True) -> None:
        super().merge_slots(obj, merge_statistic)
        kinds = list()
        for s in self.slots: 
            if (s.type_name == TransportReferent.ATTR_KIND): 
                ki = self.__get_kind(s.value)
                if (not ki in kinds): 
                    kinds.append(ki)
        if (len(kinds) > 0): 
            if (TransportKind.SPACE in kinds): 
                for i in range(len(self.slots) - 1, -1, -1):
                    if (self.slots[i].type_name == TransportReferent.ATTR_KIND and self.__get_kind(self.slots[i].value) != TransportKind.SPACE): 
                        del self.slots[i]
    
    def _check(self, on_attach : bool) -> bool:
        ki = self.kind
        if (ki == TransportKind.UNDEFINED): 
            return False
        if (self.find_slot(TransportReferent.ATTR_NUMBER, None, True) is not None): 
            if (self.find_slot(TransportReferent.ATTR_NUMBER_REGION, None, True) is None and (len(self.slots) < 3)): 
                return False
            return True
        model = self.get_string_value(TransportReferent.ATTR_MODEL)
        has_num = False
        if (model is not None): 
            for s in model: 
                if (not str.isalpha(s)): 
                    has_num = True
                    break
        if (ki == TransportKind.AUTO): 
            if (self.find_slot(TransportReferent.ATTR_BRAND, None, True) is not None): 
                if (on_attach): 
                    return True
                if (not has_num and self.find_slot(TransportReferent.ATTR_TYPE, None, True) is None): 
                    return False
                return True
            if (model is not None and on_attach): 
                return True
            return False
        if (model is not None): 
            if (not has_num and ki == TransportKind.FLY and self.find_slot(TransportReferent.ATTR_BRAND, None, True) is None): 
                return False
            return True
        if (self.find_slot(TransportReferent.ATTR_NAME, None, True) is not None): 
            nam = self.get_string_value(TransportReferent.ATTR_NAME)
            if (ki == TransportKind.FLY and nam.startswith("Аэрофлот")): 
                return False
            return True
        if (ki == TransportKind.TRAIN): 
            pass
        return False