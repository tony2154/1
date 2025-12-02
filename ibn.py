import yaml
from netmiko import ConnectHandler

# Cargar dispositivos desde devices.yaml
with open('/home/tony/redes-ibn/ibn_project/devices/devices.yaml') as f:
    devices = yaml.safe_load(f)

def config_device(device):

    # Solo routers y switches
    if device['type'] not in ['router', 'switch']:
        return

    # Tomar la primera IP del YAML (sin la máscara /24)
    ip = list(device['interfaces'].values())[0].split('/')[0]

    print(f"\n🔌 Conectando a {device['hostname']} ({ip})")

    # Conexión SSH con Netmiko
    try:
        conn = ConnectHandler(
            device_type='cisco_ios',
            host=ip,
            username='cisco',
            password='cisco'
        )
    except Exception as e:
        print(f"❌ Error de conexión a {ip}: {e}")
        return

    commands = []

    # Configurar todas las interfaces que tengan IP
    for intf, ip_addr in device['interfaces'].items():
        if "Gi" in intf:
            commands.append(f"interface {intf}")
            commands.append(f"ip address {ip_addr}")
            commands.append("no shutdown")

    # Enviar configuración
    if commands:
        output = conn.send_config_set(commands)
        print(output)

    conn.disconnect()

# Ejecutar configuración en todos los dispositivos del YAML
for dev_name, dev_data in devices.items():
    config_device(dev_data)
