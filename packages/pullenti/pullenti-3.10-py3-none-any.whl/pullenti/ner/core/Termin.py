﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import typing
import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphLang import MorphLang
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.ner.core.TerminParseAttr import TerminParseAttr


class Termin:
    """ Термин, понятие, система обозначений чего-либо и варианты его написания """
    
    class Term:
        """ Элемент термина (слово или число) """
        
        def __init__(self, src : 'TextToken', add_lemma_variant : bool=False, number : int=0) -> None:
            from pullenti.morph.MorphWordForm import MorphWordForm
            self.__m_source = None
            self.is_pattern_any = False
            self.__m_number = 0
            self.__m_variants = list()
            self.__m_gender = MorphGender.UNDEFINED
            self.__m_source = src
            if (src is not None): 
                self.variants.append(src.term)
                if (add_lemma_variant): 
                    lemma = src.lemma
                    if (lemma is not None and lemma != src.term): 
                        self.variants.append(lemma)
                    for wff in src.morph.items: 
                        wf = (wff if isinstance(wff, MorphWordForm) else None)
                        if (wf is not None and wf.is_in_dictionary): 
                            s = Utils.ifNotNull(wf.normal_full, wf.normal_case)
                            if (s != lemma and s != src.term): 
                                self.variants.append(s)
            if (number > (0)): 
                self.__m_number = number
                self.variants.append(str(number))
        
        @property
        def variants(self) -> typing.List[str]:
            """ Варианты морфологического написания """
            return self.__m_variants
        
        @property
        def canonical_text(self) -> str:
            """ Каноническое изображение (первый вариант) """
            return (self.__m_variants[0] if len(self.__m_variants) > 0 else "?")
        
        def __str__(self) -> str:
            if (self.is_pattern_any): 
                return "IsPatternAny"
            res = io.StringIO()
            for v in self.variants: 
                if (res.tell() > 0): 
                    print(", ", end="", file=res)
                print(v, end="", file=res)
            return Utils.toStringStringIO(res)
        
        @property
        def is_number(self) -> bool:
            """ Признак того, что это число """
            return self.__m_source is None
        
        @property
        def is_hiphen(self) -> bool:
            """ Это перенос """
            return self.__m_source is not None and self.__m_source.term == "-"
        
        @property
        def is_point(self) -> bool:
            """ Это точка """
            return self.__m_source is not None and self.__m_source.term == "."
        
        @property
        def gender(self) -> 'MorphGender':
            """ Род """
            from pullenti.morph.MorphWordForm import MorphWordForm
            if (self.__m_gender != MorphGender.UNDEFINED): 
                return self.__m_gender
            res = MorphGender.UNDEFINED
            if (self.__m_source is not None): 
                for wf in self.__m_source.morph.items: 
                    if ((wf if isinstance(wf, MorphWordForm) else None).is_in_dictionary): 
                        res = (Utils.valToEnum((res) | (wf.gender), MorphGender))
            return res
        
        @gender.setter
        def gender(self, value) -> 'MorphGender':
            self.__m_gender = value
            if (self.__m_source is not None): 
                for i in range(self.__m_source.morph.items_count - 1, -1, -1):
                    if ((((self.__m_source.morph.get_indexer_item(i).gender) & (value))) == (MorphGender.UNDEFINED)): 
                        self.__m_source.morph.remove_item(i)
            return value
        
        @property
        def _is_noun(self) -> bool:
            if (self.__m_source is not None): 
                for wf in self.__m_source.morph.items: 
                    if (wf.class0_.is_noun): 
                        return True
            return False
        
        @property
        def _is_adjective(self) -> bool:
            if (self.__m_source is not None): 
                for wf in self.__m_source.morph.items: 
                    if (wf.class0_.is_adjective): 
                        return True
            return False
        
        @property
        def morph_word_forms(self) -> typing.List['MorphWordForm']:
            from pullenti.morph.MorphWordForm import MorphWordForm
            res = list()
            if (self.__m_source is not None): 
                for wf in self.__m_source.morph.items: 
                    if (isinstance(wf, MorphWordForm)): 
                        res.append(wf if isinstance(wf, MorphWordForm) else None)
            return res
        
        def check_by_term(self, t : 'Term') -> bool:
            if (self.is_number): 
                return self.__m_number == t.__m_number
            if (self.__m_variants is not None and t.__m_variants is not None): 
                for v in self.__m_variants: 
                    if (v in t.__m_variants): 
                        return True
            return False
        
        def check_by_token(self, t : 'Token') -> bool:
            return self.__check(t, 0)
        
        def __check(self, t : 'Token', lev : int) -> bool:
            from pullenti.ner.TextToken import TextToken
            from pullenti.ner.MetaToken import MetaToken
            from pullenti.ner.NumberToken import NumberToken
            if (lev > 10): 
                return False
            if (self.is_pattern_any): 
                return True
            if (isinstance(t, TextToken)): 
                if (self.is_number): 
                    return False
                for v in self.variants: 
                    if (t.is_value(v, None)): 
                        return True
                return False
            if (isinstance(t, NumberToken)): 
                if (self.is_number): 
                    return self.__m_number == (t if isinstance(t, NumberToken) else None).value
                if (self.__m_source is not None): 
                    inoutarg617 = RefOutArgWrapper(0)
                    inoutres618 = Utils.tryParseInt(self.__m_source.term, inoutarg617)
                    val = inoutarg617.value
                    if (inoutres618): 
                        return val == (t if isinstance(t, NumberToken) else None).value
                return False
            if (isinstance(t, MetaToken)): 
                mt = (t if isinstance(t, MetaToken) else None)
                if (mt.begin_token == mt.end_token): 
                    if (self.__check(mt.begin_token, lev + 1)): 
                        return True
            return False
        
        def check_by_pref_token(self, prefix : 'Term', t : 'TextToken') -> bool:
            if (prefix is None or prefix.__m_source is None or t is None): 
                return False
            pref = prefix.canonical_text
            tterm = t.term
            if (pref[0] != tterm[0]): 
                return False
            if (not tterm.startswith(pref)): 
                return False
            for v in self.variants: 
                if (t.is_value(pref + v, None)): 
                    return True
            return False
        
        def check_by_str_pref_token(self, pref : str, t : 'TextToken') -> bool:
            if (pref is None or t is None): 
                return False
            for v in self.variants: 
                if (v.startswith(pref) and len(v) > len(pref)): 
                    if (t.is_value(v[len(pref):], None)): 
                        return True
            return False
        
        @staticmethod
        def _new1829(_arg1 : 'TextToken', _arg2 : bool) -> 'Term':
            res = Termin.Term(_arg1)
            res.is_pattern_any = _arg2
            return res
    
    class Abridge:
        
        def __init__(self) -> None:
            self.parts = list()
            self.tail = None
        
        def add_part(self, val : str, has_delim : bool=False) -> None:
            self.parts.append(Termin.AbridgePart._new619(val, has_delim))
        
        def __str__(self) -> str:
            if (self.tail is not None): 
                return "{0}-{1}".format(self.parts[0], self.tail)
            res = io.StringIO()
            for p in self.parts: 
                print(p, end="", file=res)
            return Utils.toStringStringIO(res)
        
        def try_attach(self, t0 : 'Token') -> 'TerminToken':
            from pullenti.ner.TextToken import TextToken
            from pullenti.ner.MetaToken import MetaToken
            from pullenti.ner.core.TerminToken import TerminToken
            from pullenti.ner.MorphCollection import MorphCollection
            t1 = (t0 if isinstance(t0, TextToken) else None)
            if (t1 is None): 
                return None
            if (t1.term != self.parts[0].value): 
                if (len(self.parts) != 1 or not t1.is_value(self.parts[0].value, None)): 
                    return None
            if (self.tail is None): 
                te = t1
                point = False
                if (te.next0_ is not None): 
                    if (te.next0_.is_char('.')): 
                        te = te.next0_
                        point = True
                    elif (len(self.parts) > 1): 
                        while te.next0_ is not None:
                            if (te.next0_.is_char_of("\\/.") or te.next0_.is_hiphen): 
                                te = te.next0_
                                point = True
                            else: 
                                break
                if (te is None): 
                    return None
                tt = te.next0_
                i = 1
                while i < len(self.parts): 
                    if (tt is not None and tt.whitespaces_before_count > 2): 
                        return None
                    if (tt is not None and ((tt.is_hiphen or tt.is_char_of("\\/.")))): 
                        tt = tt.next0_
                    elif (not point and self.parts[i - 1].has_delim): 
                        return None
                    if (tt is None): 
                        return None
                    if (isinstance(tt, TextToken)): 
                        tet = (tt if isinstance(tt, TextToken) else None)
                        if (tet.term != self.parts[i].value): 
                            if (not tet.is_value(self.parts[i].value, None)): 
                                return None
                    elif (isinstance(tt, MetaToken)): 
                        mt = (tt if isinstance(tt, MetaToken) else None)
                        if (mt.begin_token != mt.end_token): 
                            return None
                        if (not mt.begin_token.is_value(self.parts[i].value, None)): 
                            return None
                    te = tt
                    if (tt.next0_ is not None and ((tt.next0_.is_char_of(".\\/") or tt.next0_.is_hiphen))): 
                        tt = tt.next0_
                        point = True
                        if (tt is not None): 
                            te = tt
                    else: 
                        point = False
                    tt = tt.next0_
                    i += 1
                res = TerminToken._new620(t0, te, t0 == te)
                if (point): 
                    res.morph = MorphCollection()
                return res
            t1 = (t1.next0_ if isinstance(t1.next0_, TextToken) else None)
            if (t1 is None or not t1.is_char_of("-\\/")): 
                return None
            t1 = (t1.next0_ if isinstance(t1.next0_, TextToken) else None)
            if (t1 is None): 
                return None
            if (t1.term[0] != self.tail[0]): 
                return None
            return TerminToken(t0, t1)
    
    class AbridgePart:
        
        def __init__(self) -> None:
            self.value = None
            self.has_delim = False
        
        def __str__(self) -> str:
            if (self.has_delim): 
                return self.value + "."
            else: 
                return self.value
        
        @staticmethod
        def _new619(_arg1 : str, _arg2 : bool) -> 'AbridgePart':
            res = Termin.AbridgePart()
            res.value = _arg1
            res.has_delim = _arg2
            return res
        
        @staticmethod
        def _new621(_arg1 : str) -> 'AbridgePart':
            res = Termin.AbridgePart()
            res.value = _arg1
            return res
    
    def __init__(self, source : str=None, lang_ : 'MorphLang'=MorphLang(), source_is_normal : bool=False) -> None:
        """ Создать термин из строки с добавлением всех морфологических вариантов написания
        
        Args:
            source(str): строка
            lang_(MorphLang): возможный язык
            source_is_normal(bool): при true морфварианты не добавляются 
         (эквивалентно вызову InitByNormalText)
        """
        from pullenti.morph.Morphology import Morphology
        from pullenti.ner.TextToken import TextToken
        self.terms = list()
        self.additional_vars = None
        self.__m_canonic_text = None
        self.ignore_terms_order = False
        self.acronym = None
        self.acronym_smart = None
        self.acronym_can_be_lower = False
        self.abridges = None
        self.lang = MorphLang()
        self.tag = None
        self.tag2 = None
        if (source is None): 
            return
        if (source_is_normal or Termin.ASSIGN_ALL_TEXTS_AS_NORMAL): 
            self.init_by_normal_text(source, lang_)
            return
        toks = Morphology.process(source, lang_, None)
        if (toks is not None): 
            i = 0
            while i < len(toks): 
                tt = TextToken(toks[i], None)
                self.terms.append(Termin.Term(tt, not source_is_normal))
                i += 1
        self.lang = MorphLang(lang_)
    
    ASSIGN_ALL_TEXTS_AS_NORMAL = False
    
    def init_by_normal_text(self, text : str, lang_ : 'MorphLang'=MorphLang()) -> None:
        from pullenti.ner.TextToken import TextToken
        from pullenti.morph.Morphology import Morphology
        if (Utils.isNullOrEmpty(text)): 
            return
        text = text.upper()
        if (text.find('\'') >= 0): 
            text = text.replace("'", "")
        tok = False
        sp = False
        for ch in text: 
            if (not str.isalpha(ch)): 
                if (ch == ' '): 
                    sp = True
                else: 
                    tok = True
                    break
        if (not tok and not sp): 
            tt = TextToken(None, None)
            tt.term = text
            self.terms.append(Termin.Term(tt, False))
        elif (not tok and sp): 
            wrds = Utils.splitString(text, ' ', False)
            i = 0
            while i < len(wrds): 
                tt = TextToken(None, None)
                tt.term = wrds[i]
                self.terms.append(Termin.Term(tt, False))
                i += 1
        else: 
            toks = Morphology.tokenize(text)
            if (toks is not None): 
                i = 0
                while i < len(toks): 
                    tt = TextToken(toks[i], None)
                    self.terms.append(Termin.Term(tt, False))
                    i += 1
        self.lang = MorphLang(lang_)
    
    def init_by(self, begin : 'Token', end : 'Token', tag_ : object=None, add_lemma_variant : bool=False) -> None:
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.NumberToken import NumberToken
        if (tag_ is not None): 
            self.tag = tag_
        t = begin
        while t is not None: 
            if (self.lang.is_undefined and not t.morph.language.is_undefined): 
                self.lang = t.morph.language
            tt = (t if isinstance(t, TextToken) else None)
            if (tt is not None): 
                self.terms.append(Termin.Term(tt, add_lemma_variant))
            elif (isinstance(t, NumberToken)): 
                self.terms.append(Termin.Term(None, False, (t if isinstance(t, NumberToken) else None).value))
            if (t == end): 
                break
            t = t.next0_
    
    def add_variant(self, var : str, source_is_normal : bool=False) -> None:
        if (self.additional_vars is None): 
            self.additional_vars = list()
        self.additional_vars.append(Termin(var, MorphLang.UNKNOWN, source_is_normal))
    
    def add_variant_term(self, t : 'Termin') -> None:
        if (self.additional_vars is None): 
            self.additional_vars = list()
        self.additional_vars.append(t)
    
    @property
    def canonic_text(self) -> str:
        """ Каноноический текст """
        if (self.__m_canonic_text is not None): 
            return self.__m_canonic_text
        if (len(self.terms) > 0): 
            tmp = io.StringIO()
            for v in self.terms: 
                if (tmp.tell() > 0): 
                    print(' ', end="", file=tmp)
                print(v.canonical_text, end="", file=tmp)
            self.__m_canonic_text = Utils.toStringStringIO(tmp)
        elif (self.acronym is not None): 
            self.__m_canonic_text = self.acronym
        return Utils.ifNotNull(self.__m_canonic_text, "?")
    
    @canonic_text.setter
    def canonic_text(self, value) -> str:
        self.__m_canonic_text = value
        return value
    
    def set_std_acronim(self, smart : bool) -> None:
        acr = io.StringIO()
        for t in self.terms: 
            s = t.canonical_text
            if (Utils.isNullOrEmpty(s)): 
                continue
            if (len(s) > 2): 
                print(s[0], end="", file=acr)
        if (acr.tell() > 1): 
            if (smart): 
                self.acronym_smart = Utils.toStringStringIO(acr)
            else: 
                self.acronym = Utils.toStringStringIO(acr)
    
    def add_abridge(self, abr : str) -> 'Abridge':
        if (abr == "В/ГОР"): 
            pass
        a = Termin.Abridge()
        if (self.abridges is None): 
            self.abridges = list()
        i = 0
        while i < len(abr): 
            if (not str.isalpha(abr[i])): 
                break
            i += 1
        if (i == 0): 
            return None
        a.parts.append(Termin.AbridgePart._new621(abr[0:0+i].upper()))
        self.abridges.append(a)
        if (((i + 1) < len(abr)) and abr[i] == '-'): 
            a.tail = abr[i + 1:].upper()
        elif (i < len(abr)): 
            if (not Utils.isWhitespace(abr[i])): 
                a.parts[0].has_delim = True
            while i < len(abr): 
                if (str.isalpha(abr[i])): 
                    j = (i + 1)
                    while j < len(abr): 
                        if (not str.isalpha(abr[j])): 
                            break
                        j += 1
                    p = Termin.AbridgePart._new621(abr[i:i+j - i].upper())
                    if (j < len(abr)): 
                        if (not Utils.isWhitespace(abr[j])): 
                            p.has_delim = True
                    a.parts.append(p)
                    i = j
                i += 1
        return a
    
    @property
    def gender(self) -> 'MorphGender':
        """ Род (первого термина) """
        if (len(self.terms) > 0): 
            if (len(self.terms) > 0 and self.terms[0]._is_adjective and self.terms[len(self.terms) - 1]._is_noun): 
                return self.terms[len(self.terms) - 1].gender
            return self.terms[0].gender
        else: 
            return MorphGender.UNDEFINED
    
    @gender.setter
    def gender(self, value) -> 'MorphGender':
        if (len(self.terms) > 0): 
            self.terms[0].gender = value
        return value
    
    def copy_to(self, dst : 'Termin') -> None:
        dst.terms = self.terms
        dst.ignore_terms_order = self.ignore_terms_order
        dst.acronym = self.acronym
        dst.abridges = self.abridges
        dst.lang = self.lang
        dst.__m_canonic_text = self.__m_canonic_text
    
    def __str__(self) -> str:
        res = io.StringIO()
        if (len(self.terms) > 0): 
            i = 0
            while i < len(self.terms): 
                if (i > 0): 
                    print(' ', end="", file=res)
                print(self.terms[i].canonical_text, end="", file=res)
                i += 1
        if (self.acronym is not None): 
            if (res.tell() > 0): 
                print(", ", end="", file=res)
            print(self.acronym, end="", file=res)
        if (self.acronym_smart is not None): 
            if (res.tell() > 0): 
                print(", ", end="", file=res)
            print(self.acronym_smart, end="", file=res)
        if (self.abridges is not None): 
            for a in self.abridges: 
                if (res.tell() > 0): 
                    print(", ", end="", file=res)
                print(a, end="", file=res)
        return Utils.toStringStringIO(res)
    
    M_STD_ABRIDE_PREFIXES = None
    
    def add_std_abridges(self) -> None:
        if (len(self.terms) != 2): 
            return
        first = self.terms[0].canonical_text
        i = 0
        while i < len(Termin.M_STD_ABRIDE_PREFIXES): 
            if (first.startswith(Termin.M_STD_ABRIDE_PREFIXES[i])): 
                break
            i += 1
        if (i >= len(Termin.M_STD_ABRIDE_PREFIXES)): 
            return
        head = Termin.M_STD_ABRIDE_PREFIXES[i]
        second = self.terms[1].canonical_text
        i = 0
        while i < len(head): 
            if (not LanguageHelper.is_cyrillic_vowel(head[i])): 
                a = Termin.Abridge()
                a.add_part(head[0:0+i + 1], False)
                a.add_part(second, False)
                if (self.abridges is None): 
                    self.abridges = list()
                self.abridges.append(a)
            i += 1
    
    def add_all_abridges(self, tail_len : int=0, max_first_len : int=0, min_first_len : int=0) -> None:
        if (len(self.terms) < 1): 
            return
        txt = self.terms[0].canonical_text
        if (tail_len == 0): 
            for i in range(len(txt) - 2, -1, -1):
                if (not LanguageHelper.is_cyrillic_vowel(txt[i])): 
                    if (min_first_len > 0 and (i < (min_first_len - 1))): 
                        break
                    a = Termin.Abridge()
                    a.add_part(txt[0:0+i + 1], False)
                    j = 1
                    while j < len(self.terms): 
                        a.add_part(self.terms[j].canonical_text, False)
                        j += 1
                    if (self.abridges is None): 
                        self.abridges = list()
                    self.abridges.append(a)
        else: 
            tail = txt[len(txt) - tail_len:]
            txt = txt[0:0+len(txt) - tail_len - 1]
            for i in range(len(txt) - 2, -1, -1):
                if (max_first_len > 0 and i >= max_first_len): 
                    pass
                elif (not LanguageHelper.is_cyrillic_vowel(txt[i])): 
                    self.add_abridge("{0}-{1}".format(txt[0:0+i + 1], tail))
    
    def _get_hash_variants(self) -> typing.List[str]:
        res = list()
        j = 0
        while j < len(self.terms): 
            for v in self.terms[j].variants: 
                if (not v in res): 
                    res.append(v)
            if (((j + 2) < len(self.terms)) and self.terms[j + 1].is_hiphen): 
                pref = self.terms[j].canonical_text
                for v in self.terms[j + 2].variants: 
                    if (not pref + v in res): 
                        res.append(pref + v)
            if (not self.ignore_terms_order): 
                break
            j += 1
        if (self.acronym is not None): 
            if (not self.acronym in res): 
                res.append(self.acronym)
        if (self.acronym_smart is not None): 
            if (not self.acronym_smart in res): 
                res.append(self.acronym_smart)
        if (self.abridges is not None): 
            for a in self.abridges: 
                if (len(a.parts[0].value) > 1): 
                    if (not a.parts[0].value in res): 
                        res.append(a.parts[0].value)
        return res
    
    def is_equal(self, t : 'Termin') -> bool:
        if (t.acronym is not None): 
            if (self.acronym == t.acronym or self.acronym_smart == t.acronym): 
                return True
        if (t.acronym_smart is not None): 
            if (self.acronym == t.acronym_smart or self.acronym_smart == t.acronym_smart): 
                return True
        if (len(t.terms) != len(self.terms)): 
            return False
        i = 0
        while i < len(self.terms): 
            if (not self.terms[i].check_by_term(t.terms[i])): 
                return False
            i += 1
        return True
    
    def try_parse(self, t0 : 'Token', pars : 'TerminParseAttr'=TerminParseAttr.NO) -> 'TerminToken':
        from pullenti.ner.TextToken import TextToken
        from pullenti.ner.core.TerminToken import TerminToken
        from pullenti.ner.core.BracketHelper import BracketHelper
        from pullenti.ner.ReferentToken import ReferentToken
        from pullenti.ner.core.MiscHelper import MiscHelper
        from pullenti.ner.NumberToken import NumberToken
        from pullenti.ner.MorphCollection import MorphCollection
        if (t0 is None): 
            return None
        term = None
        if (isinstance(t0, TextToken)): 
            term = (t0 if isinstance(t0, TextToken) else None).term
        if (self.acronym_smart is not None and (((pars) & (TerminParseAttr.FULLWORDSONLY))) == (TerminParseAttr.NO) and term is not None): 
            if (self.acronym_smart == term): 
                if (t0.next0_ is not None and t0.next0_.is_char('.') and not t0.is_whitespace_after): 
                    return TerminToken._new623(t0, t0.next0_, self)
                else: 
                    return TerminToken._new623(t0, t0, self)
            t1 = (t0 if isinstance(t0, TextToken) else None)
            tt = (t0 if isinstance(t0, TextToken) else None)
            i = 0
            while i < len(self.acronym): 
                if (tt is None): 
                    break
                term1 = tt.term
                if (len(term1) != 1 or tt.is_whitespace_after): 
                    break
                if (i > 0 and tt.is_whitespace_before): 
                    break
                if (term1[0] != self.acronym[i]): 
                    break
                if (tt.next0_ is None or not tt.next0_.is_char('.')): 
                    break
                t1 = (tt.next0_ if isinstance(tt.next0_, TextToken) else None)
                tt = (tt.next0_.next0_ if isinstance(tt.next0_.next0_, TextToken) else None)
                i += 1
            if (i >= len(self.acronym)): 
                return TerminToken._new623(t0, t1, self)
        if (self.acronym is not None and term is not None and self.acronym == term): 
            if (t0.chars.is_all_upper or self.acronym_can_be_lower or ((not t0.chars.is_all_lower and len(term) >= 3))): 
                return TerminToken._new623(t0, t0, self)
        if (self.acronym is not None and t0.chars.is_last_lower and t0.length_char > 3): 
            if (t0.is_value(self.acronym, None)): 
                return TerminToken._new623(t0, t0, self)
        cou = 0
        i = 0
        while i < len(self.terms): 
            if (self.terms[i].is_hiphen): 
                cou -= 1
            else: 
                cou += 1
            i += 1
        if (len(self.terms) > 0 and ((not self.ignore_terms_order or cou == 1))): 
            t1 = t0
            tt = t0
            e0_ = None
            eup = None
            ok = True
            mc = None
            dont_change_mc = False
            i = 0
            first_pass3717 = True
            while True:
                if first_pass3717: first_pass3717 = False
                else: i += 1
                if (not (i < len(self.terms))): break
                if (self.terms[i].is_hiphen): 
                    continue
                if (tt is not None and tt.is_hiphen and i > 0): 
                    tt = tt.next0_
                if (i > 0 and tt is not None): 
                    if ((((pars) & (TerminParseAttr.IGNOREBRACKETS))) != (TerminParseAttr.NO) and not tt.chars.is_letter and BracketHelper.is_bracket(tt, False)): 
                        tt = tt.next0_
                if (((((pars) & (TerminParseAttr.CANBEGEOOBJECT))) != (TerminParseAttr.NO) and i > 0 and (isinstance(tt, ReferentToken))) and tt.get_referent().type_name == "GEO"): 
                    tt = tt.next0_
                if ((isinstance(tt, ReferentToken)) and e0_ is None): 
                    eup = tt
                    e0_ = (tt if isinstance(tt, ReferentToken) else None).end_token
                    tt = (tt if isinstance(tt, ReferentToken) else None).begin_token
                if (tt is None): 
                    ok = False
                    break
                if (not self.terms[i].check_by_token(tt)): 
                    if (tt.next0_ is not None and tt.is_char('.') and self.terms[i].check_by_token(tt.next0_)): 
                        tt = tt.next0_
                    elif (((i > 0 and tt.next0_ is not None and (isinstance(tt, TextToken))) and ((tt.morph.class0_.is_preposition or MiscHelper.is_eng_article(tt))) and self.terms[i].check_by_token(tt.next0_)) and not self.terms[i - 1].is_pattern_any): 
                        tt = tt.next0_
                    else: 
                        ok = False
                        if (((i + 2) < len(self.terms)) and self.terms[i + 1].is_hiphen and self.terms[i + 2].check_by_pref_token(self.terms[i], (tt if isinstance(tt, TextToken) else None))): 
                            i += 2
                            ok = True
                        elif (((not tt.is_whitespace_after and tt.next0_ is not None and (isinstance(tt, TextToken))) and (tt if isinstance(tt, TextToken) else None).length_char == 1 and tt.next0_.is_char_of("\"'`’“”")) and not tt.next0_.is_whitespace_after and (isinstance(tt.next0_.next0_, TextToken))): 
                            if (self.terms[i].check_by_str_pref_token((tt if isinstance(tt, TextToken) else None).term, (tt.next0_.next0_ if isinstance(tt.next0_.next0_, TextToken) else None))): 
                                ok = True
                                tt = tt.next0_.next0_
                        if (not ok): 
                            if (i > 0 and (((pars) & (TerminParseAttr.IGNORESTOPWORDS))) != (TerminParseAttr.NO)): 
                                if (isinstance(tt, TextToken)): 
                                    if (not tt.chars.is_letter): 
                                        tt = tt.next0_
                                        i -= 1
                                        continue
                                    mc1 = tt.get_morph_class_in_dictionary()
                                    if (mc1.is_conjunction or mc1.is_preposition): 
                                        tt = tt.next0_
                                        i -= 1
                                        continue
                                if (isinstance(tt, NumberToken)): 
                                    tt = tt.next0_
                                    i -= 1
                                    continue
                            break
                if (tt.morph.items_count > 0 and not dont_change_mc): 
                    mc = MorphCollection(tt.morph)
                    if (((mc.class0_.is_noun or mc.class0_.is_verb)) and not mc.class0_.is_adjective): 
                        if (((i + 1) < len(self.terms)) and self.terms[i + 1].is_hiphen): 
                            pass
                        else: 
                            dont_change_mc = True
                if (tt.morph.class0_.is_preposition or tt.morph.class0_.is_conjunction): 
                    dont_change_mc = True
                if (tt == e0_): 
                    tt = eup
                    eup = (None)
                    e0_ = (None)
                if (e0_ is None): 
                    t1 = tt
                tt = tt.next0_
            if (ok and i >= len(self.terms)): 
                if (t1.next0_ is not None and t1.next0_.is_char('.') and self.abridges is not None): 
                    for a in self.abridges: 
                        if (a.try_attach(t0) is not None): 
                            t1 = t1.next0_
                            break
                return TerminToken._new628(t0, t1, mc)
        if (len(self.terms) > 1 and self.ignore_terms_order): 
            terms_ = list(self.terms)
            t1 = t0
            tt = t0
            while len(terms_) > 0:
                if (tt != t0 and tt is not None and tt.is_hiphen): 
                    tt = tt.next0_
                if (tt is None): 
                    break
                j = 0
                while j < len(terms_): 
                    if (terms_[j].check_by_token(tt)): 
                        break
                    j += 1
                if (j >= len(terms_)): 
                    if (tt != t0 and (((pars) & (TerminParseAttr.IGNORESTOPWORDS))) != (TerminParseAttr.NO)): 
                        if (isinstance(tt, TextToken)): 
                            if (not tt.chars.is_letter): 
                                tt = tt.next0_
                                continue
                            mc1 = tt.get_morph_class_in_dictionary()
                            if (mc1.is_conjunction or mc1.is_preposition): 
                                tt = tt.next0_
                                continue
                        if (isinstance(tt, NumberToken)): 
                            tt = tt.next0_
                            continue
                    break
                del terms_[j]
                t1 = tt
                tt = tt.next0_
            for i in range(len(terms_) - 1, -1, -1):
                if (terms_[i].is_hiphen): 
                    del terms_[i]
            if (len(terms_) == 0): 
                return TerminToken(t0, t1)
        if (self.abridges is not None and (((pars) & (TerminParseAttr.FULLWORDSONLY))) == (TerminParseAttr.NO)): 
            res = None
            for a in self.abridges: 
                r = a.try_attach(t0)
                if (r is None): 
                    continue
                if (r.abridge_without_point and len(self.terms) > 0): 
                    if (not ((isinstance(t0, TextToken)))): 
                        continue
                    if (a.parts[0].value != (t0 if isinstance(t0, TextToken) else None).term): 
                        continue
                if (res is None or (res.length_char < r.length_char)): 
                    res = r
            if (res is not None): 
                return res
        return None
    
    @staticmethod
    def _new113(_arg1 : str, _arg2 : str) -> 'Termin':
        res = Termin(_arg1)
        res.acronym = _arg2
        return res
    
    @staticmethod
    def _new118(_arg1 : str, _arg2 : object) -> 'Termin':
        res = Termin(_arg1)
        res.tag = _arg2
        return res
    
    @staticmethod
    def _new119(_arg1 : str, _arg2 : object, _arg3 : 'MorphLang') -> 'Termin':
        res = Termin(_arg1)
        res.tag = _arg2
        res.lang = _arg3
        return res
    
    @staticmethod
    def _new120(_arg1 : str, _arg2 : object, _arg3 : object) -> 'Termin':
        res = Termin(_arg1)
        res.tag = _arg2
        res.tag2 = _arg3
        return res
    
    @staticmethod
    def _new142(_arg1 : str, _arg2 : str, _arg3 : object) -> 'Termin':
        res = Termin(_arg1)
        res.canonic_text = _arg2
        res.tag = _arg3
        return res
    
    @staticmethod
    def _new144(_arg1 : str, _arg2 : object, _arg3 : str) -> 'Termin':
        res = Termin(_arg1)
        res.tag = _arg2
        res.acronym = _arg3
        return res
    
    @staticmethod
    def _new181(_arg1 : str, _arg2 : str, _arg3 : bool) -> 'Termin':
        res = Termin(_arg1)
        res.acronym = _arg2
        res.acronym_can_be_lower = _arg3
        return res
    
    @staticmethod
    def _new259(_arg1 : str, _arg2 : object, _arg3 : 'MorphGender') -> 'Termin':
        res = Termin(_arg1)
        res.tag = _arg2
        res.gender = _arg3
        return res
    
    @staticmethod
    def _new260(_arg1 : str, _arg2 : object, _arg3 : 'MorphLang', _arg4 : 'MorphGender') -> 'Termin':
        res = Termin(_arg1)
        res.tag = _arg2
        res.lang = _arg3
        res.gender = _arg4
        return res
    
    @staticmethod
    def _new262(_arg1 : str, _arg2 : object, _arg3 : object, _arg4 : 'MorphGender') -> 'Termin':
        res = Termin(_arg1)
        res.tag = _arg2
        res.tag2 = _arg3
        res.gender = _arg4
        return res
    
    @staticmethod
    def _new263(_arg1 : str, _arg2 : object, _arg3 : 'MorphLang', _arg4 : object, _arg5 : 'MorphGender') -> 'Termin':
        res = Termin(_arg1)
        res.tag = _arg2
        res.lang = _arg3
        res.tag2 = _arg4
        res.gender = _arg5
        return res
    
    @staticmethod
    def _new290(_arg1 : str, _arg2 : object, _arg3 : str, _arg4 : object, _arg5 : 'MorphGender') -> 'Termin':
        res = Termin(_arg1)
        res.tag = _arg2
        res.acronym = _arg3
        res.tag2 = _arg4
        res.gender = _arg5
        return res
    
    @staticmethod
    def _new303(_arg1 : str, _arg2 : str, _arg3 : object, _arg4 : object, _arg5 : 'MorphGender') -> 'Termin':
        res = Termin(_arg1)
        res.canonic_text = _arg2
        res.tag = _arg3
        res.tag2 = _arg4
        res.gender = _arg5
        return res
    
    @staticmethod
    def _new307(_arg1 : str, _arg2 : str, _arg3 : object, _arg4 : 'MorphLang', _arg5 : object, _arg6 : 'MorphGender') -> 'Termin':
        res = Termin(_arg1)
        res.canonic_text = _arg2
        res.tag = _arg3
        res.lang = _arg4
        res.tag2 = _arg5
        res.gender = _arg6
        return res
    
    @staticmethod
    def _new308(_arg1 : str, _arg2 : str, _arg3 : object, _arg4 : 'MorphGender') -> 'Termin':
        res = Termin(_arg1)
        res.acronym = _arg2
        res.tag = _arg3
        res.gender = _arg4
        return res
    
    @staticmethod
    def _new331(_arg1 : object, _arg2 : bool) -> 'Termin':
        res = Termin()
        res.tag = _arg1
        res.ignore_terms_order = _arg2
        return res
    
    @staticmethod
    def _new416(_arg1 : str, _arg2 : object, _arg3 : object, _arg4 : 'MorphLang') -> 'Termin':
        res = Termin(_arg1)
        res.tag = _arg2
        res.tag2 = _arg3
        res.lang = _arg4
        return res
    
    @staticmethod
    def _new477(_arg1 : str, _arg2 : 'MorphLang', _arg3 : object) -> 'Termin':
        res = Termin(_arg1, _arg2)
        res.tag = _arg3
        return res
    
    @staticmethod
    def _new534(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : str, _arg5 : object) -> 'Termin':
        res = Termin(_arg1, _arg2, _arg3)
        res.canonic_text = _arg4
        res.tag = _arg5
        return res
    
    @staticmethod
    def _new692(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : str) -> 'Termin':
        res = Termin(_arg1, _arg2, _arg3)
        res.canonic_text = _arg4
        return res
    
    @staticmethod
    def _new694(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : object) -> 'Termin':
        res = Termin(_arg1, _arg2, _arg3)
        res.tag = _arg4
        return res
    
    @staticmethod
    def _new886(_arg1 : str, _arg2 : 'MorphLang') -> 'Termin':
        res = Termin(_arg1)
        res.lang = _arg2
        return res
    
    @staticmethod
    def _new897(_arg1 : str, _arg2 : 'MorphLang', _arg3 : object, _arg4 : object) -> 'Termin':
        res = Termin(_arg1, _arg2)
        res.tag = _arg3
        res.tag2 = _arg4
        return res
    
    @staticmethod
    def _new901(_arg1 : str, _arg2 : 'MorphLang', _arg3 : object, _arg4 : str) -> 'Termin':
        res = Termin(_arg1, _arg2)
        res.tag = _arg3
        res.acronym = _arg4
        return res
    
    @staticmethod
    def _new907(_arg1 : str, _arg2 : str, _arg3 : 'MorphLang', _arg4 : object) -> 'Termin':
        res = Termin(_arg1)
        res.canonic_text = _arg2
        res.lang = _arg3
        res.tag = _arg4
        return res
    
    @staticmethod
    def _new910(_arg1 : str, _arg2 : object, _arg3 : str, _arg4 : object) -> 'Termin':
        res = Termin(_arg1)
        res.tag = _arg2
        res.acronym = _arg3
        res.tag2 = _arg4
        return res
    
    @staticmethod
    def _new912(_arg1 : str, _arg2 : 'MorphLang', _arg3 : object, _arg4 : str, _arg5 : object) -> 'Termin':
        res = Termin(_arg1, _arg2)
        res.tag = _arg3
        res.acronym = _arg4
        res.tag2 = _arg5
        return res
    
    @staticmethod
    def _new981(_arg1 : str, _arg2 : 'MorphLang', _arg3 : str, _arg4 : object) -> 'Termin':
        res = Termin(_arg1, _arg2)
        res.canonic_text = _arg3
        res.tag = _arg4
        return res
    
    @staticmethod
    def _new988(_arg1 : str, _arg2 : str, _arg3 : object, _arg4 : object) -> 'Termin':
        res = Termin(_arg1)
        res.acronym = _arg2
        res.tag = _arg3
        res.tag2 = _arg4
        return res
    
    @staticmethod
    def _new1085(_arg1 : str, _arg2 : str) -> 'Termin':
        res = Termin(_arg1)
        res.canonic_text = _arg2
        return res
    
    @staticmethod
    def _new1120(_arg1 : str, _arg2 : 'MorphLang', _arg3 : str) -> 'Termin':
        res = Termin(_arg1, _arg2)
        res.canonic_text = _arg3
        return res
    
    @staticmethod
    def _new1217(_arg1 : str, _arg2 : 'MorphLang') -> 'Termin':
        res = Termin()
        res.acronym = _arg1
        res.lang = _arg2
        return res
    
    @staticmethod
    def _new1398(_arg1 : str, _arg2 : 'MorphLang', _arg3 : str) -> 'Termin':
        res = Termin(_arg1, _arg2)
        res.acronym = _arg3
        return res
    
    @staticmethod
    def _new2194(_arg1 : str, _arg2 : object) -> 'Termin':
        res = Termin(_arg1)
        res.tag2 = _arg2
        return res
    
    @staticmethod
    def _new2439(_arg1 : str, _arg2 : bool) -> 'Termin':
        res = Termin(_arg1)
        res.ignore_terms_order = _arg2
        return res
    
    @staticmethod
    def _new2461(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : object) -> 'Termin':
        res = Termin(_arg1, _arg2, _arg3)
        res.tag2 = _arg4
        return res
    
    @staticmethod
    def _new2550(_arg1 : str, _arg2 : str, _arg3 : object, _arg4 : str) -> 'Termin':
        res = Termin(_arg1)
        res.canonic_text = _arg2
        res.tag = _arg3
        res.acronym = _arg4
        return res
    
    @staticmethod
    def _new2560(_arg1 : str, _arg2 : str, _arg3 : object, _arg4 : str, _arg5 : bool) -> 'Termin':
        res = Termin(_arg1)
        res.canonic_text = _arg2
        res.tag = _arg3
        res.acronym = _arg4
        res.acronym_can_be_lower = _arg5
        return res
    
    @staticmethod
    def _new2572(_arg1 : str, _arg2 : 'MorphLang', _arg3 : bool, _arg4 : str, _arg5 : object, _arg6 : object) -> 'Termin':
        res = Termin(_arg1, _arg2, _arg3)
        res.canonic_text = _arg4
        res.tag = _arg5
        res.tag2 = _arg6
        return res
    
    @staticmethod
    def _new2573(_arg1 : str, _arg2 : str, _arg3 : object, _arg4 : object) -> 'Termin':
        res = Termin(_arg1)
        res.canonic_text = _arg2
        res.tag = _arg3
        res.tag2 = _arg4
        return res
    
    @staticmethod
    def _new2576(_arg1 : str, _arg2 : str, _arg3 : str, _arg4 : object, _arg5 : object, _arg6 : bool) -> 'Termin':
        res = Termin(_arg1)
        res.canonic_text = _arg2
        res.acronym = _arg3
        res.tag = _arg4
        res.tag2 = _arg5
        res.acronym_can_be_lower = _arg6
        return res
    
    @staticmethod
    def _new2594(_arg1 : str, _arg2 : str, _arg3 : object) -> 'Termin':
        res = Termin(_arg1)
        res.acronym = _arg2
        res.tag = _arg3
        return res
    
    @staticmethod
    def _new2603(_arg1 : str, _arg2 : str, _arg3 : str, _arg4 : object) -> 'Termin':
        res = Termin(_arg1)
        res.canonic_text = _arg2
        res.acronym = _arg3
        res.tag = _arg4
        return res
    
    # static constructor for class Termin
    @staticmethod
    def _static_ctor():
        Termin.M_STD_ABRIDE_PREFIXES = ["НИЖ", "ВЕРХ", "МАЛ", "БОЛЬШ", "НОВ", "СТАР"]

Termin._static_ctor()