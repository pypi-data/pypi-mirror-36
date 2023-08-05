﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

import io
from pullenti.unisharp.Utils import Utils


class ResourceHelper:
    """ Это для поддержки получения встроенных ресурсов """
    
    @staticmethod
    def get_bytes(name : str) -> bytearray:
        # ignored: assembly = ResourceHelper.
        names = Utils.getResourcesNames('pullenti.ner.address.properties', '.dat;.png')
        for n in names: 
            if (Utils.endsWithString(n, name, True)): 
                try: 
                    inf = Utils.getResourceInfo('pullenti.ner.address.properties', n)
                    if (inf is None): 
                        continue
                    with Utils.getResourceStream('pullenti.ner.address.properties', n) as stream: 
                        buf = Utils.newArrayOfBytes(Utils.getLengthIO(stream), 0)
                        Utils.readIO(stream, buf, 0, len(buf))
                        return buf
                except Exception as ex: 
                    pass
        return None
    
    @staticmethod
    def get_string(name : str) -> str:
        arr = ResourceHelper.get_bytes(name)
        if (arr is None): 
            return None
        if ((len(arr) > 3 and arr[0] == (0xEF) and arr[1] == (0xBB)) and arr[2] == (0xBF)): 
            return arr[3:3+len(arr) - 3].decode('utf-8', 'ignore')
        else: 
            return arr.decode('utf-8', 'ignore')