﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
from pullenti.unisharp.Utils import Utils
from pullenti.ner.Referent import Referent
from pullenti.morph.LanguageHelper import LanguageHelper


class WeaponReferent(Referent):
    
    def __init__(self) -> None:
        from pullenti.ner.weapon.internal.MetaWeapon import MetaWeapon
        super().__init__(WeaponReferent.OBJ_TYPENAME)
        self.instance_of = MetaWeapon._global_meta
    
    OBJ_TYPENAME = "WEAPON"
    
    ATTR_TYPE = "TYPE"
    
    ATTR_BRAND = "BRAND"
    
    ATTR_MODEL = "MODEL"
    
    ATTR_NAME = "NAME"
    
    ATTR_NUMBER = "NUMBER"
    
    ATTR_DATE = "DATE"
    
    def to_string(self, short_variant : bool, lang : 'MorphLang', lev : int=0) -> str:
        from pullenti.ner.core.MiscHelper import MiscHelper
        res = io.StringIO()
        str0_ = None
        for s in self.slots: 
            if (s.type_name == WeaponReferent.ATTR_TYPE): 
                n = s.value
                if (str0_ is None or (len(n) < len(str0_))): 
                    str0_ = n
        if (str0_ is not None): 
            print(str0_.lower(), end="", file=res)
        str0_ = self.get_string_value(WeaponReferent.ATTR_BRAND)
        if ((str0_) is not None): 
            print(" {0}".format(MiscHelper.convert_first_char_upper_and_other_lower(str0_)), end="", file=res, flush=True)
        str0_ = self.get_string_value(WeaponReferent.ATTR_MODEL)
        if ((str0_) is not None): 
            print(" {0}".format(str0_), end="", file=res, flush=True)
        str0_ = self.get_string_value(WeaponReferent.ATTR_NAME)
        if ((str0_) is not None): 
            print(" \"{0}\"".format(MiscHelper.convert_first_char_upper_and_other_lower(str0_)), end="", file=res, flush=True)
            for s in self.slots: 
                if (s.type_name == WeaponReferent.ATTR_NAME and str0_ != (s.value)): 
                    if (LanguageHelper.is_cyrillic_char(str0_[0]) != LanguageHelper.is_cyrillic_char((s.value)[0])): 
                        print(" ({0})".format(MiscHelper.convert_first_char_upper_and_other_lower(s.value)), end="", file=res, flush=True)
                        break
        str0_ = self.get_string_value(WeaponReferent.ATTR_NUMBER)
        if ((str0_) is not None): 
            print(", номер {0}".format(str0_), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    def can_be_equals(self, obj : 'Referent', typ : 'EqualType'=Referent.EqualType.WITHINONETEXT) -> bool:
        tr = (obj if isinstance(obj, WeaponReferent) else None)
        if (tr is None): 
            return False
        s1 = self.get_string_value(WeaponReferent.ATTR_NUMBER)
        s2 = tr.get_string_value(WeaponReferent.ATTR_NUMBER)
        if (s1 is not None or s2 is not None): 
            if (s1 is None or s2 is None): 
                if (typ == Referent.EqualType.DIFFERENTTEXTS): 
                    return False
            else: 
                if (s1 != s2): 
                    return False
                return True
        eq_types = False
        for t in self.get_string_values(WeaponReferent.ATTR_TYPE): 
            if (tr.find_slot(WeaponReferent.ATTR_TYPE, t, True) is not None): 
                eq_types = True
                break
        if (not eq_types): 
            return False
        s1 = self.get_string_value(WeaponReferent.ATTR_BRAND)
        s2 = tr.get_string_value(WeaponReferent.ATTR_BRAND)
        if (s1 is not None or s2 is not None): 
            if (s1 is None or s2 is None): 
                if (typ == Referent.EqualType.DIFFERENTTEXTS): 
                    return False
            elif (s1 != s2): 
                return False
        s1 = self.get_string_value(WeaponReferent.ATTR_MODEL)
        s2 = tr.get_string_value(WeaponReferent.ATTR_MODEL)
        if (s1 is not None or s2 is not None): 
            if (s1 is None or s2 is None): 
                if (typ == Referent.EqualType.DIFFERENTTEXTS): 
                    return False
            else: 
                if (self.find_slot(WeaponReferent.ATTR_MODEL, s2, True) is not None): 
                    return True
                if (tr.find_slot(WeaponReferent.ATTR_MODEL, s1, True) is not None): 
                    return True
                return False
        for s in self.slots: 
            if (s.type_name == WeaponReferent.ATTR_NAME): 
                if (tr.find_slot(WeaponReferent.ATTR_NAME, s.value, True) is not None): 
                    return True
        if (s1 is not None and s2 is not None): 
            return True
        return False
    
    def merge_slots(self, obj : 'Referent', merge_statistic : bool=True) -> None:
        super().merge_slots(obj, merge_statistic)