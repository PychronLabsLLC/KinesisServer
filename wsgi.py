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
import sys, os

sys.path.append(os.path.dirname(__file__))

import kinesis

kinesis.init(r'C:\Program Files\Thorlabs\Kinesis')

from controller import get_controller

app = Flask(__name__)


CONTROLLER_SERIAL_NUMBER = os.environ.get('KINESIS_SN', '70206084')

controller = get_controller(CONTROLLER_SERIAL_NUMBER)


@app.route('/position/<int:axis>')
def get_position(axis):
    resp = {axis: {'position': controller.get_position(axis)}}
    return resp


@app.route('/positions')
def get_positions():
    resp = {}
    for i in range(3):
        axis = i + 1
        resp[axis] = {'position': controller.get_position(axis)}
    return resp


@app.route('/linear_move/<float: x>/<float: y>', methods=['POST'])
def linear_move(x, y):
    controller.linear_move(x, y)
    return {'status': 'OK'}


@app.route('/move_absolute/<int: axis>/<float: pos>', methods=['POST'])
def move_absolute(axis, pos):
    controller.move_absolute(axis, pos)
    return {'status': 'OK'}


@app.route('/move_relative/<int: axis>/<float: pos>', methods=['POST'])
def move_relative(axis, pos):
    controller.move_relative(axis, pos)
    return {'status': 'OK'}


@app.route('/home', methods=['POST'])
def home():
    controller.home()
    return {'status': 'OK'}
# ============= EOF =============================================
