import pyudev

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by('block')

for action, device in monitor:

    if action == 'add' and 'usb' in device.get('ID_BUS'):
        print('Dispositivo almacenamiento insertado:', device.get('DEVNAME'))
    elif action == 'remove' and 'usb' in device.get('ID_BUS'):
	    print('Dispositivo almacenamiento:', device.get('DEVNAME'))