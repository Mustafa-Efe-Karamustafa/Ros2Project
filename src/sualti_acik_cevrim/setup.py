from setuptools import setup

package = 'sualti_acik_cevrim'

setup(
    name=package,
    version='0.1.0',
    packages=[package],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package]),
        ('share/' + package, ['package.xml']),
        ('share/' + package + '/launch', ['launch/test_surusu.launch.py']),
        ('share/' + package + '/worlds', ['worlds/pool.sdf']),
    ],
    install_requires=['setuptools'],
    entry_points={'console_scripts': ['test_surusu = sualti_acik_cevrim.surus:main']},
)
