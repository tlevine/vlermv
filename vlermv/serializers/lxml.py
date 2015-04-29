class _meta_xml:
    def __init__(self, lxml_module):
        self.module = lxml_module

    @staticmethod
    def dump(obj, fp):
        fp.write(self.module.tostring(obj))

    @staticmethod
    def load(fp):
        return self.module.fromstring(fp.read())

    vlermv_cache_exceptions = False
    vlermv_binary_mode = False

try:
    import lxml
except ImportError:
    pass
else:
    import lxml.html, lxml.etree
    html = _meta_xml(lxml.html)
    xml = _meta_xml(lxml.etree)
