
from django.views.generic import TemplateView, View
from django.http import HttpResponse
import json

from builtins import print

from openpyxl import Workbook
from openpyxl import load_workbook

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
            d['date'] = row[0].value
            d['name'] = row[1].value
            d['producer'] = row[2].value
            d['symbol'] = row[3].value
            d['contract_type'] = row[4].value
            d['supply'] = row[5].value
            d['base_price'] = row[6].value
            d['supliers_offer'] = row[7].value
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
            d['suplier'] = row[22].value
            d['method_of_supply'] = row[23].value
            d['supply_code'] = row[24].value
            d['supply_type'] = row[25].value

            self.datas.append(d)



    def getProductProducer(self, product_group,start_date,time_slot):

        result = {}

        for item in self.product_producer:



    def supply(self, end_date, time_slot, product_id, producer_id, payment_type):

        x = []
        y = []


        for row in self.datas:

            symbol = producer_id + '-' + product_id
            if symbol in row['symbol']:
                x.append(row['date'])
                y.append(row['supply'])


            d = {}
            d['x'] = x
            d['y'] = y

            return d



