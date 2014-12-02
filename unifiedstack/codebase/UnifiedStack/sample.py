# Sample to check
from logger.models import ConsoleLog
class SampleIntegrator:
    
    @staticmethod
    def print_hello():
        print "HEY IM CALLED>>>> SIMPLE INTEGRATOR"
        
    @staticmethod
    def write_console(msg):
        cl = ConsoleLog(console_summary=msg)
        cl.save()
    