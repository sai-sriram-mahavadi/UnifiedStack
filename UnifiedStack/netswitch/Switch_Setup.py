import Switch2960_Setup as sw_2960
import Switch3750_Setup as sw_3750
import Switch9k_Setup as n9k
import TS_Setup as TS


class SwitchConfigurator:
	
	def configure_switch(self)
		sw3750_config = sw_3750.Switch3750Configurator()
		sw3750_config.configure3750_switch()
		sw9k_config = n9k.Switch9kConfigurator()
		sw9k_config.configure9k_switch()


if __name__ == "__main__":
	sw_config = sw.SwitchConfigurator()
	sw_config.configure_switch()
