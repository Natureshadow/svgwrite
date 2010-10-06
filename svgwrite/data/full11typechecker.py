import re
import pattern

def iterflatlist(values):
    """ Flatten nested *values*, returns an *iterator*. """
    for element in values:
        if hasattr(element, "__iter__") and not isinstance(element, basestring):
            for item in iterflatlist(element):
                yield item
        else:
            yield element

INVALID_NAME_CHARS = frozenset([' ', '\t', '\r', '\n', ',', '(', ')'])
WHITESPACE = frozenset([' ', '\t', '\r', '\n'])
SHAPE_PATTERN = re.compile("rect\((.*),(.*),(.*),(.*)\)")
FUNCIRI_PATTERN = re.compile("url\((.*)\)")

class Full11TypeChecker(object):
    def get_version(self):
        return ('1.1', 'full')

    def is_angle(self, value):
        #angle ::= number (~"deg" | ~"grad" | ~"rad")?
        if self.is_number(value):
            return True
        elif isinstance(value, basestring):
            return pattern.angle.match(value.strip()) is not None
        return False

    def is_anything(self, value):
        #anything ::= Char*
        return True
    is_string = is_anything

    def is_color(self, value):
        #color    ::= "#" hexdigit hexdigit hexdigit (hexdigit hexdigit hexdigit)?
        #             | "rgb(" wsp* integer comma integer comma integer wsp* ")"
        #             | "rgb(" wsp* integer "%" comma integer "%" comma integer "%" wsp* ")"
        #             | color-keyword
        #hexdigit ::= [0-9A-Fa-f]
        #comma    ::= wsp* "," wsp*
        return True

    def is_frequency(self, value):
        #frequency ::= number (~"Hz" | ~"kHz")
        if self.is_number(value):
            return True
        elif isinstance(value, basestring):
            return pattern.frequency.match(value.strip()) is not None
        return False

    def is_FuncIRI(self, value):
        #FuncIRI ::= "url(" <IRI> ")"
        res = FUNCIRI_PATTERN.match(value.strip())
        if res:
            return self.is_IRI(res.group(1))
        return False

    def is_icccolor(self, value):
        #icccolor ::= "icc-color(" name (comma-wsp number)+ ")"
        return True

    def is_integer(self, value):
        try:
            number = int(value)
            return True
        except:
            return False

    is_IRI = is_anything
        #Internationalized Resource Identifiers
        #a more generalized complement to Uniform Resource Identifiers (URIs)

    def is_length(self, value):
        #length ::= number ("em" | "ex" | "px" | "in" | "cm" | "mm" | "pt" | "pc" | "%")?
        if value is None:
            return False
        if isinstance(value, (int, float)):
            return self.is_number(value)
        elif isinstance(value, basestring):
            result = pattern.length.match(value.strip())
            if result:
                number, tmp, unit = result.groups()
                return self.is_number(number) # for tiny check!
        return False

    is_coordinate = is_length

    def is_list_of_T(self, value, t='string'):
        def split(value):
            #TODO: improve split function!!!!
            if isinstance(value, (int, float)):
                return (value, )
            if isinstance(value, basestring):
                return iterflatlist(v.split(',') for v in value.split(' '))
            return value
        #list-of-Ts ::= T
        #               | T comma-wsp list-of-Ts
        #comma-wsp  ::= (wsp+ ","? wsp*) | ("," wsp*)
        #wsp        ::= (#x20 | #x9 | #xD | #xA)
        checker = self.get_func_by_name(t)
        for v in split(value):
            if not checker(v):
                return False
        return True

    def is_semicolon_list(self, value):
        #a semicolon-separated list of values
        #               | value comma-wsp list-of-values
        #comma-wsp  ::= (wsp+ ";" wsp*) | ("," wsp*)
        #wsp        ::= (#x20 | #x9 | #xD | #xA)
        return True

    def is_name(self, value):
        #name  ::= [^,()#x20#x9#xD#xA] /* any char except ",", "(", ")" or wsp */
        if INVALID_NAME_CHARS.intersection(frozenset(str(value))):
            return False
        else:
            return True

    def is_number(self, value):
        try:
            number = float(value)
            return True
        except:
            return False

    def is_number_optional_number(self, value):
        #number-optional-number ::= number
        #                           | number comma-wsp number
        if isinstance(value, basestring):
            values = re.split(' *,? *', value.strip())
            if 0 < len(values) < 3: # 1 or 2 numbers
                for v in values:
                    if not self.is_number(v):
                        return False
                return True
        else:
            try: # is it a 2-tuple
                n1, n2 = value
                if self.is_number(n1) and \
                   self.is_number(n2):
                    return True
            except TypeError: # just one value
                return self.is_number(value)
            except ValueError: # more than 2 values
                pass
        return False

    def is_paint(self, value):
        #paint ::=	"none" |
        #           "currentColor" |
        #           <color> [<icccolor>] |
        #           <funciri> [ "none" | "currentColor" | <color> [<icccolor>] |
        #           "inherit"
        return True

    def is_percentage(self, value):
        #percentage ::= number "%"
        if self.is_number(value):
            return True
        elif isinstance(value, basestring):
            return pattern.percentage.match(value.strip()) is not None
        return False

    def is_time(self, value):
        #time ::= <number> (~"ms" | ~"s")?
        if self.is_number(value):
            return True
        elif isinstance(value, basestring):
            return pattern.time.match(value.strip()) is not None
        return False

    def is_transform_list(self, value):
        return True

    def is_XML_Name(self, value):
        return True

    def is_shape(self, value):
        #shape ::= (<top> <right> <bottom> <left>)
        # where <top>, <bottom> <right>, and <left> specify offsets from the
        # respective sides of the box.
        # <top>, <right>, <bottom>, and <left> are <length> values
        # i.e. 'rect(5px, 10px, 10px, 5px)'
        res = SHAPE_PATTERN.match(value.strip())
        if res:
            for arg in res.groups():
                if not self.is_length(arg):
                    return False
        else:
            return False
        return True

    def get_func_by_name(self, funcname):
        return getattr(self,
                       'is_'+funcname.replace('-', '_'),
                       self.is_anything)

    def check(self, typename, value):
        if typename.startswith('list-of-'):
            t = typename[8:]
            return self.is_list_of_T(value, t)
        return self.get_func_by_name(typename)(value)