from technical_analysis import EMA, SMA

list_for_testing = (1,3,4,2,6,2,5,8,2,1,4,5)

ema_3 = SMA(3)

for i in list_for_testing:
    avg = ema_3.add(i)
    sd = ema_3.sigma_delta()
    print(f"added {i} to queue: {ema_3.queue()} - ema: {avg} - sd: {ema_3.sigma_delta()}")