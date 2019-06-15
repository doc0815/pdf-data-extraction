import cx_Oracle, re

class Database():
    
    def __init__(self):
        # open data base connection
        self.__db = cx_Oracle.connect(<user>,<password>,'localhost:1521/xe')
        print('Connected to the Oracle ' + self.__db.version + ' database.')
        
        # declare an insert statement with binding variables
        self.__stmt_rdiv_insert =                      \
            "INSERT INTO raw_dividend"          + "\n" + \
            "( rdiv_filename"                   + "\n" + \
            ", rdiv_isin"                       + "\n" + \
            ", rdiv_is_isin_valid"              + "\n" + \
            ", rdiv_exdiv_date"                 + "\n" + \
            ", rdiv_valuta"                     + "\n" + \
            ", rdiv_unit"                       + "\n" + \
            ", rdiv_payout_gross"               + "\n" + \
            ", rdiv_payout_gross_ccy"           + "\n" + \
            ", rdiv_retention_gross"            + "\n" + \
            ", rdiv_retention_gross_ccy"        + "\n" + \
            ", rdiv_payout_net"                 + "\n" + \
            ", rdiv_payout_net_ccy"             + "\n" + \
            ", rdiv_payout_gross_unit"          + "\n" + \
            ", rdiv_payout_gross_unit_ccy"      + "\n" + \
            ", rdiv_retention_gross_unit"       + "\n" + \
            ", rdiv_retention_gross_unit_ccy"   + "\n" + \
            ", rdiv_tax_base"                   + "\n" + \
            ", rdiv_tax_base_ccy"               + "\n" + \
            ", rdiv_income_taxable"             + "\n" + \
            ", rdiv_income_taxable_ccy"         + "\n" + \
            ", rdiv_tax_withhold"               + "\n" + \
            ", rdiv_tax_withhold_ccy"           + "\n" + \
            ", rdiv_article_27"                 + "\n" + \
            ", rdiv_fx_rate )"                  + "\n" + \
            "VALUES"                            + "\n" + \
            "( :bFilename"                      + "\n" + \
            ", :bIsin"                          + "\n" + \
            ", :bIsinCheck"                     + "\n" + \
            ", :bExDivDate"                     + "\n" + \
            ", :bValuta"                        + "\n" + \
            ", :bUnit"                          + "\n" + \
            ", :bPayoutGross"                   + "\n" + \
            ", :bPayoutGrossCcy"                + "\n" + \
            ", :bRetentionGross"                + "\n" + \
            ", :bRetentionGrossCcy"             + "\n" + \
            ", :bPayoutNet"                     + "\n" + \
            ", :bPayoutNetCcy"                  + "\n" + \
            ", :bPayoutGrossUnit"               + "\n" + \
            ", :bPayoutGrossUnitCcy"            + "\n" + \
            ", :bRetentionGrossUnit"            + "\n" + \
            ", :bRetentionGrossUnitCcy"         + "\n" + \
            ", :bTaxbase"                       + "\n" + \
            ", :bTaxbaseCcy"                    + "\n" + \
            ", :bTaxableIncome"                 + "\n" + \
            ", :bTaxableIncomeCcy"              + "\n" + \
            ", :bWithholdTax"                   + "\n" + \
            ", :bWithholdTaxCcy"                + "\n" + \
            ", :bArt27"                         + "\n" + \
            ", :bFxRate )"
        
        # parse the statement by replacing line returns with a single
        # whitespace, replacing multiple whitespaces with single spaces
        self.__stmt_rdiv_insert = re.sub('\s+',' ',self.__stmt_rdiv_insert.replace('\n',' ').replace('\r',''))
    
    def write_to_database(self, listen, filename):
        
        try:
            cursor = self.__db.cursor()
            
            # execute statement
            cursor.execute(self.__stmt_rdiv_insert                                          \
                               , bFilename = filename                                       \
                               , bIsin = listen._sIsin                                      \
                               , bIsinCheck= listen._sIsinCheck                             \
                               , bExDivDate = listen._sExDivDate                            \
                               , bValuta = listen._sValuta                                  \
                               , bUnit = listen._sUnit                                      \
                               , bPayoutGross = listen._sPayoutGross                        \
                               , bPayoutGrossCcy = listen._sPayoutGrossCcy                  \
                               , bRetentionGross = listen._sRetentionGross                  \
                               , bRetentionGrossCcy = listen._sRetentionGrossCcy            \
                               , bPayoutNet = listen._sPayoutNet                            \
                               , bPayoutNetCcy = listen._sPayoutNetCcy                      \
                               , bPayoutGrossUnit = listen._sPayoutGrossUnit                \
                               , bPayoutGrossUnitCcy = listen._sPayoutGrossUnitCcy          \
                               , bRetentionGrossUnit = listen._sRetentionGrossUnit          \
                               , bRetentionGrossUnitCcy = listen._sRetentionGrossUnitCcy    \
                               , bTaxbase = listen._sTaxbase                                \
                               , bTaxbaseCcy = listen._sTaxbaseCcy                          \
                               , bTaxableIncome = listen._sTaxableIncome                    \
                               , bTaxableIncomeCcy = listen._sTaxableIncomeCcy              \
                               , bWithholdTax = listen._sWithholdTax                        \
                               , bWithholdTaxCcy = listen._sWithholdTaxCcy                  \
                               , bArt27 = listen._sArt27                                    \
                               , bFxRate = listen._sFxRate                                  \
            )
            
            # commit the inserted value.
            self.__db.commit()
        
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            print(error.code)
            print(error.message)
            print(error.context)
        
        finally:
            cursor.close()
    
    def close(self):
        # close data base connection
        self.__db.close()
