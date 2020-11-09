import pytest
import allure
from income.FR_M_3 import *


#
# @allure.feature('Расчетные показатели')
# @allure.story('Сравнение всех записей')
# @allure.severity('critical')
# def test_equal_00004(hcode_id_00004_eq_1, hcode_id_00004_eq_2, connection):
#     connection.execute(hcode_id_00004_eq_1)
#     connection.execute(hcode_id_00004_eq_2)
#     lines = connection.fetchall()
#     connection.execute('drop function public.lilo_auto_qa();')
#
#     assert lines[0][0] == lines[1][0]
#
#
# @allure.feature('Расчетные показатели')
# @allure.story('Полная сверка')
# @allure.severity('critical')
# def test_empty_00004(connection, hcode_id_00004_emp_1, hcode_id_00004_emp_2):
#     connection.execute(hcode_id_00004_emp_1)
#     connection.execute(hcode_id_00004_emp_2)
#     lines = connection.fetchall()
#     connection.execute('drop function public.lilo_auto_qa();')
#
#     assert lines == []


HCODES_65_103 = [
    ('00097', '00081', '00065'),
    ('00081', '00069', '00066'),
    ('00097', '00069', '00067'),
    ('00097', '00069', '00067'),
    ('00100', '00105', '00099'),
    ('00105', '00102', '00104'),
    ('00100', '00102', '00103'),
    ('00100', '00102', '00103')
]


@allure.feature('Коэффициент соотношения экспуатируемого и рабочего парка локомотивов в грузовом движении.')
@allure.story('Сравнение всех записей')
@allure.severity('critical')
@pytest.mark.parametrize('hcodes', HCODES_65_103)
def test_equeal(connection, hcodes, hcode_id_65_103_eq_1, hcode_id_65_103_eq_2):
    connection.execute(hcode_id_65_103_eq_1, (hcodes[0], hcodes[1]))
    connection.execute(hcode_id_65_103_eq_2, (hcodes[2],))
    lines = connection.fetchall()
    connection.execute('drop function public.lilo_auto_qa();')

    assert lines[0][0] == lines[1][0]


@allure.feature('Коэффициент соотношения экспуатируемого и рабочего парка локомотивов в грузовом движении.')
@allure.story('Полная сверка')
@allure.severity('critical')
@pytest.mark.parametrize('hcodes', HCODES_65_103)
def test_empty(connection, hcodes, hcode_id_65_103_emp_1, hcode_id_65_103_emp_2):
    connection.execute(hcode_id_65_103_emp_1, (hcodes[0], hcodes[1], hcodes[2], hcodes[2]))
    connection.execute(hcode_id_65_103_emp_2, (hcodes[2],))
    lines = connection.fetchall()
    connection.execute('drop function public.lilo_auto_qa();')

    assert lines == []


HCODES_AND_UNIT = [
    ('00031', '00011', '00028', 39),
    ('00149', '00155', '00026', 46)
]


@allure.feature('Вес_вагона. Темп роста производетельности труда')
@allure.story('Сравнение всех записей')
@allure.severity('critical')
@pytest.mark.parametrize('hcodes', HCODES_AND_UNIT)
def test_equal_31_149(connection, hcodes, hcode_id_31_149_eq_1, hcode_id_31_149_eq_2):
    connection.execute(hcode_id_31_149_eq_1, (hcodes[1], hcodes[2]))
    connection.execute(hcode_id_31_149_eq_2, (hcodes[0],))
    lines = connection.fetchall()
    connection.execute('drop function public.lilo_auto_qa();')

    assert lines[0][0] == lines[1][0]


@allure.feature('Вес_вагона. Темп роста производетельности труда')
@allure.story('Полная сверка')
@allure.severity('critical')
@pytest.mark.parametrize('hcodes', HCODES_AND_UNIT)
def test_empty_31_149(connection, hcodes, hcode_id_31_149_emp_1, hcode_id_31_149_emp_2):
    connection.execute(hcode_id_31_149_emp_1, (hcodes[1], hcodes[2], hcodes[0], hcodes[3],hcodes[0]))
    connection.execute(hcode_id_31_149_emp_2, (hcodes[0],))
    lines = connection.fetchall()
    connection.execute('drop function public.lilo_auto_qa();')

    assert lines == []


HCODES_150_152 = [('00150','00018'),
                  ('00151','00019'),
                  ('00152','00020')]


@allure.feature('Удельный показатель по отказам')
@allure.story('Сравнение всех записей')
@allure.severity('critical')
@pytest.mark.parametrize('hcodes', HCODES_150_152)
def test_equal_150_152(connection, hcodes, hcode_id_150_152_eq1, hcode_id_150_152_eq2):
    connection.execute(hcode_id_150_152_eq1, (hcodes[1],))
    connection.execute(hcode_id_150_152_eq2, (hcodes[0],))
    lines = connection.fetchall()
    connection.execute('drop function public.lilo_auto_qa();')

    assert lines[0][0] == lines[1][0]


@allure.feature('Удельный показатель по отказам')
@allure.story('Полная сверка')
@allure.severity('critical')
@pytest.mark.parametrize('hcodes', HCODES_150_152)
def test_empty_150_152(connection, hcodes, hcode_id_150_152_emp1, hcode_id_150_152_emp2):
    connection.execute(hcode_id_150_152_emp1, (hcodes[1], hcodes[0], hcodes[0], ))
    connection.execute(hcode_id_150_152_emp2, (hcodes[0],))
    lines = connection.fetchall()
    connection.execute('drop function public.lilo_auto_qa();')

    assert lines == []


HCODES_215_223 = [
    ('00215', '00109', 'Потери поездо-часов, вызванных отказами 1, 2 категории (поездо-час)'),
    ('00217', '00111', 'Потери поездо-часов, вызванных технологическими нарушениями (поездо-час)'),
    ('00218', '00165', 'Потери поездо-часов из-за отказов 1, 2 категории по типу поездов (грузовые, поездо-час)'),
    ('00219', '00166', 'Потери поездо-часов из-за отказов 1, 2 категории по типу поездов (пассажирские, поездо-час)'),
    ('00220', '00167', 'Потери поездо-часов из-за отказов 1, 2 категории по типу поездов (пригородные, поездо-час)'),
    ('00221', '00168', 'Потери поездо-часов из-за отказов 3 категории по типу поездов (грузовые, поездо-час)'),
    ('00222', '00169', 'Потери поездо-часов из-за отказов 3 категории по типу поездов (пассажирские, поездо-час)'),
    ('00223', '00170', 'Потери поездо-часов из-за отказов 3 категории по типу поездов (пригородные, поездо-час)')
]


@allure.feature('Потери поездо-часов')
@allure.story('Сравнение всех записей')
@allure.severity('critical')
@pytest.mark.parametrize('hcodes', HCODES_215_223)
def test_equal_215_223(connection, hcodes, hcode_id_215_223_1):
    connection.execute(hcode_id_215_223_1, (hcodes[1], hcodes[0]))
    lines = connection.fetchall()

    assert lines[0][0] == lines[1][0]


@allure.feature('Потери поездо-часов')
@allure.story('Полная сверка')
@allure.severity('critical')
@pytest.mark.parametrize('hcodes', HCODES_215_223)
def test_empty_215_223(connection, hcodes, hcode_id_215_223_2):
    connection.execute(hcode_id_215_223_2, (hcodes[0], hcodes[2], hcodes[1], hcodes[0],))
    lines = connection.fetchall()

    assert lines == []


HCODES_297_305 = [
    ('00297', '00109'),
    ('00299', '00111'),
    ('00300', '00165'),
    ('00301', '00166'),
    ('00302', '00167'),
    ('00303', '00168'),
    ('00304', '00169'),
    ('00305', '00170')
]


@allure.feature('Удельный показатель по потерям поездо-часов')
@allure.story('Сравнение всех записей')
@allure.severity('critical')
@pytest.mark.parametrize('hcodes', HCODES_297_305)
def test_equal_297_305(connection, hcodes, hcode_id_297_305_1, hcode_id_297_305_2):
    connection.execute(hcode_id_297_305_1, (hcodes[1],))
    connection.execute(hcode_id_297_305_2, (hcodes[0],))
    lines = connection.fetchall()
    connection.execute('drop function public.lilo_auto_qa();')

    assert lines[0][0] == lines[1][0]


@allure.feature('Удельный показатель по потерям поездо-часов')
@allure.story('Полная сверка')
@allure.severity('critical')
@pytest.mark.parametrize('hcodes', HCODES_297_305)
def test_empty_297_305(connection, hcodes, hcode_id_297_305_3, hcode_id_297_305_4):
    connection.execute(hcode_id_297_305_3, (hcodes[1], hcodes[0], hcodes[0], ))
    connection.execute(hcode_id_297_305_4, (hcodes[0],))
    lines = connection.fetchall()
    connection.execute('drop function public.lilo_auto_qa();')

    assert lines == []


HCODES_306_134 =[
    ('00328', 45, '00306', 25),
    ('00322', 41, '00308', 8),
    ('00323', 41, '00309', 8),
    ('00324', 29, '00310', 17),
    ('00325', 29, '00311', 17),
    ('00326', 29, '00312', 17),
    ('00327', 45, '00043', 25),
    ('00002', 41, '00134', 8)
]


@allure.feature('[СЕЛЕКТОР]')
@allure.story('Сравнение всех записей')
@allure.severity('critical')
@pytest.mark.parametrize('hcodes', HCODES_306_134)
def test_equal_306_134(connection, hcodes, hcode_id_306_134_1):
    connection.execute(hcode_id_306_134_1, (hcodes[2], hcodes[3], hcodes[0], hcodes[1]))
    lines = connection.fetchall()

    assert lines[0][0] == lines[1][0]


@allure.feature('[СЕЛЕКТОР]')
@allure.story('Полная сверка')
@allure.severity('critical')
@pytest.mark.parametrize('hcodes', HCODES_306_134)
def test_empty_306_134(connection, hcodes, hcode_id_306_134_2):
    connection.execute(hcode_id_306_134_2, (hcodes[2], hcodes[3], hcodes[2], hcodes[3],hcodes[2],hcodes[0],hcodes[1]))
    lines = connection.fetchall()

    assert lines == []


HCODES_335_337 = [
    ('00335', '00318'),
    ('00336', '00319'),
    ('00337', '00320')
]


@allure.feature('[СЕЛЕКТОР]Удельный показатель по отказам ')
@allure.story('Сравнение всех записей')
@allure.severity('critical')
@pytest.mark.parametrize('hcodes', HCODES_335_337)
def test_equal_297_305(connection, hcodes, hcode_id_335_337_1, hcode_id_335_337_2):
    connection.execute(hcode_id_335_337_1, (hcodes[1],))
    connection.execute(hcode_id_335_337_2, (hcodes[0],))
    lines = connection.fetchall()
    connection.execute('drop function public.lilo_auto_qa();')

    assert lines[0][0] == lines[1][0]


@allure.feature('[СЕЛЕКТОР]Удельный показатель по отказам ')
@allure.story('Полная сверка')
@allure.severity('critical')
@pytest.mark.parametrize('hcodes', HCODES_335_337)
def test_empty_297_305(connection, hcodes, hcode_id_335_337_3, hcode_id_335_337_4):
    connection.execute(hcode_id_335_337_3, (hcodes[1], hcodes[0], hcodes[0]))
    connection.execute(hcode_id_335_337_4, (hcodes[0],))
    lines = connection.fetchall()
    connection.execute('drop function public.lilo_auto_qa();')

    assert lines == []


QUERIES_COMPARE = [
    (query_3_01, query_3_02),
    (query_3_25,),
    (query_3_27,),
    (query_3_29,),
    (query_3_30,),
    (query_3_073, query_3_074),
    (query_3_045, query_3_046),
    (query_3_50,),
    (query_3_049, query_3_050),
    (query_3_053, query_3_054),
    (query_3_0129, query_3_0130),
    (query_3_0121, query_3_0122),
    (query_3_061, query_3_062),
    (query_3_057, query_3_058),
    (query_3_98,),
    (query_3_0129, query_3_0130),
    (query_3_88,),
    (query_3_065, query_3_066),
    (query_3_069, query_3_070)
]


@allure.feature('Расчетные показатели')
@allure.story('Сравнение всех записей')
@allure.severity('critical')
@pytest.mark.parametrize('query', QUERIES_COMPARE)
def test_income_equal(query, connection):
    if len(query) == 2:
        connection.execute(query[0])
        connection.execute(query[1])
        lines = connection.fetchall()
        connection.execute('drop function public.lilo_auto_qa();')

        assert lines[0][0] == lines[1][0]

    elif len(query) == 1:
        connection.execute(query[0])
        lines = connection.fetchall()
        #connection.execute('drop function public.lilo_auto_qa();')

        assert lines[0][0] == lines[1][0]


QUERIES_EMPTY = [
    (query_3_03, query_3_04),
    (query_3_26,),
    (query_3_28,),
    (query_3_31,),
    (query_3_075, query_3_076),
    (query_3_047, query_3_048),
    (query_3_51,),
    (query_3_051, query_3_052),
    (query_3_055, query_3_056),
    (query_3_0131, query_3_0132),
    (query_3_0123, query_3_0124),
    (query_3_063, query_3_064),
    (query_3_059, query_3_060),
    (query_3_99,),
    (query_3_0131, query_3_0132),
    (query_3_89,),
    (query_3_067, query_3_068),
    (query_3_071, query_3_072)
]


@allure.feature('Расчетные показатели')
@allure.story('Полная сверка')
@allure.severity('critical')
@pytest.mark.parametrize('query', QUERIES_EMPTY)
def test_income_empty(query, connection):
    if len(query) == 2:
        connection.execute(query[0])
        connection.execute(query[1])
        lines = connection.fetchall()
        connection.execute('drop function public.lilo_auto_qa();')

        assert lines == []

    elif len(query) == 1:
        connection.execute(query[0])
        lines = connection.fetchall()
        #connection.execute('drop function public.lilo_auto_qa();')

        assert lines == []