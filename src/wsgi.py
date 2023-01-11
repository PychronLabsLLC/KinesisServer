# ===============================================================================
# Copyright 2023 ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================

from flask import Flask
from src import kinesis
kinesis.init(r'C:\Program Files\Thorlabs\Kinesis')

from src.controller import get_controller

app = Flask(__name__)

controller = get_controller(70206084)

@app.route('/position/<int:axis>')
def get_position(axis):
    resp = {axis: {'position': controller.get_position(axis)}}
    return resp


@app.route('/positions')
def get_positions():
    resp = {}
    for i in range(3):
        axis = i+1
        resp[axis] = {'position': controller.get_position(axis)}


if __name__ == '__main__':
    app.run()

# ============= EOF =============================================
