from talon import actions, Module

class SleepSetting:
    def __init__(self, name: str, default_amount: float, description: str):
        module = Module()
        self.setting = module.setting(
            name,
            type = float,
            default = default_amount,
            desc = f'How much to pause when {description}. If any commands using this setting are not working, try increasing this.'
        )

    def sleep(self):
        actions.sleep(self.get())
    
    def get(self):
        return self.setting.get()

def sleep_max_setting(* args):
    maximum_delay_amount = 0
    for setting in args:
        if setting.get() > maximum_delay_amount:
            maximum_delay_amount = setting.get()
    actions.sleep(maximum_delay_amount)
