from setuptools import find_packages, setup

package_name = 'my_teleop'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Ryoya SATO',
    maintainer_email='satoryoya1012711@gmail.com',
    description='ZX200 Teleoperation package using PS5 controller',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'zx200_teleop_node = my_teleop.zx200_ps5_teleop:main',
            ],
    },
)
