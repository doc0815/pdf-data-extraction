grammar PdfDividend;

// parser rules
rules
    : (
    any_expression 
    | extag
    | valuta
    | unit
    | dividend
    | retention
    | dividend_unit
    | retention_unit
    | isin
    | tax_withhold
    | income_taxable
    | payout_net
    | tax_base
    | fx_rate
    | article_27
    )+
    ;

extag
    : KEY_EXTAG TIMESTAMP
    ;

valuta
    : KEY_VALUTA TIMESTAMP
    ;

unit
    : KEY_UNIT (INTEGER|DECIMAL) // some units come with decimal separator
    ;

dividend
    : KEY_DIVIDEND_GROSS DECIMAL CURRENCY
    ;

retention
    : KEY_RETENTION_GROSS DECIMAL CURRENCY
    ;

dividend_unit
    : KEY_DIVIDEND_GROSS_UNIT DECIMAL CURRENCY
    ;

retention_unit
    : KEY_RETENTION_GROSS_UNIT DECIMAL CURRENCY
    ;

isin
    : ISIN
    ;

tax_withhold
    : KEY_TAX_WITHHOLD DECIMAL CURRENCY
    ;

income_taxable
    : KEY_INCOME_TAXABLE DECIMAL CURRENCY? // currency has quality problems, thus it is optional
    ;

payout_net
    : KEY_PAYOUT_NET DECIMAL CURRENCY
    ;

tax_base
    : KEY_TAX_BASE DECIMAL CURRENCY
    ;

fx_rate
    : KEY_FX_RATE DECIMAL
    ;

article_27
    : KEY_ARTICLE_27
    ;

any_expression // only non-skipped
    : (TIMESTAMP|INTEGER|FLOAT|DECIMAL|CURRENCY|COUNTRY)+
    ;

//////////////////////////////////////////////////////////////////////////////
// Keywords
//////////////////////////////////////////////////////////////////////////////

KEY_EXTAG
    : 'Extag' WHITESPACE? COLON
    ;

KEY_VALUTA
    : 'Valuta' WHITESPACE? COLON
    ;

KEY_UNIT
    : 'St.' WHITESPACE? COLON
    ;

KEY_DIVIDEND_GROSS
    : 'Bruttoausschüttung' WHITESPACE? COLON
    | 'Bruttodividende' WHITESPACE? COLON
    ;

KEY_RETENTION_GROSS
    : 'Bruttothesaurierung' WHITESPACE? COLON
    ;

KEY_DIVIDEND_GROSS_UNIT
    : 'Bruttoausschüttung' WHITESPACE? 'pro Stück' WHITESPACE? COLON
    | 'Bruttodividende' WHITESPACE? 'pro Stück' WHITESPACE? COLON
    ;

KEY_RETENTION_GROSS_UNIT
    : 'Bruttothesaurierung' WHITESPACE? 'pro Stück' WHITESPACE? COLON
    ;
   
KEY_TAX_WITHHOLD
    : STAR+ WHITESPACE? 'Einbeh. Steuer' WHITESPACE? COLON
    ;

KEY_INCOME_TAXABLE
    : 'steuerpflichtiger Ertrag' WHITESPACE? STAR* WHITESPACE? COLON
    ;

KEY_PAYOUT_NET
    : 'Endbetrag' WHITESPACE? COLON
    ;

KEY_TAX_BASE
    : 'Bemessungs' WHITESPACE? '-' WHITESPACE? 'grundlage' WHITESPACE? COLON
    ;

KEY_FX_RATE
    : 'Devisenkurs' WHITESPACE? COLON
    ;

KEY_ARTICLE_27
    : '§ 27neu KStG'
    ;

//////////////////////////////////////////////////////////////////////////////
// Whitespace and other things to skip
//////////////////////////////////////////////////////////////////////////////

WHITESPACE
    : WS+
    -> skip
    ;

ANY
    : (
      PARANTHESIS
    | COLON
    | COMMA
    | STOP
    | STAR
    | NOT_SPECIFIED
    )+
    -> skip
    ;

//////////////////////////////////////////////////////////////////////////////
// Timestamp
//////////////////////////////////////////////////////////////////////////////

TIMESTAMP
    : DATE ('T' TIME?)?
    | YEAR '-' MONTH 'T'
    | YEAR 'T'
    ;

fragment
DATE
    : YEAR '-' MONTH '-' DAY
    | DAY '.' MONTH '.' YEAR
    ;

fragment
YEAR
    : '000'             [1-9]
    | '00'        [1-9] DIGIT
    | '0'   [1-9] DIGIT DIGIT
    | [1-9] DIGIT DIGIT DIGIT
    ;

fragment
MONTH
    : '0' [1-9]
    | '1' [0-2]
    ;

fragment
DAY
    : '0'   [1-9]
    | [1-2] DIGIT
    | '3'   [0-1]
    ;

fragment
TIME
    : HOUR ':' MINUTE (':' SECOND)? OFFSET
    ;

fragment
OFFSET
    : 'Z'
    | PLUS_OR_MINUS HOUR ':' MINUTE
    ;

fragment
HOUR
    : [01] DIGIT
    | '2'  [0-3]
    ;

fragment
MINUTE
    : [0-5] DIGIT
    ;

// millesconds separated by '.'
fragment
SECOND
    : [0-5] DIGIT ('.' DIGIT+)?
    ;

//////////////////////////////////////////////////////////////////////////////
// Int
//////////////////////////////////////////////////////////////////////////////

INTEGER
    : '-'? UNSIGNED_INTEGER
    ;

//////////////////////////////////////////////////////////////////////////////
// Float
//////////////////////////////////////////////////////////////////////////////

FLOAT
    : INTEGER DEC_FRAC? FLOAT_EXP
    ;

fragment
FLOAT_EXP
    : [Ee] PLUS_OR_MINUS? DIGIT+
    ;

//////////////////////////////////////////////////////////////////////////////
// Decimal
//////////////////////////////////////////////////////////////////////////////

DECIMAL
    : INTEGER DEC_FRAC? DECIMAL_EXP?
    ;

fragment
DECIMAL_EXP
    : [Dd] PLUS_OR_MINUS? DIGIT+
    ;


//////////////////////////////////////////////////////////////////////////////
// Words
//////////////////////////////////////////////////////////////////////////////

ISIN
    : COUNTRY (ALPHA_C|DIGIT) (ALPHA_C|DIGIT) (ALPHA_C|DIGIT) (ALPHA_C|DIGIT) (ALPHA_C|DIGIT) (ALPHA_C|DIGIT) (ALPHA_C|DIGIT) (ALPHA_C|DIGIT) (ALPHA_C|DIGIT) DIGIT
    ;

COUNTRY
    : 'BE'|'BM'|'FR'|'BG'|'VE'|'DK'|'HR'|'DE'|'JP'|'HU'|'HK'|'JO'|'BR'|'XS'|'FI'|'GR'|'IS'|'RU'|'LB'
    | 'PT'|'NO'|'TW'|'UA'|'TR'|'LK'|'LV'|'LU'|'TH'|'NL'|'PK'|'PH'|'RO'|'EG'|'PL'|'AA'|'CH'|'CN'|'CL'
    | 'EE'|'CA'|'IR'|'IT'|'ZA'|'CZ'|'CY'|'AR'|'AU'|'AT'|'IN'|'CS'|'CR'|'IE'|'ID'|'ES'|'PE'|'TN'|'PA'
    | 'SG'|'IL'|'US'|'MX'|'SK'|'KR'|'SI'|'KW'|'MY'|'MO'|'SE'|'GB'|'GG'|'KY'|'JE'|'VG'|'NG'|'SA'|'MU'
    ;

// CURRENCY is a set of special words and must be placed before WORD
// matching might be successfull for both CURRENCY and WORD
CURRENCY
    : 'EUR'
    | 'USD'
    | 'CHF'
    | 'GBP'
    | 'JPY'
    ;

WORD
    : ALPHA_ALL+ (ALPHA_ALL|DIGIT)*
    -> skip
    ;

//////////////////////////////////////////////////////////////////////////////
// Common Lexer Primitives
//////////////////////////////////////////////////////////////////////////////

fragment
COLON
    : ':'
    ;

fragment
COMMA
    : ','
    ;

fragment
STOP
    : '.'
    ;

fragment
STAR
    : '*'
    ;

fragment
PARANTHESIS
    : '['
    | '('
    | '{'
    | '<'
    | ']'
    | ')'
    | '}'
    | '>'
    ;

fragment
NOT_SPECIFIED
    : '/'
    | '_'
    | '-'
    | '+'
    | '='
    | '\u0040' // @
    | '\uFB02' // ﬂ
    | '\u00A7' // §
    | '\u0025' // %
    ;

fragment
ALPHA_ALL
    : ALPHA_C
    | ALPHA_S
    | GER_SPECIAL
    ;

fragment
UNSIGNED_INTEGER
    : DIGIT+ ('.' DIGIT DIGIT DIGIT)*
    ;

fragment
DEC_FRAC
    : ','
    | ',' DIGIT+
    ;

fragment
ALPHA_C
    : [A-Z]
    ;

fragment
ALPHA_S
    : [a-z]
    ;

fragment
GER_SPECIAL
    : '\u00C4' // Ä
    | '\u00D6' // Ö
    | '\u00DC' // Ü
    | '\u00E4' // ä
    | '\u00F6' // ö
    | '\u00FC' // ü
    ;

fragment
DIGIT
    : [0-9]
    ;

fragment
PLUS_OR_MINUS
    : [+\-]
    ;

fragment
WS
    : WS_NOT_NL
    | '\u000A' // line feed
    | '\u000D' // carriage return
    ;

fragment
NL
    : '\u000D\u000A'  // carriage return + line feed
    | '\u000D'        // carriage return
    | '\u000A'        // line feed
    ;

fragment
WS_NOT_NL
    : '\u0009' // tab
    | '\u000B' // vertical tab
    | '\u000C' // form feed
    | '\u0020' // space
    ;
