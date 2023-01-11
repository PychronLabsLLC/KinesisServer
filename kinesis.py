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
import os, sys, clr

THORLABS_KINESIS_CONTROL_DLL_FILENAME = 'Thorlabs.MotionControl.Controls.dll'

this = sys.modules[__name__]
this.PATH_SET = False


def check_import():
    if not this.PATH_SET:
        raise ImportError('Must initialize before importing this package. Use py_thorlabs_ctrl.kinesis.init(path)')


def init(path):
    if os.path.isdir(path):
        if os.path.exists(os.path.join(path, THORLABS_KINESIS_CONTROL_DLL_FILENAME)):
            sys.path.append(path)
            this.PATH_SET = True
        else:
            raise ImportError('Cannot find .NET controls')
    else:
        raise ImportError('Path does not exist')

    clr.AddReference('System.Collections')

    clr.AddReference("Thorlabs.MotionControl.Controls")
    import Thorlabs.MotionControl.Controls

# ============= EOF =============================================
