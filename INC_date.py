# ИНКРЕМЕНТ v3 

# date1 = """'2020-08-27'"""
# date2 = """'2020-08-27'"""
# date3 = """'2020-08-27'"""


# ИНКРЕМЕНТ V2 

# # 2.1 Наростайка факт

# date1 = """'2020-08-28',
#  		'2020-08-27',
#         '2020-08-26',
# 		'2020-07-01',
#         '2019-08-28',
#         '2019-08-27',
#         '2019-08-26',
#         '2019-08-01',
#         '2019-07-01'"""

date1 = """(select current_date - 1),
				(select current_date - 2),
				(select current_date - 3),
				--(select date_trunc('month', current_date - 1)),
				(select date_trunc('month', current_date - 1 - interval '1 month')),
				--(select date_trunc('year', current_date - 1 )),
				(select date_trunc('day', current_date - 1 - interval '1 year')),
				(select date_trunc('day', current_date - 2 - interval '1 year')),
				(select date_trunc('day', current_date - 3 - interval '1 year')),
				(select date_trunc('month', current_date - 1 - interval '1 year')),
				(select date_trunc('month', current_date - 1 - interval '1 year' - interval '1 month'))
				--(select date_trunc('year', current_date - 1 - interval '1 year' ))
                """


# # 2.2 Наростайка план 
# # 2.3 Расчет итогов для специфичных показателей

# date2 = """'2020-08-28',
#  		'2020-08-01',
# 		'2020-07-01'"""

date2 = """(select current_date - 1),
						--(select current_date - 2),
						--(select current_date - 3),
						(select date_trunc('month', current_date - 1)),
						(select date_trunc('month', current_date - 1 - interval '1 month'))
						--(select date_trunc('year', current_date - 1 )),
						--(select date_trunc('day', current_date - 1 - interval '1 year')),
						--(select date_trunc('day', current_date - 2 - interval '1 year')),
						--(select date_trunc('day', current_date - 3 - interval '1 year')),
						--(select date_trunc('month', current_date - 1 - interval '1 year')),
						--(select date_trunc('month', current_date - 1 - interval '1 year' - interval '1 month'))
						--(select date_trunc('year', current_date - 1 - interval '1 year' ))
                        """


# # 3. Расчетные показатели
# # 4. Отклонение
# # 5. Влияния

# date3 = """'2020-08-28',
#  		'2020-08-27',
#         '2020-08-26',
# 		'2020-08-01',
#         '2020-07-01',
#         '2019-08-28',
#         '2019-08-27',
#         '2019-08-26',
#         '2019-08-01',
#         '2019-07-01'"""

date3 = """(select current_date - 1),
				(select current_date - 2),
				(select current_date - 3),
				(select date_trunc('month', current_date - 1)),
				(select date_trunc('month', current_date - 1 - interval '1 month')),
				--(select date_trunc('year', current_date - 1 )),
				(select date_trunc('day', current_date - 1 - interval '1 year')),
				(select date_trunc('day', current_date - 2 - interval '1 year')),
				(select date_trunc('day', current_date - 3 - interval '1 year')),
				(select date_trunc('month', current_date - 1 - interval '1 year')),
				(select date_trunc('month', current_date - 1 - interval '1 year' - interval '1 month'))
				--(select date_trunc('year', current_date - 1 - interval '1 year' ))
				"""