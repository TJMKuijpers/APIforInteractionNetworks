import requests
import json

class GetInformationFromCtd:

    def __init__(self,database):
        self.database = database
        self.url = None
        self.resp_status_code = None
        self.parameters_for_query = None
        self.response = None
        self.report = None
        self.input_type = None
        self.input_terms = None
        self.url_to_retrieve = None
        self.format_to_report = None
        self.report_parameter = None
        self.filtered_output_json = None

    def set_url_for_request(self):
        if self.database == 'CTD':
            self.url = 'http://ctdbase.org/tools/batchQuery.go'
        resp = requests.get(self.url)
        if resp.status_code != 200:
            raise ApiErrpr('GET url'.format(resp.status_code))
        self.resp_status_code=resp.status_code

    def set_input_type(self,input_type=None):
        self.input_type=input_type

    def set_input_terms_for_ctd(self,input_terms=None):
        self.input_terms=input_terms

    def set_report_parameters(self,report_parameter,format_to_report):
        self.report_parameter = report_parameter
        self.format_to_report = format_to_report

    def get_information_from_database(self):
        self.url_to_retrieve = self.url + '?inputType=' + self.input_type + '&inputTerms=' + self.input_terms + '&report='+self.report_parameter+'&format='+self.format_to_report
        response=requests.get(self.url_to_retrieve)
        if response.status_code == 200:
            print('request is successful')
        self.response = response

    def filter_response_on_organism(self,organism_to_select):
        get_response_report=self.response.json()
        get_response_with_organism=[x for x in get_response_report if 'Organism' in x.keys()]
        response_report_filtered=[i for i in get_response_with_organism if i['Organism'] == organism_to_select]
        response_report_filtered_json=json.dumps(response_report_filtered)
        self.filtered_output_json=response_report_filtered_json

CTD=GetInformationFromCtd('CTD')
CTD.set_url_for_request()
CTD.set_input_type(input_type='chem')
CTD.set_input_terms_for_ctd(input_terms='mercury')
CTD.set_report_parameters(report_parameter='genes_curated',format_to_report='json')
print('CTD status code', CTD.resp_status_code)
CTD.get_information_from_database()
CTD.filter_response_on_organism(organism_to_select='Homo sapiens')