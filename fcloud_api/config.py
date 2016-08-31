__author__ = 'liujiahua'
import logging
# vim: tabstop=4 shiftwidth=4 softtabstop=4

#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

#############################################################################
# Identity Service Endpoint
#############################################################################

KEYSTONE = {
        "uri": "http://10.24.247.1:5000",
        "admin_proj": "62e5e4e323b04598b0822ad422969b86",
        "admin_token": "froad",
        "ks_user": "admin",
        "ks_pass": "froad"
}


DATABASE = 'mysql://root:@localhost/fcloud_api'


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(pathname)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='F:/PY_PROJECT/fcloud_api/logs/all.log',
                    filemode='a')



# change password
C2_CHANGE_VIR_WINDOWS_PWD_SCRIPT = "python /opt/minion/extmods/modules/chg_win_pwd"
C2_CHANGE_VIR_PWD_SCRIPT="python /opt/minion/extmods/modules/chg_pwd"


# http timeout
DEFAULT_TIMEOUT_SECONDS = 10

# Marathon base url
MARATHON_URL = "http://10.43.1.237:8080"

# image register
IMAGE_STORE = 'http://10.24.247.22:5000'