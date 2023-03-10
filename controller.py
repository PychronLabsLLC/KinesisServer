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
import clr, time

POLLING_INTERVAL = 250
ENABLE_SLEEP_TIME = 0.1

import kinesis

kinesis.check_import()

from System import Decimal

clr.AddReference('System.Collections')

clr.AddReference("Thorlabs.MotionControl.GenericMotorCLI")
clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI")

from Thorlabs.MotionControl.DeviceManagerCLI import DeviceManagerCLI


class BenchTopStepperController:
    device = None

    def __init__(self, serial_number):
        self.serial_number = str(serial_number)

    def get_device(self):
        try:
            device = self.device
        except AttributeError:
            print('device not created!')
            raise

        return device

    def get_channel(self, idx):
        device = self.get_device()
        return device.GetChannel(idx)

    def create(self):
        clr.AddReference("ThorLabs.MotionControl.Benchtop.StepperMotorCLI")
        from Thorlabs.MotionControl.Benchtop.StepperMotorCLI import BenchtopStepperMotor

        DeviceManagerCLI.BuildDeviceList()
        self.device = BenchtopStepperMotor.CreateBenchtopStepperMotor(self.serial_number)

    def enable(self):
        device = self.get_device()

        device.Connect(self.serial_number)

        for i in range(3):
            channel = device.GetChannel(i + 1)
            if not channel.IsSettingsInitialized():
                channel.WaitForSettingsInitialized(self.INIT_TIMEOUT)

            channel.StartPolling(POLLING_INTERVAL)
            time.sleep(ENABLE_SLEEP_TIME)
            channel.EnableDevice()
            time.sleep(ENABLE_SLEEP_TIME)

            channel.LoadMotorConfiguration(channel.DeviceID)

    def get_position(self, channel):
        channel = self.get_channel(channel)
        return Decimal.ToDouble(channel.DevicePosition)

    def linear_move(self, x, y):
        xm = self.get_channel(1)
        xm.MoveTo(Decimal(x), 0)
        ym = self.get_channel(2)
        ym.MoveTo(Decimal(y), 0)

    def home(self):
        for i in range(3):
            channel = self.get_channel(i+1)
            channel.Home(0)

    def move_absolute(self, axis, pos):
        m = self.get_channel(axis)
        m.MoveTo(Decimal(pos), 0)

    def move_relative(self, axis, pos):
        m = self.get_channel(axis)
        m.SetMoveRelativeDistance(Decimal(pos))
        m.MoveRelative(0)


def get_controller(serial_number):
    controller = BenchTopStepperController(str(serial_number))
    controller.create()
    controller.enable()
    return controller

# ============= EOF =============================================
