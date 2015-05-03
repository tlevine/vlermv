class _meta_xml:
    @staticmethod
    def dump(obj, fp):
        fp.write(self.module.tostring(obj))

    @staticmethod
    def load(fp):
        return self.module.fromstring(fp.read())

    cache_exceptions = False
    binary_mode = False

try:
    import lxml
except ImportError:
    pass
else:
    import lxml.html, lxml.etree
    class html(_meta_xml):
        module = lxml.html
    class xml(_meta_xml):
        module = lxml.etree
