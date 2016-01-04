from django.views.generic import TemplateView, View
from django.http import HttpResponse
import json
import jdatetime as jdate
from openpyxl import load_workbook


ONE_WEEK = 1
THREE_WEEK = 3
THREE_MONTHS = 12
ONE_YEAR = 52


class Index(TemplateView):
    template_name = 'test.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        return context


class Datas(View):
    def __init__(self):
        self.datas = []
        self.product_producer = ['NCI-CCAA-00', 'NCI-CR08AB-00', 'NCI-SLG-00', 'NCI-SLR-00', 'CWD-CR08AB-00']

    def get(self, request, *args, **kwargs):

        labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July']
        datas = [28, 48, 40, 19, 86, 27, 90]
        output = {'labels': labels, 'datas': datas}
        return HttpResponse(json.dumps(output))


    def initialize(self):

        wb = load_workbook(filename='excel_read/test2.xlsx', read_only=True)

        ws = wb.active  # ws is now an IterableWorksheet

        for row in ws:
            d = {}

            if row[0].value == 'تاریخ':
                continue
            dates = row[0].value.split('/')
            persian_date = jdate.date(int(dates[0]), int(dates[1]), int(dates[2]))

            d['date'] = persian_date
            d['date'] = row[0].value
            d['name'] = row[1].value
            d['producer'] = row[2].value
            d['symbol'] = row[3].value
            d['contract_type'] = row[4].value
            d['supply'] = float(row[5].value)
            d['base_price'] = row[6].value
            d['suppliers_offer'] = row[7].value
            d['final_demand'] = row[8].value
            d['payan_sabz'] = row[9].value
            d['highest_demand_price'] = row[10].value
            d['traded_amount'] = row[11].value
            d['least_traded_price_rials'] = row[12].value
            d['Average_traded_price_rials'] = row[13].value
            d['Average_traded_price_origcurrency'] = row[14].value
            d['highest_traded_price_rials'] = row[15].value
            d['value_KRials'] = row[16].value
            d['delivery_date'] = row[17].value
            d['subgroup'] = row[18].value
            d['group'] = row[19].value
            d['main_group'] = row[20].value
            d['details'] = row[21].value
            d['supplier'] = row[22].value
            d['method_of_supply'] = row[23].value
            d['supply_code'] = row[24].value
            d['supply_type'] = row[25].value

            self.datas.append(d)

    # This method takes a symbol which represents a certain product produced by a certain company
    # an end date and a time slot with together represent a time duration. For example if time_slot
    # equals 1, it represents a one week duration ending with end_date (time_slot is given in weeks).
    def extract_chart(self, symbol, chart_name, end_date, time_slot):

        # the list representing the labels of a line chart
        x = []
        # the list representing the data of a line chart
        y = []
        # the return value (a tuple)
        d = None

        if time_slot == ONE_WEEK or time_slot == THREE_WEEK:
            for row in self.datas:

                # Considering a week has 7 days, we extract those rows from our database
                # that match the given symbol and time duration given as inputs to the method
                if symbol == row['symbol'] and row['date'] <= end_date and row['date'] > end_date - time_slot * 7:
                    x.append(row['date'])
                    y.append(row[chart_name])

                d = (x, y)

        elif time_slot == THREE_MONTHS:
            start_date = end_date - 12 * 7
            date = start_date
            while date <= end_date:
                sum_value = 0
                for row in self.datas:
                    if symbol == row['symbol'] and row['date'] > date and row['date'] <= date + 7:
                        sum_value = sum_value + row[chart_name]
                x.append(date + 1)
                y.append(sum_value)
                date += 7
            d = (x, y)

        elif time_slot == ONE_YEAR:
            start_date = jdate.date(end_date.year - 1, end_date.month, end_date.day)
            date = start_date
            while date <= end_date:
                sum_value = 0
                for row in self.datas:
                    if symbol == row['symbol'] and row['date'].year == date.year and row['date'].month == date.month:
                        sum_value = sum_value + row[chart_name]
                x.append(date.j_months_fa[date.month - 1])
                y.append(sum_value)
                date -= 30
            d = (x, y)
        return d

    # for now product_group is set "Copper or مس" as default
    def get_product_producer(self, product_group, end_date, time_slot):

        # a dictionary containing one dictionary per each symbol we are given
        # regarding a specific group of products (eg. Copper).
        result = {}

        # each group of products has a specific symbol for each product produced by a company
        # there is a dictionary (charts_per_symbol) for every symbol, containing tuples of lists
        # for each chart. (There are currently 3 charts, supply, trade and demand)
        # self.product_producer is a list of symbols (for now it contains the symbols regarding the copper group)
        for item in self.product_producer:
            charts_per_symbol = {}

            charts_per_symbol['supply'] = self.extract_chart(item, 'supply', end_date, time_slot)
            charts_per_symbol['demand'] = self.extract_chart(item, 'demand', end_date, time_slot)
            charts_per_symbol['trade'] = self.extract_chart(item, 'trade', end_date, time_slot)

            result[item] = charts_per_symbol
        return result