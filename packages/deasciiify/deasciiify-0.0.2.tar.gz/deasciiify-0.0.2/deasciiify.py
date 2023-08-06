# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re


class _LinearCongruentialGenerator(object):

    _modulus = 4294967296
    _multiplier = 1664525
    _increment = 1013904223

    def __init__(self, seed):
        self._value = seed % self._modulus

    def get(self):
        self._value = (((self._multiplier * self._value) + self._increment) %
                       self._modulus)
        return self._value


_letter_map = {
    'a': ['à', 'á', 'â', 'ã', 'ä', 'å', 'ā', 'ă', 'ą', 'ǎ', 'ǟ', 'ǡ', 'ǻ', 'ȁ',
          'ȃ', 'ȧ', 'ӑ', 'ӓ', 'ᶏ', 'ḁ', 'ẚ', 'ạ', 'ả', 'ấ', 'ầ', 'ẩ', 'ẫ', 'ậ',
          'ắ', 'ằ', 'ẳ', 'ẵ', 'ặ', 'ɐ', 'α', 'ά', 'ἀ', 'ἁ', 'ἂ', 'ἃ', 'ἄ',
          'ἅ', 'ἆ', 'ἇ', 'ὰ', 'ά'],
    'b': ['ƀ', 'ƃ', 'ɓ', 'ᵬ', 'ᶀ', 'ḃ', 'ḅ', 'ḇ'],
    'c': ['ç', 'ć', 'ĉ', 'ċ', 'č', 'ƈ', 'ȼ', 'ɕ', 'ḉ', '¢'],
    'd': ['ď', 'đ', 'ƌ', 'ȡ', 'ɖ', 'ɗ', 'ᵭ', 'ᶁ', 'ᶑ', 'ḋ', 'ḍ', 'ḏ', 'ḑ',
          'ḓ'],
    'e': ['è', 'é', 'ê', 'ë', 'ē', 'ĕ', 'ė', 'ę', 'ě', 'ȅ', 'ȇ', 'ȩ', 'ᶒ', 'ḕ',
          'ḗ', 'ḙ', 'ḛ', 'ḝ', 'ẹ', 'ẻ', 'ẽ', 'ế', 'ề', 'ể', 'ễ', 'ệ', 'ǝ'],
    'f': ['ƒ', 'ᵮ', 'ᶂ', 'ḟ', 'ƒ'],
    'g': ['ĝ', 'ğ', 'ġ', 'ģ', 'ǥ', 'ǧ', 'ǵ', 'ɠ', 'ᶃ', 'ḡ', 'ᵷ'],
    'h': ['ĥ', 'ħ', 'ȟ', 'ɦ', 'ḣ', 'ḥ', 'ḧ', 'ḩ', 'ḫ', 'ẖ'],
    'i': ['ì', 'í', 'î', 'ï', 'ĩ', 'ī', 'ĭ', 'į', 'ǐ', 'ȉ', 'ȋ', 'ɨ', 'ᶖ', 'ḭ',
          'ḯ', 'ỉ', 'ị'],
    'j': ['ĵ', 'ǰ', 'ʝ'],
    'k': ['ķ', 'ƙ', 'ǩ', 'ᶄ', 'ḱ', 'ḳ', 'ḵ', 'ʞ'],
    'l': ['ĺ', 'ļ', 'ľ', 'ŀ', 'ł', 'ƚ', 'ȴ', 'ɫ', 'ɬ', 'ɭ', 'ᶅ', 'ḷ', 'ḹ', 'ḻ',
          'ḽ', 'ℓ'],
    'm': ['ɱ', 'ᵯ', 'ᶆ', 'ḿ', 'ṁ', 'ṃ'],
    'n': ['ñ', 'ń', 'ņ', 'ň', 'ƞ', 'ǹ', 'ȵ', 'ɲ', 'ɳ', 'ᵰ', 'ᶇ', 'ṅ', 'ṇ', 'ṉ',
          'ṋ', 'η', 'ή', 'ἠ', 'ἡ', 'ἢ', 'ἣ', 'ἤ', 'ἥ', 'ἦ', 'ἧ', 'ὴ', 'ή'],
    'o': ['ò', 'ó', 'ô', 'õ', 'ö', 'ø', 'ō', 'ŏ', 'ő', 'ơ', 'ǒ', 'ǫ', 'ǭ', 'ǿ',
          'ȍ', 'ȏ', 'ȫ', 'ȭ', 'ȯ', 'ȱ', 'ӧ', 'ṍ', 'ṏ', 'ṑ', 'ṓ', 'ọ', 'ỏ', 'ố',
          'ồ', 'ổ', 'ỗ', 'ộ', 'ớ', 'ờ', 'ở', 'ỡ', 'ợ'],
    'p': ['ƥ', 'ᵱ', 'ᵽ', 'ᶈ', 'ṕ', 'ṗ'],
    'q': ['ʠ'],
    'r': ['ŕ', 'ŗ', 'ř', 'ȑ', 'ȓ', 'ɼ', 'ɽ', 'ɾ', 'ᵲ', 'ᵳ', 'ᶉ', 'ṙ', 'ṛ', 'ṝ',
          'ṟ'],
    's': ['ś', 'ŝ', 'ş', 'š', 'ș', 'ȿ', 'ʂ', 'ᵴ', 'ᶊ', 'ṡ', 'ṣ', 'ṥ', 'ṧ',
          'ṩ'],
    't': ['ţ', 'ť', 'ŧ', 'ƫ', 'ƭ', 'ț', 'ȶ', 'ʈ', 'ᵵ', 'ṫ', 'ṭ', 'ṯ', 'ṱ',
          'ẗ', '✝'],
    'u': ['ù', 'ú', 'û', 'ü', 'ũ', 'ū', 'ŭ', 'ů', 'ű', 'ų', 'ư', 'ǔ', 'ǖ', 'ǘ',
          'ǚ', 'ǜ', 'ȕ', 'ȗ', 'ᶙ', 'ṳ', 'ṵ', 'ṷ', 'ṹ', 'ṻ', 'ụ', 'ủ', 'ứ', 'ừ',
          'ử', 'ữ', 'ự', 'μ'],
    'v': ['ʋ', 'ᶌ', 'ṽ', 'ṿ'],
    'w': ['ŵ', 'ẁ', 'ẃ', 'ẅ', 'ẇ', 'ẉ', 'ẘ', 'ω', 'ώ', 'ὠ', 'ὡ', 'ὢ', 'ὣ',
          'ὤ', 'ὥ', 'ὦ', 'ὧ', 'ὼ', 'ώ'],
    'x': ['ᶍ', 'ẋ', 'ẍ', '×'],
    'y': ['ý', 'ÿ', 'ŷ', 'ƴ', 'ȳ', 'ẏ', 'ẙ', 'ỳ', 'ỵ', 'ỷ', 'ỹ', 'Ӯ', 'Ӱ',
          'Ӳ', 'γ'],
    'z': ['ź', 'ż', 'ž', 'ƶ', 'ȥ', 'ɀ', 'ʐ', 'ʑ', 'ᵶ', 'ᶎ', 'ẑ', 'ẓ', 'ẕ'],
    'A': ['À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Ā', 'Ă', 'Ą', 'Ǎ', 'Ǟ', 'Ǡ', 'Ǻ', 'Ȁ',
          'Ȃ', 'Ȧ', 'Ⱥ', 'Ӑ', 'Ӓ', 'Ḁ', 'Ạ', 'Ả', 'Ấ', 'Ầ', 'Ẩ', 'Ẫ', 'Ậ', 'Ắ',
          'Ằ', 'Ẳ', 'Ẵ', 'Ặ', 'Λ', '𝔸'],
    'B': ['Ɓ', 'Ḃ', 'Ḅ', 'Ḇ', 'β', 'ß', '𝔹'],
    'C': ['Ç', 'Ć', 'Ĉ', 'Ċ', 'Č', 'Ƈ', 'Ȼ', 'Ḉ', 'ℭ', 'ℂ'],
    'D': ['Ď', 'Đ', 'Ɗ', 'Ƌ', 'Ḋ', 'Ḍ', 'Ḏ', 'Ḑ', 'Ḓ', '𝔻'],
    'E': ['È', 'É', 'Ê', 'Ë', 'Ē', 'Ĕ', 'Ė', 'Ę', 'Ě', 'Ȅ', 'Ȇ', 'Ȩ', 'Ḕ', 'Ḗ',
          'Ḙ', 'Ḛ', 'Ḝ', 'Ẹ', 'Ẻ', 'Ẽ', 'Ế', 'Ề', 'Ể', 'Ễ', 'Ệ', '€', '𝔼'],
    'F': ['Ƒ', 'Ḟ', 'Ⅎ', '𝔽'],
    'G': ['Ĝ', 'Ğ', 'Ġ', 'Ģ', 'Ɠ', 'Ǥ', 'Ǧ', 'Ǵ', 'Ḡ', '⅁', '𝔾'],
    'H': ['Ĥ', 'Ħ', 'Ȟ', 'Ḣ', 'Ḥ', 'Ḧ', 'Ḩ', 'Ḫ', 'ℌ', 'ℍ'],
    'I': ['Ì', 'Í', 'Î', 'Ï', 'Ĩ', 'Ī', 'Ĭ', 'Į', 'İ', 'Ɨ', 'Ǐ', 'Ȉ', 'Ȋ', 'ᵻ',
          'Ḭ', 'Ḯ', 'Ỉ', 'Ị'],
    'J': ['Ĵ', '𝕁'],
    'K': ['Ķ', 'Ƙ', 'Ǩ', 'Ḱ', 'Ḳ', 'Ḵ', '𝕂'],
    'L': ['Ĺ', 'Ļ', 'Ľ', 'Ŀ', 'Ł', 'Ƚ', 'Ḷ', 'Ḹ', 'Ḻ', 'Ḽ', '𝕃'],
    'M': ['Ḿ', 'Ṁ', 'Ṃ', '𝕄'],
    'N': ['Ñ', 'Ń', 'Ņ', 'Ň', 'Ɲ', 'Ǹ', 'Ƞ', 'Ṅ', 'Ṇ', 'Ṉ', 'Ṋ', 'Ѝ', 'Ӣ', 'Ӥ',
          'И', 'Й', 'ℕ'],
    'O': ['Ò', 'Ó', 'Ô', 'Õ', 'Ö', 'Ø', 'Ō', 'Ŏ', 'Ő', 'Ɵ', 'Ơ', 'Ǒ', 'Ǫ', 'Ǭ',
          'Ǿ', 'Ȍ', 'Ȏ', 'Ȫ', 'Ȭ', 'Ȯ', 'Ȱ', 'Ӧ', 'Ṍ', 'Ṏ', 'Ṑ', 'Ṓ', 'Ọ', 'Ỏ',
          'Ố', 'Ồ', 'Ổ', 'Ỗ', 'Ộ', 'Ớ', 'Ờ', 'Ở', 'Ỡ', 'Ợ', 'Θ', '𝕆', '⃠'],
    'P': ['Ƥ', 'Ṕ', 'Ṗ', 'ℙ'],
    'Q': ['℺', 'ℚ'],
    'R': ['Ŕ', 'Ŗ', 'Ř', 'Ȑ', 'Ȓ', 'Ṙ', 'Ṛ', 'Ṝ', 'Ṟ', 'ᴚ', 'ℜ', 'ℝ', '℟'],
    'S': ['Ś', 'Ŝ', 'Ş', 'Š', 'Ș', 'Ṡ', 'Ṣ', 'Ṥ', 'Ṧ', 'Ṩ', '𝕊'],
    'T': ['Ţ', 'Ť', 'Ŧ', 'Ƭ', 'Ʈ', 'Ț', 'Ⱦ', 'Ṫ', 'Ṭ', 'Ṯ', 'Ṱ', '𝕋'],
    'U': ['Ù', 'Ú', 'Û', 'Ü', 'Ũ', 'Ū', 'Ŭ', 'Ů', 'Ű', 'Ų', 'Ư', 'Ǔ', 'Ǖ', 'Ǘ',
          'Ǚ', 'Ǜ', 'Ȕ', 'Ȗ', 'ᵾ', 'Ṳ', 'Ṵ', 'Ṷ', 'Ṹ', 'Ṻ', 'Ụ', 'Ủ', 'Ứ', 'Ừ',
          'Ử', 'Ữ', 'Ự', '𝕌'],
    'V': ['Ʋ', 'Ṽ', 'Ṿ', '𝕍', '℣'],
    'W': ['Ŵ', 'Ẁ', 'Ẃ', 'Ẅ', 'Ẇ', 'Ẉ', '𝕎'],
    'X': ['Ẋ', 'Ẍ', '𝕏'],
    'Y': ['Ý', 'Ŷ', 'Ÿ', 'Ƴ', 'Ȳ', 'Ẏ', 'Ỳ', 'Ỵ', 'Ỷ', 'Ỹ', 'Ψ', '𝕐'],
    'Z': ['Ź', 'Ż', 'Ž', 'Ƶ', 'Ȥ', 'Ẑ', 'Ẓ', 'Ẕ', 'ℤ'],
}


def _translate(text):
    random = _LinearCongruentialGenerator(sum([ord(l) for l in text]))

    result = ''
    for letter in text:
        if letter in _letter_map:
            i = random.get() % len(_letter_map[letter])
            result += _letter_map[letter][i]
        else:
            result += letter

    return result


_consonents = r'[BCDFGHJKLMNPQRSTVWXYZbcdfghjklmnpqrstvwxyz]'
_vowels = r'[AEIOUaeiou]'

_elongation_patterns = [
    re.compile(_consonents + r'(a+)' + _consonents),
    re.compile(r'(bb+)'),
    re.compile(r'c(h+)'),
    re.compile(r'(dd+)'),
    re.compile(r'(ee+)'),
    re.compile(r'(f+)'),
    re.compile(r'(gg+)'),
    re.compile(_consonents + r'(i+)' + _consonents),
    re.compile(r'(k+)'),
    re.compile(r'(ll+)'),
    re.compile(r'(m+)'),
    re.compile(_vowels + r'(n+)[dg\b]'),
    re.compile(r'(oo+)'),
    re.compile(r'(pp+)'),
    re.compile(r'(r+)'),
    re.compile(r'(s+)'),
    re.compile(r's(h+)'),
    re.compile(r'(tt+)'),
    re.compile(_consonents + r'(u+)' + _consonents),
    re.compile(r'(x+)'),
    re.compile(r'(y+)\b'),
    re.compile(r'(z+)'),
]


def _elongate(text, n):
    if n <= 0:
        return text

    orig_len = len(text)
    if 0 < n < 1:
        n = int(round(orig_len * n))

    random = _LinearCongruentialGenerator(sum([ord(l) for l in text]))

    num_patterns = len(_elongation_patterns)

    for _ in xrange(n * num_patterns):
        pattern = _elongation_patterns[random.get() % num_patterns]
        matches = list(pattern.finditer(text))
        if not matches:
            continue

        match = matches[random.get() % len(matches)]
        replacement = match.group(1) + match.group(1)[-1]
        text = text[:match.start(1)] + replacement + text[match.end(1):]

        if len(text) - orig_len >= n:
            break

    return text


_fragment_placeholder = u'\xff\x2a\x7e\x00'
_fragment_pattern = re.compile(r"""
(
    # HTML tags
    <[^>]*>
    # HTML entities
    | &[^\s;]+;
    # % format
    | %(?:\([^\)]+\))?s
    # escaped { for format string
    | \{\{
    # escaped } for format string
    | \}\}
    # {} format specifier
    | \{(?:[^\{\}]|\{[^\{\}]*\})*\}
)
""", re.VERBOSE)


def _extract_fragments(text):
    matches = list(_fragment_pattern.finditer(text))
    if not matches:
        return text, []

    fragments = []
    result = ''
    pos = 0
    for match in matches:
        fragments.append(text[match.start(1):match.end(1)])
        result += text[pos:match.start(1)] + _fragment_placeholder
        pos = match.end(1)

    result += text[pos:]

    return result, fragments


def _restore_fragments(text, fragments):
    pl = len(_fragment_placeholder)

    for fragment in fragments:
        i = text.index(_fragment_placeholder)
        text = text[:i] + fragment + text[i + pl:]

    return text


def deasciiify(text, elongate=0):
    """Translate ASCII text into readable non-ASCII text

    >>> # basic usage
    >>> print(deasciiify('The quick brown fox jumps over the lazy dog.'))
    Ṱḥẹ ʠǚîĉʞ ɓṙōẇṇ ᶂø× ǰúṁᶈș óʋᶒṝ ᵵĥĕ ȴạᵶý ḍọḡ.

    >>> # elongate by 50%
    >>> print(deasciiify('The quick brown fox jumps over the lazy dog.',
    ...                  elongate=0.5))
    𝕋ȟẹ ʠůḭċḱ ᵬṙồẁñ ḟḟᶂᵮợẋᶍ ǰưḿṁᵱṣᵴṣ ǫṽếṛᵳ ṭħȇ ɫäǎąẩžɀẓẑẕᶎᶎẓẓỹÿŷӮ ḋöᵷ.

    >>> # elongate by 100 characters
    >>> print(deasciiify('The quick brown fox jumps over the lazy dog.',
    ...                  elongate=100))
    ... # doctest: +NORMALIZE_WHITESPACE
    Ʈɦẻ ʠűȋḉƙḱᶄḵḳķʞǩƙḱᶄḵḳ ƀᶉŏẁἦ ƒḟḟᶂḟƒởᶍ×ẍẋᶍ ĵứȗửǔǚṷȕǜûủũṳṹữụṻưṃɱḿṁḿɱḿṁᶈşᵴșŝș
    ȫṽḙɽᵳɾŕŕŗȓṙɼᵳȑᵳɽȓȑᶉᵳᶉ ƭẖė ℓἂậẳẩầạẳἇầǡᶏạᶏƶžźƶȥᶎẑᵶżȥᶎẑᶎγƴẏӲӰýỳŷẏγẏỳ ᶑốǥ.

    >>> # preserve HTML, entities, and gettext params
    >>> print(deasciiify(
    ...     'The <em>quick</em> <strong style="color:brown;">brown</strong> '
    ...     'fox %(verb)s over the &ldquo;lazy&rdquo; %s.'))
    ... # doctest: +NORMALIZE_WHITESPACE
    Ṯȟè <em>ʠúᶖćḵ</em> <strong style="color:brown;">ḃᵲóẅἢ</strong> ḟọẍ %(verb)s
    ȏʋềŕ ṱȟḝ &ldquo;ḽӓżӮ&rdquo; %s.

    >>> # preserve Python brace format params
    >>> print(deasciiify(
    ...     'The {} brown fox {verb} over the lazy dog. '
    ...     'Escaped braces: {{escaped}}'))
    Ŧḩẻ {} ḇᶉớωň ḟöᶍ {verb} ṓṽēȑ ŧĥể ĺåʐý ďòğ. Ḕʂċἂṗḕɗ ḅřἄćēṥ: {{ẻȿçẩṕḛƌ}}

    """
    text, fragments = _extract_fragments(text)
    text = _translate(_elongate(text, elongate))
    text = _restore_fragments(text, fragments)
    return text


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.NORMALIZE_WHITESPACE)
