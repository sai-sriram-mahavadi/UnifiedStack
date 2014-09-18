#import Switch2960_Setup as sw_2960
import Switch3750_Setup as sw_3750
import Switch9k_Setup as n9k
#import TS_Setup as TS


class SwitchConfigurator:

    def configure_switch(self, console):
        sw3750_config = sw_3750.Switch3750Configurator()
        sw3750_config.configure_3750switch(console)
        console.cprint_progress_bar("Configured the 3750 switch", 50)
        sw9k_config = n9k.Switch9kConfigurator()
        sw9k_config.configure_9kswitch()
        console.cprint_progress_bar("Configured the N9K switch", 100)


if __name__ == "__main__":
    sw_config = sw.SwitchConfigurator()
    sw_config.configure_switch()
