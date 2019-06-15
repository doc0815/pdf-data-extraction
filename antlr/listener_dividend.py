from PdfDividendListener import PdfDividendListener
from PdfDividendParser import PdfDividendParser

class ListenerDividend(PdfDividendListener):
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self._sIsin = ''
        self._sIsinCheck = 0
        self._sExDivDate = ''
        self._sValuta = ''
        self._sUnit = ''
        self._sPayoutGross = ''
        self._sPayoutGrossCcy = ''
        self._sRetentionGross = ''
        self._sRetentionGrossCcy = ''
        self._sPayoutNet = ''
        self._sPayoutNetCcy = ''
        self._sPayoutGrossUnit = ''
        self._sPayoutGrossUnitCcy = ''
        self._sRetentionGrossUnit = ''
        self._sRetentionGrossUnitCcy = ''
        self._sTaxbase = ''
        self._sTaxbaseCcy = ''
        self._sTaxableIncome = ''
        self._sTaxableIncomeCcy = ''
        self._sWithholdTax = ''
        self._sWithholdTaxCcy = ''
        self._sFxRate = ''
        self._sArt27 = 0
    
    def __check_isin(self, a):
        if len(a) != 12 or not all(c.isalpha() for c in a[:2]) or not all(c.isalnum() for c in a[2:]):
            return False
        s = "".join(str(int(c, 36)) for c in a)
        return 0 == (sum(sum(divmod(2 * (ord(c) - 48), 10)) for c in s[-2::-2]) + sum(ord(c) - 48 for c in s[::-2])) % 10
    
    def exitRules(self, ctx): # rules is top level grammer element
        
        for child in ctx.children:
            
            if isinstance(child, PdfDividendParser.ExtagContext):
                self._sExDivDate = child.TIMESTAMP().getText()
            
            elif isinstance(child, PdfDividendParser.ValutaContext):
                self._sValuta = child.TIMESTAMP().getText()
            
            elif isinstance(child, PdfDividendParser.UnitContext):
                if child.INTEGER() == None:
                    self._sUnit = int(float(child.DECIMAL().getText().replace(',','.')))
                else:
                    self._sUnit = child.INTEGER().getText().replace('.','')
            
            elif isinstance(child, PdfDividendParser.DividendContext):
                self._sPayoutGross = child.DECIMAL().getText()
                self._sPayoutGrossCcy = child.CURRENCY().getText()
            
            elif isinstance(child, PdfDividendParser.RetentionContext):
                self._sRetentionGross = child.DECIMAL().getText()
                self._sRetentionGrossCcy = child.CURRENCY().getText()
            
            elif isinstance(child, PdfDividendParser.Dividend_unitContext):
                self._sPayoutGrossUnit = child.DECIMAL().getText()
                self._sPayoutGrossUnitCcy = child.CURRENCY().getText()
            
            elif isinstance(child, PdfDividendParser.Retention_unitContext):
                self._sRetentionGrossUnit = child.DECIMAL().getText()
                self._sRetentionGrossUnitCcy = child.CURRENCY().getText()
            
            elif isinstance(child, PdfDividendParser.IsinContext):
                self._sIsin = child.ISIN().getText()
                self._sIsinCheck = int(self.__check_isin(self._sIsin))
            
            elif isinstance(child, PdfDividendParser.Tax_withholdContext):
                self._sWithholdTax = child.DECIMAL().getText()
                self._sWithholdTaxCcy = child.CURRENCY().getText()
            
            elif isinstance(child, PdfDividendParser.Income_taxableContext):
                self._sTaxableIncome = child.DECIMAL().getText()
                # currency is optional as it has quality issues
                if child.CURRENCY() == None:
                    self._sTaxableIncomeCcy = ''
                else:
                    self._sTaxableIncomeCcy = child.CURRENCY().getText()
            
            elif isinstance(child, PdfDividendParser.Payout_netContext):
                self._sPayoutNet = child.DECIMAL().getText()
                self._sPayoutNetCcy = child.CURRENCY().getText()
            
            elif isinstance(child, PdfDividendParser.Tax_baseContext):
                self._sTaxbase = child.DECIMAL().getText()
                self._sTaxbaseCcy = child.CURRENCY().getText()
            
            elif isinstance(child, PdfDividendParser.Fx_rateContext):
                self._sFxRate = child.DECIMAL().getText()
      
            elif isinstance(child, PdfDividendParser.Article_27Context):
                self._sArt27 = 1
