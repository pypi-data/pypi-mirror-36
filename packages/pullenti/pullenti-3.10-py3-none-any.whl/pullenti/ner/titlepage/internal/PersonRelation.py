﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
from pullenti.unisharp.Utils import Utils


class PersonRelation:
    
    def __init__(self) -> None:
        self.person = None
        self.coefs = dict()
    
    @property
    def best(self) -> 'Types':
        from pullenti.ner.titlepage.internal.TitleItemToken import TitleItemToken
        res = TitleItemToken.Types.UNDEFINED
        max0_ = 0
        for v in self.coefs.items(): 
            if (v[1] > max0_): 
                res = v[0]
                max0_ = v[1]
            elif (v[1] == max0_): 
                res = TitleItemToken.Types.UNDEFINED
        return res
    
    def __str__(self) -> str:
        from pullenti.morph.MorphLang import MorphLang
        res = io.StringIO()
        print("{0} {1}".format(self.person.to_string(True, MorphLang.UNKNOWN, 0), Utils.enumToString(self.best)), end="", file=res, flush=True)
        for v in self.coefs.items(): 
            print(" {0}({1})".format(v[1], Utils.enumToString(v[0])), end="", file=res, flush=True)
        return Utils.toStringStringIO(res)
    
    @staticmethod
    def _new2478(_arg1 : 'PersonReferent') -> 'PersonRelation':
        res = PersonRelation()
        res.person = _arg1
        return res