from .ctconfig import CTConfig
from .eligibility import process_eligibility_naive

def __getattr__(name):
    if name == "CTProc":
        from .proc import CTProc
        return CTProc
    if name == "CTDocument":
        from .ctdocument import CTDocument
        return CTDocument
    if name == "EligCrit":
        from .ctdocument import EligCrit
        return EligCrit
    if name == "CTTopic":
        from .cttopic import CTTopic
        return CTTopic
    if name in ("CTBase", "CTEntity", "NLPTools"):
        from . import ctbase
        return getattr(ctbase, name)
    raise AttributeError(f"module 'ctproc' has no attribute {name!r}")
