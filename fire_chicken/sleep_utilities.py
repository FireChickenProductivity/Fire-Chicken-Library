from talon import actions, Module, settings

class SleepSetting:
    def __init__(self, name: str, default_amount: float, description: str, provided_module: Module):
        module = provided_module
        
        self.setting_name = 'user.' + name
        module.setting(
            name,
            type = float,
            default = default_amount,
            desc = f'How much to pause when {description}. If any commands using this setting are not working, try increasing this.'
        )

    def sleep(self):
        actions.sleep(self.get())

    def sleep_with_factor(self, factor):
        actions.sleep(self.get() * factor)
    
    def get(self):
        return settings.get(self.setting_name)

def sleep_max_setting(* args):
    maximum_delay_amount = 0
    for setting in args:
        if setting.get() > maximum_delay_amount:
            maximum_delay_amount = setting.get()
    actions.sleep(maximum_delay_amount)