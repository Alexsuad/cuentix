#!/bin/bash

echo "🔧 Corrigiendo DNS para WSL..."

# 1. Configurar WSL para que no sobrescriba resolv.conf
echo "[network]" | sudo tee /etc/wsl.conf > /dev/null
echo "generateResolvConf = false" | sudo tee -a /etc/wsl.conf > /dev/null
echo "✅ Archivo /etc/wsl.conf actualizado."

# 2. Eliminar resolv.conf si existe y recrear manualmente
sudo rm -f /etc/resolv.conf
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf > /dev/null
echo "nameserver 1.1.1.1" | sudo tee -a /etc/resolv.conf > /dev/null
echo "options timeout:1" | sudo tee -a /etc/resolv.conf > /dev/null
echo "✅ Archivo /etc/resolv.conf configurado manualmente."

# 3. Proteger resolv.conf para evitar sobrescritura futura
sudo chattr +i /etc/resolv.conf
echo "🔒 Archivo /etc/resolv.conf protegido (chattr +i)."

# 4. Instalar resolvconf si no está instalado
if ! command -v resolvconf &> /dev/null; then
  echo "📦 Instalando resolvconf..."
  sudo apt update && sudo apt install -y resolvconf
else
  echo "✅ resolvconf ya está instalado."
fi

# 5. Reiniciar servicio de DNS
sudo service resolvconf restart
echo "♻️ Servicio resolvconf reiniciado."

# 6. Aviso para cerrar WSL
echo "⚠️ Para aplicar completamente los cambios, ejecuta: wsl --shutdown desde PowerShell y vuelve a entrar."

echo "✅ DNS corregido con éxito en WSL."
