# Açık çevrim su altı aracı testi

ROS 2 Humble ve Gazebo Fortress ile çalışır. Paket, arşivdeki havuz ve araç
modelini kullanır. X ekseninde gövdeye sırasıyla +11 N (5 saniye),
0 N (2 saniye), −11 N (5 saniye) ve 0 N uygulanır.
Düğüm sadece Gazebo saatini kullanır. Sensör, odometri ve PID yoktur.
Atalet ve sürüklenme nedeniyle araç başlangıç noktasına tam dönmeyebilir.

```bash
cd "$(xdg-user-dir DESKTOP)/ros2_ws2"
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
ros2 launch sualti_acik_cevrim test_surusu.launch.py
```

Arayüzsüz çalıştırmak için son komuta `gui:=false` ekleyin.
Süre ve kuvveti değiştirmek için `surus.py` içindeki `PHASES` dizisini düzenleyin.
