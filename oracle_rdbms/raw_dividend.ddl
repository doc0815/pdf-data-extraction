/* sequences */
--    drop sequence pms.seq_rdiv_id;
create sequence pms.seq_rdiv_id
minvalue 10000000 maxvalue 99999999
increment by 1 start with 10000000
nocache noorder nocycle;

/
/* tables and comments */
--    drop table pms.raw_dividend;
create table pms.raw_dividend(
    rdiv_id                           number(8)       not null
  , rdiv_filename                     varchar2(200)   not null
  , rdiv_tech_date                    timestamp(3)    not null
  , rdiv_isin                         char(12)
  , rdiv_is_isin_valid                number(1,0)
  , rdiv_exdiv_date                   date
  , rdiv_valuta                       date
  , rdiv_unit                         number(6,0)
  , rdiv_payout_gross                 number(12,2)
  , rdiv_payout_gross_ccy             char(3)
  , rdiv_retention_gross              number(12,2)
  , rdiv_retention_gross_ccy          char(3)
  , rdiv_payout_net                   number(12,2)
  , rdiv_payout_net_ccy               char(3)
  , rdiv_payout_gross_unit            number(12,6)
  , rdiv_payout_gross_unit_ccy        char(3)
  , rdiv_retention_gross_unit         number(12,6)
  , rdiv_retention_gross_unit_ccy     char(3)
  , rdiv_tax_base                     number(12,2)
  , rdiv_tax_base_ccy                 char(3)
  , rdiv_income_taxable               number(12,2)
  , rdiv_income_taxable_ccy           char(3)
  , rdiv_tax_withhold                 number(12,2)
  , rdiv_tax_withhold_ccy             char(3)
  , rdiv_article_27                   number(1,0)
  , rdiv_fx_rate                      number(12,6)
);


/
/* constraints */
alter table pms.raw_dividend add constraint pk_rdiv primary key (rdiv_id);


/
/* triggers */
create or replace trigger pms.trg_rdiv_id
before insert or update on pms.raw_dividend
for each row
begin
  
  if inserting then
    :new.rdiv_id        := pms.seq_rdiv_id.nextval;
    :new.rdiv_tech_date := systimestamp;
    
  elsif updating then
    null;
  
  elsif deleting then
    null;
  
  else
    null;
  
  end if;
  
end;

/
select * from pms.raw_dividend;
