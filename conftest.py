import psycopg2
import pytest
from INC_date import *


def pytest_addoption(parser):
    parser.addoption(
        "--contur",
        action="store",
        default="rnd_uat",
        help="Chose testing contur example --skim, by default rnd_uat"
    )


@pytest.fixture(scope="module")
def connection(request):
    if request.config.getoption('--contur') == 'rnd_uat':
        con = psycopg2.connect(
                    database="rnd_uat",
                    user="skim_qa2_etl_srv",
                    password="skim_qa2_etl_srv123",
                    host="10.248.96.23",
                    port="5432"
                )
        cur = con.cursor()
        cur.execute('set enable_nestloop to off;')
        cur.execute('set enable_mergejoin to off;')

        yield cur

        cur.close()
        con.close()
    elif request.config.getoption('--contur') == 'dev':
        con = psycopg2.connect(
            database="dev",
            user="skim_qa_etl_srv",
            password="skim_qa_etl_srv123",
            host="10.248.96.23",
            port="5432"
        )
        cur = con.cursor()
        cur.execute('set enable_nestloop to off;')
        cur.execute('set enable_mergejoin to off;')

        yield cur

        cur.close()
        con.close()
    elif request.config.getoption('--contur') == 'skim':
        con = psycopg2.connect(
            database="skim",
            user="skim_qa2_etl_srv",
            password="skim_qa2_etl_srv123",
            host="10.248.96.23",
            port="5432"
        )
        cur = con.cursor()
        cur.execute('set enable_nestloop to off;')
        cur.execute('set enable_mergejoin to off;')

        yield cur

        cur.close()
        con.close()


# -- hcode '00065' --> '00103'

# -- Сравнение кол-ва записей
@pytest.fixture
def hcode_id_65_103_eq_1():
    return """create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in (%s)and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in (%s) and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
	;
end;
$f$
;"""


@pytest.fixture
def hcode_id_65_103_eq_2():
    return """select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = %s
and calc_rule = 'ratio'
--and dt in ()
union all
select * from public.lilo_auto_qa();"""



# -- Полная сверка

@pytest.fixture
def hcode_id_65_103_emp_1():
    return """create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in (%s) and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in (%s) and a.calc_rule not in ('influence', 'deviation');
	return query
select 
	%s::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (a.org_id, b.org_id)::int8 as org_id,  
	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,  
	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id, 
	coalesce (a.metric_type_id, b.metric_type_id)::int8 as metric_type_id, 
	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id, 
  	22::int8 as unit_id, 
 	coalesce (a.dt, b.dt)::date as dt, 
  	((a.value/nullif(b.value,0))::numeric(20,6))::float8 as value, 
	coalesce (a.duch_id, b.duch_id)::int8 as duch_id, 
	coalesce (a.nod_id, b.nod_id)::int8 as nod_id, 
	coalesce (a.dir_id, b.dir_id)::int8 as dir_id, 
	coalesce (a.kato_id, b.kato_id)::int8 as kato_id, 
	coalesce (a.vids_id, b.vids_id)::int8 as vids_id
from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
cross join (select * from dm.d_hcode_t where id = %s) hcd
    ;
end;
$f$
;"""

@pytest.fixture
def hcode_id_65_103_emp_2():
    return """select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id from dm_rep.dm_all_indicators_v
where hcode_id = %s
and calc_rule = 'ratio'"""
# -- Ожидаемый результат: Запрос должен возвращать пустой вывод.


# -- hcode '00004'

# -- Сравнение кол-ва записей
#
# @pytest.fixture
# def hcode_id_00004_eq_1():
#     return """create or replace function public.lilo_auto_qa() returns table(cnt int8)
# language plpgsql
# as $f$
# begin
# 	drop table if exists public.la_qa1;
# 	drop table if exists public.la_qa2;
# 	create table public.la_qa1 as
# 		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00327') and unit_id = 45 and calc_rule not in ('influence', 'deviation');
# 	create table public.la_qa2 as
# 		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00131') and unit_id in (17,89) and calc_rule not in ('influence', 'deviation');
# 	return query
# select count(0) from public.la_qa1 a
# 	left join public.la_qa2 b
# 		on  a.org_id = b.org_id
# 		and a.date_type_id = b.date_type_id
# 		and a.cargo_type_id = b.cargo_type_id
# 		and a.val_type_id = b.val_type_id
# 		and a.metric_type_id = b.metric_type_id
# 		and a.dt = b.dt
# 		and a.nod_id = b.nod_id
# 		and a.duch_id = b.duch_id
# 		and a.vids_id = b.vids_id
# 		and a.kato_id = b.kato_id
# 		and a.dir_id = b.dir_id
# 	;
# end;
# $f$
# ;"""
#
#
# @pytest.fixture
# def hcode_id_00004_eq_2():
#     return """select count(0) from dm_rep.dm_all_indicators_v
# where hcode_id = '00004'
# and calc_rule = 'income'
# --and dt in ()
# union all
# select * from public.lilo_auto_qa();"""
#
# # -- Ожидаемый результат: Кол-во записей должно совпадать.
#
#
# # -- Полная сверка
# @pytest.fixture
# def hcode_id_00004_emp_1():
#     return """create or replace function public.lilo_auto_qa()
# 	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8,
# 					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date,
# 					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8)
# language plpgsql
# as $f$
# begin
# 	drop table if exists public.la_qa1;
# 	drop table if exists public.la_qa2;
# 	create table public.la_qa1 as
# 		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00327') and a.unit_id = 45 and a.calc_rule not in ('influence', 'deviation');
# 	create table public.la_qa2 as
# 		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00131') and a.unit_id in (17,89) and a.calc_rule not in ('influence', 'deviation');
# 	return query
# select
# 	'00004'::bpchar as hcode_id,
# 	hcd.name as hcode_name,
# 	hcd.unit_name as hcode_unit_name,
# 	coalesce (a.org_id, b.org_id)::int8 as org_id,
# 	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,
# 	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id,
# 	coalesce (a.metric_type_id, b.metric_type_id)::int8 as metric_type_id,
# 	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id,
# 	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id,
#   	49::int8 as unit_id,
#  	coalesce (a.dt, b.dt)::date as dt,
#   	((a.value/b.value)::numeric(20,6))::float8 as value,
# 	coalesce (a.duch_id, b.duch_id)::int8 as duch_id,
# 	coalesce (a.nod_id, b.nod_id)::int8 as nod_id,
# 	coalesce (a.dir_id, b.dir_id)::int8 as dir_id,
# 	coalesce (a.kato_id, b.kato_id)::int8 as kato_id,
# 	coalesce (a.vids_id, b.vids_id)::int8 as vids_id
# from public.la_qa1 a
# 	left join public.la_qa2 b
# 		on  a.org_id = b.org_id
# 		and a.date_type_id = b.date_type_id
# 		and a.cargo_type_id = b.cargo_type_id
# 		and a.val_type_id = b.val_type_id
# 		and a.metric_type_id = b.metric_type_id
# 		and a.dt = b.dt
# 		and a.nod_id = b.nod_id
# 		and a.duch_id = b.duch_id
# 		and a.vids_id = b.vids_id
# 		and a.kato_id = b.kato_id
# 		and a.dir_id = b.dir_id
# cross join (select * from dm.d_hcode_t where id = '00004') hcd
#     ;
# end;
# $f$
# ;"""
#
# @pytest.fixture
# def hcode_id_00004_emp_2():
#     return """select * from public.lilo_auto_qa()
# except
# select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt,
# 		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id from dm_rep.dm_all_indicators_v
# where hcode_id = '00004'
# and calc_rule = 'income'"""


# -- hcode '00031' + '00149'


@pytest.fixture
def hcode_id_31_149_eq_1():
    return """create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in (%s)and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in (%s) and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
	;
end;
$f$
;"""


@pytest.fixture
def hcode_id_31_149_eq_2():
 return """select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = %s
and calc_rule = 'ratio'
--and dt in ()
union all
select * from public.lilo_auto_qa();"""

# -- Полная сверка


@pytest.fixture
def hcode_id_31_149_emp_1():
    return """create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in (%s) and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in (%s) and a.calc_rule not in ('influence', 'deviation');
	return query
select 
	%s::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (a.org_id, b.org_id)::int8 as org_id,  
	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,  
	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id, 
	coalesce (a.metric_type_id, b.metric_type_id)::int8 as metric_type_id, 
	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id, 
  	%s::int8 as unit_id, 
 	coalesce (a.dt, b.dt)::date as dt, 
  	((a.value/nullif(b.value,0))::numeric(20,6))::float8 as value, 
	coalesce (a.duch_id, b.duch_id)::int8 as duch_id, 
	coalesce (a.nod_id, b.nod_id)::int8 as nod_id, 
	coalesce (a.dir_id, b.dir_id)::int8 as dir_id, 
	coalesce (a.kato_id, b.kato_id)::int8 as kato_id, 
	coalesce (a.vids_id, b.vids_id)::int8 as vids_id
from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
cross join (select * from dm.d_hcode_t where id = %s) hcd
    ;
end;
$f$
;"""


@pytest.fixture
def hcode_id_31_149_emp_2():
    return """select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id from dm_rep.dm_all_indicators_v
where hcode_id = %s
and calc_rule = 'ratio'"""




# -- hcode '00150' --> '00152'

@pytest.fixture
def hcode_id_150_152_eq1():
    return """create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in (%s) and metric_type_id in (1) and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00154') and metric_type_id in (17) and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
	;
end;
$f$
;"""

@pytest.fixture
def hcode_id_150_152_eq2():
    return """select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = %s
and calc_rule = 'ratio'
--and dt in ()
union all
select * from public.lilo_auto_qa();"""


# -- Полная сверка
@pytest.fixture
def hcode_id_150_152_emp1():
    return """create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in (%s) and a.metric_type_id in (1) and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00154') and a.metric_type_id in (17) and a.calc_rule not in ('influence', 'deviation');
	return query
select 
	%s::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (a.org_id, b.org_id)::int8 as org_id,  
	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,  
	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id, 
	1::int8 as metric_type_id, 
	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id, 
  	106::int8 as unit_id, 
 	coalesce (a.dt, b.dt)::date as dt, 
  	(((a.value/nullif(b.value,0))*1000000)::numeric(20,6))::float8 as value, 
	coalesce (a.duch_id, b.duch_id)::int8 as duch_id, 
	coalesce (a.nod_id, b.nod_id)::int8 as nod_id, 
	coalesce (a.dir_id, b.dir_id)::int8 as dir_id, 
	coalesce (a.kato_id, b.kato_id)::int8 as kato_id, 
	coalesce (a.vids_id, b.vids_id)::int8 as vids_id
from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
cross join (select * from dm.d_hcode_t where id = %s) hcd
    ;
end;
$f$
;"""


@pytest.fixture
def hcode_id_150_152_emp2():
    return """select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id from dm_rep.dm_all_indicators_v
where hcode_id = %s
and calc_rule = 'ratio'"""

# -- hcode '00149' - закомментировано

@pytest.fixture
def hcode_id_215_223_1():
    return """select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = %s
and ss = 'SAS'
and metric_type_id in (1,12,17)
--and dt in()
union all
select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = %s
and unit_id = 48
and metric_type_id in (1,12,17)
--and dt in ()"""


@pytest.fixture
def hcode_id_215_223_2():
    return """select 	%s as hcode_id, %s as hcode_name, 'поездо-час' as hcode_unit_id, org_id, dor_kod, 
		date_type_id, metric_type_id, cargo_type_id, val_type_id, '48' as unit_id, dt, (value/60) as value, ss, duch_id, nod_id, dir_id, kato_id, vids_id
	from dm_rep.dm_all_indicators_v
where hcode_id = %s
and ss = 'SAS'
and metric_type_id in (1,12,17)
--and dt in ()
except
select hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, value, ss, duch_id, nod_id,
		dir_id, kato_id, vids_id from dm_rep.dm_all_indicators_v
where hcode_id = %s
and metric_type_id in (1,12,17)
--and dt in ()"""


@pytest.fixture
def hcode_id_297_305_1():
    return """create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in (%s) and metric_type_id = 1 and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00154') and metric_type_id = 17 and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
	;
end;
$f$
;"""


@pytest.fixture
def hcode_id_297_305_2():
    return """select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = %s
and calc_rule = 'ratio'
--and dt in ()
union all
select * from public.lilo_auto_qa();"""



# -- Полная сверка

@pytest.fixture
def hcode_id_297_305_3():
    return """create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in (%s) and a.metric_type_id = 1 and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00154') and a.metric_type_id = 17 and a.calc_rule not in ('influence', 'deviation');
	return query
select 
	%s::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (a.org_id, b.org_id)::int8 as org_id,  
	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,  
	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id, 
	coalesce (a.metric_type_id, b.metric_type_id)::int8 as metric_type_id, 
	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id, 
  	138::int8 as unit_id, 
 	coalesce (a.dt, b.dt)::date as dt, 
  	(((a.value/60/b.value)*1000000)::numeric(20,6))::float8 as value, 
	coalesce (a.duch_id, b.duch_id)::int8 as duch_id, 
	coalesce (a.nod_id, b.nod_id)::int8 as nod_id, 
	coalesce (a.dir_id, b.dir_id)::int8 as dir_id, 
	coalesce (a.kato_id, b.kato_id)::int8 as kato_id, 
	coalesce (a.vids_id, b.vids_id)::int8 as vids_id
from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
cross join (select * from dm.d_hcode_t where id = %s) hcd
    ;
end;
$f$
;"""


@pytest.fixture
def hcode_id_297_305_4():
    return """select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id from dm_rep.dm_all_indicators_v
where hcode_id = %s
and calc_rule = 'ratio'"""


@pytest.fixture
def hcode_id_306_134_1():
    return """select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = %s
and unit_id = %s
and calc_rule not in ('influence', 'deviation')
--and dt in ()
union all
select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = %s
and unit_id = %s
and calc_rule not in ('influence', 'deviation')
--and dt in ()"""


@pytest.fixture
def hcode_id_306_134_2():
    return """select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, 
		unit_id, dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id 
	from dm_rep.dm_all_indicators_v
where hcode_id = %s
and unit_id = %s
and calc_rule not in ('influence', 'deviation')
--and dt in ()
except
select 	%s as hcode_id, hcd."name", hcd.unit_name, 
		org_id, dor_kod, date_type_id	, metric_type_id, cargo_type_id, val_type_id, '%s' as unit_id, dt, 
		(value/1000) as value, ss, duch_id, nod_id, dir_id, kato_id, vids_id
	from dm_rep.dm_all_indicators_v ind
	cross join (select * from dm_rep.d_hcode_v where id = %s) hcd
where hcode_id = %s
and ind.unit_id = %s
and calc_rule not in ('influence', 'deviation')
--and dt in ()"""


@pytest.fixture
def hcode_id_335_337_1():
    return """create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in (%s) and metric_type_id in (1) and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00338') and metric_type_id in (17) and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
	;
end;
$f$
;"""


@pytest.fixture
def hcode_id_335_337_2():
    return """select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = %s
and calc_rule = 'ratio'
--and dt in ()
union all
select * from public.lilo_auto_qa();"""


@pytest.fixture
def hcode_id_335_337_3():
    return """
create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in (%s) and a.metric_type_id in (1) and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00338') and a.metric_type_id in (17) and a.calc_rule not in ('influence', 'deviation');
	return query
select 
	%s::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (a.org_id, b.org_id)::int8 as org_id,  
	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,  
	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id, 
	1::int8 as metric_type_id, 
	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id, 
  	106::int8 as unit_id, 
 	coalesce (a.dt, b.dt)::date as dt, 
  	(((a.value/b.value)*1000000)::numeric(20,6))::float8 as value, 
	coalesce (a.duch_id, b.duch_id)::int8 as duch_id, 
	coalesce (a.nod_id, b.nod_id)::int8 as nod_id, 
	coalesce (a.dir_id, b.dir_id)::int8 as dir_id, 
	coalesce (a.kato_id, b.kato_id)::int8 as kato_id, 
	coalesce (a.vids_id, b.vids_id)::int8 as vids_id
from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
cross join (select * from dm.d_hcode_t where id = %s) hcd
    ;
end;
$f$
;"""


@pytest.fixture
def hcode_id_335_337_4():
    return """select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id from dm_rep.dm_all_indicators_v
where hcode_id = '00335'
and calc_rule = 'ratio'"""


# -- hcode '00150'
#
# query_3_033 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
# language plpgsql
# as $f$
# begin
# 	drop table if exists public.la_qa1;
# 	drop table if exists public.la_qa2;
# 	create table public.la_qa1 as
# 		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00018') and metric_type_id in (1) and calc_rule not in ('influence', 'deviation');
# 	create table public.la_qa2 as
# 		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00154') and metric_type_id in (17) and calc_rule not in ('influence', 'deviation');
# 	return query
# select count(0) from public.la_qa1 a
# 	left join public.la_qa2 b
# 		on  a.org_id = b.org_id
# 		and a.date_type_id = b.date_type_id
# 		and a.cargo_type_id = b.cargo_type_id
# 		and a.val_type_id = b.val_type_id
# 		and a.dt = b.dt
# 		and a.nod_id = b.nod_id
# 		and a.duch_id = b.duch_id
# 		and a.vids_id = b.vids_id
# 		and a.kato_id = b.kato_id
# 		and a.dir_id = b.dir_id
# 	;
# end;
# $f$
# ;""")
#
# query_3_034 = ("""select count(0) from dm_rep.dm_all_indicators_v
# where hcode_id = '00150'
# and calc_rule = 'ratio'
# --and dt in ()
# union all
# select * from public.lilo_auto_qa();""")
#

# @pytest.fixture
# def script_equal():
#     return """select * from (
#     	select 'calc', val_type_id, count(0) from dm_rep.dm_all_indicators_v
#     	where 	calc_rule = 'deviation'
#     		and metric_type_id = %s
#     		and date_type_id = 3
#     		and dt in (""" + date3 + """)
#     	group by val_type_id
#     	union all
#     	select 'join', cd.val_type_id, count(0) from (select * from dm_rep.dm_all_indicators_v) cd
#     		left join (select * from dm_rep.dm_all_indicators_v) pyd
#     			on (	cd.hcode_id = pyd.hcode_id
#     				and cd.org_id = pyd.org_id
#     				and cd.date_type_id = pyd.date_type_id
#     				and cd.metric_type_id = pyd.metric_type_id
#     				and cd.cargo_type_id = pyd.cargo_type_id
#     				and cd.val_type_id = pyd.val_type_id
#     				and cd.unit_id = pyd.unit_id
#     				and cd.dir_id = pyd.dir_id
#     				and cd.vids_id = pyd.vids_id
#     				and cd.kato_id = pyd.kato_id
#     				and cd.duch_id = pyd.duch_id
#     				and cd.nod_id = pyd.nod_id
#     				and date_part('month', cd.dt) = date_part('month', pyd.dt)
#     				and date_part('day', cd.dt) = date_part('day', pyd.dt)
#     				and date_part('year', cd.dt) = date_part('year', pyd.dt)+1)
#     	where 	cd.val_type_id in (1,3,7,8)
#     		and cd.metric_type_id = 17
#     		and cd.date_type_id = 3
#     		and cd.dt in (""" + date3 + """)
#     	group by cd.val_type_id
#     )a
#     order by val_type_id"""
#
#
# @pytest.fixture
# def script_empty():
#     return """select 	cd.hcode_id, hcd.name, hcd.unit_name, cd.org_id, cd.dor_kod, cd.date_type_id, 21 as metric_type_id, cd.cargo_type_id,
# 		cd.val_type_id, cd.unit_id, cd.dt, (cd.value - pyd.value)/abs(case when pyd.value = 0
# 		then null else pyd.value end)*100, cd.ss, cd.duch_id, cd.nod_id, cd.dir_id, cd.kato_id, cd.vids_id
# 		from (select * from dm_rep.dm_all_indicators_v) cd
#         join dm_rep.d_hcode_v hcd on cd.hcode_id = hcd.id
# 		left join (select * from dm_rep.dm_all_indicators_v) pyd
# 			on (	cd.hcode_id = pyd.hcode_id
# 				and cd.org_id = pyd.org_id
# 				and cd.date_type_id = pyd.date_type_id
# 				and cd.metric_type_id = pyd.metric_type_id
# 				and cd.cargo_type_id = pyd.cargo_type_id
# 				and cd.val_type_id = pyd.val_type_id
# 				and cd.unit_id = pyd.unit_id
# 				and cd.dir_id = pyd.dir_id
# 				and cd.vids_id = pyd.vids_id
# 				and cd.kato_id = pyd.kato_id
# 				and cd.duch_id = pyd.duch_id
# 				and cd.nod_id = pyd.nod_id
# 				and date_part('month', cd.dt) = date_part('month', pyd.dt)
# 				and date_part('day', cd.dt) = date_part('day', pyd.dt)
# 				and date_part('year', cd.dt) = date_part('year', pyd.dt)+1)
# where 	cd.val_type_id in (1)
# 	and cd.metric_type_id = %s
# 	and cd.date_type_id = 3
# 	and cd.dt in (""" + date3 + """)
# except
# select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, value,
# 		ss, duch_id, nod_id, dir_id, kato_id, vids_id
# from dm_rep.dm_all_indicators_v
# where 	calc_rule = 'deviation'
# 	and metric_type_id = 21
# 	and date_type_id = 3
# 	and val_type_id = 1
# 	and dt in (""" + date3 + """)"""
#
#
# #,120,22,23,117,204,202
# @pytest.fixture(params=[21, 120])
# def metric_types(request):
#     return request.param