from core.as7265x import AS7265X
from .models import Training
from core.meas.models import Measuring,MeasuringData
from core.meas.utils import MeasuringI2C
from core.binn.models import  BinnacleMessages
import time
def train_thread(name,count,predict):
    try:
        tr,created=Training.objects.get_or_create(name=name)
        tr.state=None
        if created == True:
            tr.predict=predict
        else:
            tr.predict="M"
        __count=tr.count
        tr.count+=count
        tr.save()
        for _count in range(int(count)):
            MeasuringI2C(f"TR~{tr.name}~{__count+_count}",tr,predict)
        tr.state=True
        BinnacleMessages.info("DataTrain Thread",f"OK-----name:{name}-----datas to add: {count}-----datas:{__count}")
    except Exception as e:
        BinnacleMessages.error(e) 
        tr.state=False
    tr.save()


def csv_thread(_1f,count,csv_read,name):
    def save1(count,csv_read,name):
        try:
            t=Training.objects.create(
                name=name,
                predict="C",
            )
            _count=count
            _r=csv_read.decode("utf-8").splitlines()[1:_count]
            rows=[]
            for r in _r:
                rows.append(r.split(',')) 
            for count in range(len(rows)):
                predict=predictChoices[int(rows[count][1])-1][0]
                m=Measuring.objects.create(
                    name=f"T~{name}~{count}",
                    training=t,
                    predict=predict
                )
                
                t.count+=1
                for c,d in enumerate(rows[count],start=-2):
                    if c<0:
                        continue
                    MeasuringData.objects.create(
                        chanel= Measuring.chanels()[c],
                        value=float(d),
                        measuring=m
                    )
            t.state=True
            BinnacleMessages.info("CSV Thread",f"OK-----name: {name}-----datas: {count}")
        except Exception as e:
            BinnacleMessages.error(e)
            t.state=False
        t.save() 
    try:
        if _1f==True:
            return save1(count,csv_read,name)
        t=Training.objects.create(
            name=name,
            predict="C",
        )
        _count=count
        _r=csv_read.decode("utf-8").splitlines()[1:_count]
        rows=[]
        for r in _r:
            rows.append(r.split(',')) 
        for count in range(len(rows)):
            predict=predictChoices[int(rows[count][18])][0]
            m=Measuring.objects.create(
                name=f"T~{name}~{count}",
                training=t,
                predict=predict
            )
            t.count+=1
            for c,d in enumerate(rows[count]):
                if c==18:
                    break
                MeasuringData.objects.create(
                    chanel= Measuring.chanels()[c],
                    value=float(d),
                    measuring=m
                )
        t.state=True
        BinnacleMessages.info("CSV Thread",f"OK-----name: {name}-----datas: {count}")
    except Exception as e:
        BinnacleMessages.error(e)
        t.state=False
    t.save() 
# def TrainingI2C(name,count,predict="N"):
#     tr,created=Training.objects.get_or_create(name=name)
#     if created == True:
#         tr.predict=predict
#     else:
#         tr.predict="M"
#     __count=tr.count
#     tr.count+=count
#     tr.save()
#     # tr=Training.objects.create(
#     #     name=name,
#     #     count=count,
#     #     predict=predict,
#     # )
#     for _count in range(int(count)):
#         MeasuringI2C(f"TR~{tr.name}~{__count+_count}",tr,predict)
    
        