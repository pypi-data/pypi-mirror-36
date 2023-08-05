﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.ner.ReferentClass import ReferentClass


class MetaInstrument(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.instrument.InstrumentBlockReferent import InstrumentBlockReferent
        from pullenti.ner.instrument.InstrumentReferent import InstrumentReferent
        super().__init__()
        self.add_feature(InstrumentReferent.ATTR_TYPE, "Тип", 0, 1)
        self.add_feature(InstrumentBlockReferent.ATTR_NUMBER, "Номер", 0, 1)
        self.add_feature(InstrumentReferent.ATTR_CASENUMBER, "Номер дела", 0, 1)
        self.add_feature(InstrumentReferent.ATTR_DATE, "Дата", 0, 1)
        self.add_feature(InstrumentReferent.ATTR_SOURCE, "Публикующий орган", 0, 1)
        self.add_feature(InstrumentReferent.ATTR_GEO, "Географический объект", 0, 1)
        self.add_feature(InstrumentBlockReferent.ATTR_NAME, "Наименование", 0, 0)
        self.add_feature(InstrumentBlockReferent.ATTR_CHILD, "Внутренний элемент", 0, 0).show_as_parent = True
        self.add_feature(InstrumentReferent.ATTR_SIGNER, "Подписант", 0, 1)
        self.add_feature(InstrumentReferent.ATTR_PART, "Часть", 0, 1)
        self.add_feature(InstrumentReferent.ATTR_APPENDIX, "Приложение", 0, 0)
        self.add_feature(InstrumentReferent.ATTR_PARTICIPANT, "Участник", 0, 0).show_as_parent = True
        self.add_feature(InstrumentReferent.ATTR_ARTEFACT, "Артефакт", 0, 0).show_as_parent = True
    
    @property
    def name(self) -> str:
        from pullenti.ner.instrument.InstrumentReferent import InstrumentReferent
        return InstrumentReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Нормативно-правовой акт"
    
    DOC_IMAGE_ID = "decree"
    
    PART_IMAGE_ID = "part"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        return MetaInstrument.DOC_IMAGE_ID
    
    GLOBAL_META = None
    
    # static constructor for class MetaInstrument
    @staticmethod
    def _static_ctor():
        MetaInstrument.GLOBAL_META = MetaInstrument()

MetaInstrument._static_ctor()