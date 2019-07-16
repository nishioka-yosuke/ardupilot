from dronekit import connect,VehicleMode,LocationGlobalRelative
import time

# 機体へコネクト
vehicle = connect("tcp:127.0.0.1:5762",wait_ready=True)
print("vehicle is connected")

print(vehicle.mode.name,vehicle.armed)

while not vehicle.is_armable:
    print("Waiting for vehhicle to initialize...")
    time.sleep(1)

# ホームロケーションのロード
while not vehicle.home_location:
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()

    if not vehicle.home_location:
        print("Waiting for home location...")
print("\n Home location: %s"%vehicle.home_location)

homelat = vehicle.location.global_relative_frame.lat
homelon = vehicle.location.global_relative_frame.lon
homealt = 15

# targetロケーションの設定
# target A (上)
targetlat_A = homelat + 0.00009013
targetlon_A = homelon 
targetalt_A = homealt + 5

# target B (左下)
targetlat_B = homelat - 0.00016305
targetlon_B = homelon - 0.00006428 
targetalt_B = homealt - 5

# target C (右上)
targetlat_C = homelat + 0.00010077
targetlon_C = homelon + 0.00016825
targetalt_C = homealt

# target D (左上)
targetlat_D = homelat
targetlon_D = homelon - 0.00020794
targetalt_D = homealt

# target E (右下)
targetlat_E = homelat - 0.00010077
targetlon_E = homelon + 0.00016825
targetalt_E = homealt - 5

# target F (home)
targetlat_F = targetlat_A
targetlon_F = targetlon_A
targetalt_F = targetalt_A

# targetのタプル（リスト）の作成
targetlat = (targetlat_A,targetlat_B,targetlat_C,targetlat_D,targetlat_E,targetlat_F)
targetlon = (targetlon_A,targetlon_B,targetlon_C,targetlon_D,targetlon_E,targetlon_F)
targetalt = (targetalt_A,targetalt_B,targetalt_C,targetalt_D,targetalt_E,targetalt_F)

print("Arming  motors")
vehicle.mode = VehicleMode("GUIDED")
vehicle.armed =True

while not vehicle.armed:
    print("Waiting for arming...")
    time.sleep(1)

print("Take off!!!")
vehicle.simple_takeoff(homealt)

while True:
    if vehicle.location.global_relative_frame.alt >= homealt-0.1:
        print("Reached home Location!!")
        print("Latitude:",vehicle.location.global_relative_frame.lat,",","Longitude:",vehicle.location.global_relative_frame.lon,",","Altitude:",vehicle.location.global_relative_frame.alt)
        break

time.sleep(5)

# star型飛行
for i in range(6):
    targetlocation = LocationGlobalRelative(targetlat[i],targetlon[i],targetalt[i])
    judgelatmin = targetlat[i] - 0.0000009
    judgelatmax = targetlat[i] + 0.0000009
    judgelonmin = targetlon[i] - 0.00000109
    judgelonmax = targetlon[i] + 0.00000109
    judgealtmin = targetalt[i] - 0.1
    judgealtmax = targetalt[i] + 0.1

    vehicle.simple_goto(targetlocation, groundspeed=10) 
    while True:
        if vehicle.location.global_relative_frame.lat >= judgelatmin and vehicle.location.global_relative_frame.lat <= judgelatmax:
            if vehicle.location.global_relative_frame.lon >= judgelonmin and vehicle.location.global_relative_frame.lon <= judgelonmax:
                if vehicle.location.global_relative_frame.alt >= judgealtmin and vehicle.location.global_relative_frame.alt <= judgealtmax:
                    print("Reached target Location")
        break
    time.sleep(20)
    print("Latitude:",vehicle.location.global_relative_frame.lat,",","Longitude:",vehicle.location.global_relative_frame.lon,",","Altitude:",vehicle.location.global_relative_frame.alt)
    print("target:",i," finish")
    print("next")

time.sleep(10)

print("Returning to Launch")
vehicle.mode = VehicleMode("RTL")

time.sleep(1)

print("Close vehicle object")
vehicle.close()
