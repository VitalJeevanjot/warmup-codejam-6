from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from web3 import Web3
from kivy.loader import Loader
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
from kivy.uix.recycleview import RecycleView

my_provider = Web3.HTTPProvider('https://rpc.astor.host/node')
w3 = Web3(my_provider)

class Web3Widget(BoxLayout):
    pass

class RV(RecycleView):
    pass

class MainWidget(App):
    # print(w3.eth.filter('pending').get_new_entries())
    transactions = []
    current_address = ""

    def build(self):
        root_widget = Web3Widget()
        return root_widget


    def get_data(self, address, rsv):
        self.current_address = address.text
        req = UrlRequest(url="https://blockscout.funcoin.io/api?module=account&action=txlist&address="+address.text,
                         on_success=self.set_list, on_failure=self.on_error, on_error=self.on_error)
        self.transactions = rsv

    def set_list(self, req, result):
        # Add loading here
        if result['result'] == None:
            self.transactions.data = [{"color": (.5, .5, 1, 1), 'text': str('No transaction for this input box address')}]
        else:
            self.transactions.data = []
            for transaction in result['result']:
                if(self.current_address == transaction['to']):
                    self.transactions.data.append(
                        {
                            "color":(0,1,0,1),
                            "text":str(transaction['value'])
                        }
                    )
                else:
                    self.transactions.data.append(
                        {
                            "color": (1, 0, 0, 1),
                            "text": str(transaction['value'])
                        }
                    )
        pass

    def on_error(self, req, error):
        print('error')
        print(error)
        self.transactions.data = [{"color": (.5, .5, 1, 1), 'text': str(error)}]
        pass
        # App.get_running_app().root.ids.get_values.text



def get_chain_index(dt):
    App.get_running_app().root.ids.blocknom.text = str(w3.eth.blockNumber)


Clock.schedule_once(get_chain_index, 1)

Builder.load_file('Web3.kv')
MainWidget().run()