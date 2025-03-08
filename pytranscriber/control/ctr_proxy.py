'''
   (C) 2025 Raryel C. Souza
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from pytranscriber.util.util import MyUtil
from pytranscriber.gui.message_util import MessageUtil
from pytranscriber.gui.proxy.view_proxy import ViewProxy


class Ctr_Proxy():
    proxy = {
        'http': None,
        'https': None
    }

    def __init__(self, ctrMain):
        self.ctrMain = ctrMain
        self.viewProxy = None

    def show(self):
        if self.viewProxy is None:
            self.viewProxy = ViewProxy(self)
        self.viewProxy.show()

    def save(self):
        self.ctrMain.ctrDB.clear_proxy()
        # saving the proxy address
        if self.proxy['https']:
            self.ctrMain.ctrDB.save_proxy(self.proxy)
        # saving proxy address disabled
        else:
            MessageUtil.show_info_message('Proxy disabled successfully', 'Proxy disabled')

    def load_data(self):
        if self.viewProxy is None:
            self.viewProxy = ViewProxy(self)

        data = self.ctrMain.ctrDB.load_proxy()
        if data is not None:
            self.set_proxy_setting(data[1], False)

    def test_proxy_setting(self, proxy_addr):
        proxy = {'http': proxy_addr, 'https': proxy_addr}

        if not MyUtil.is_internet_connected(proxy):
            MessageUtil.show_error_message('Error connecting to Google.','Error')
        else:
            MessageUtil.show_info_message('Successfully connected to Google.', 'Success')

    def set_proxy_setting(self, proxy_addr, frontend_request=False):
        self.proxy = {'http': proxy_addr, 'https': proxy_addr}
        if frontend_request:
            self.save()
        else:
            self.viewProxy.refresh_gui(proxy_addr)

    def get_proxy_setting(self):
        return self.proxy
