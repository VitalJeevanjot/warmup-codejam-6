from pathlib import Path

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from web3 import Web3
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
from kivy.uix.recycleview import RecycleView
from kivy.properties import ColorProperty
from kivy.properties import StringProperty
import webbrowser

my_provider = Web3.HTTPProvider('https://rpc.astor.host/node')
w3 = Web3(my_provider)


BLOCK_SCOUT_URL = "https://blockscout.funcoin.io/api?module=account&action=txlist&address={}"
LAST_SEARCH_FILE = Path(__file__).parent / 'last_search.txt'

class CustomLabel(BoxLayout):

    def __init__(self, **kwargs):
        super(CustomLabel, self).__init__(**kwargs)
        label_text = StringProperty(None)
        transaction_id = StringProperty(None)
        label_color = ColorProperty(None)

    def open_url(self, transaction_id):
        webbrowser.open_new_tab('https://blockscout.funcoin.io/tx/'+transaction_id+'/internal_transactions')


class Web3Widget(BoxLayout):
    pass


class RV(RecycleView):
    pass


class MainWidget(App):
    # print(w3.eth.filter('pending').get_new_entries())
    transactions = []
    
    last_search = ''

    def build(self):
        root_widget = Web3Widget()
        return root_widget

    def get_data(self, address, rsv):

        req = UrlRequest(url=BLOCK_SCOUT_URL.format(address.text),
                         on_success=self.set_list,
                         on_failure=self.on_error,
                         on_error=self.on_error)
        self.transactions = rsv
        self.last_search = address.text

    def set_list(self, req, result):
        # Add loading here
        if result['result'] == None:
            self.transactions.data = [
                {"label_color": (.5, .5, 1, 1),
                 'label_text': str('No transaction for this input box address'),
                 'transaction_id':''
                 }
            ]
        else:
            self.transactions.data = []
            for transaction in result['result']:
                if(self.last_search.lower() == transaction['to'].lower()):
                    self.transactions.data.append(
                        {
                            "label_color":(0,1,0,1),
                            "label_text":str(transaction['value']),
                            "transaction_id":transaction['hash']
                        }
                    )
                else:
                    self.transactions.data.append(
                        {
                            "label_color": (1, 0, 0, 1),
                            "label_text": str(transaction['value']),
                            "transaction_id": transaction['hash']
                        }
                    )
        pass


    def on_error(self, req, error):
        print('error')
        print(error)
        self.transactions.data = [
            {"label_color": (.5, .5, 1, 1),
             'label_text': str(error),
             "transaction_id":''
             }
        ]
        pass
        # App.get_running_app().root.ids.get_values.text

    def on_start(self):
        if LAST_SEARCH_FILE.exists():
            with open(LAST_SEARCH_FILE, 'r') as f:
                self.last_search = f.read()

    def on_stop(self):
        with open(LAST_SEARCH_FILE, 'w') as f:
            f.write(self.last_search)


def get_chain_index(dt):
    App.get_running_app().root.ids.blocknom.text = str(w3.eth.blockNumber)


Clock.schedule_once(get_chain_index, 1)

Builder.load_file('Web3.kv')
MainWidget().run()
