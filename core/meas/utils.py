from core.as7265x import AS7265X
from .models import Measuring,MeasuringData,Training
import time
from config._config import ENVIRONMENT
def MeasuringI2C(name,training=None,prediction="N"):
    try:
        if ENVIRONMENT=="RASPBERRY":
            from smbus import SMBus    
            _as7265x=AS7265X(SMBus(1))
            _as7265x.begin()
            _as7265x.takeMeasurementsWithBulb()
            _l=['A','B','C','D','E','F','G','H','I','J','K','L','R','S','T','U','V','W']
            measuring=Measuring.objects.create(
                name=name,
                training=training,
                predict=prediction,
            )
            for l in _l:
                MeasuringData.objects.create(
                    chanel=l,
                    value=eval(f"_as7265x.getCalibrated{l}()"),
                    measuring=measuring,
                )
        else:
            import random
            _l=['A','B','C','D','E','F','G','H','I','J','K','L','R','S','T','U','V','W']
            
            measuring=Measuring.objects.create(
                name=name,
                training=training,
                predict=prediction,
            )
            for l in _l:
                MeasuringData.objects.create(
                    chanel=l,
                    value=random.randint(0,10000/100),
                    measuring=measuring,
                )
    except ModuleNotFoundError:
        pass
    return measuring
