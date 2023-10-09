
Доступные переменные перечислены ниже вместе со значениями по умолчанию (set defaults/main.yml):
dnsdist_install_repo: ""

По умолчанию dnsdist устанавливается из репозиториев программного обеспечения, настроенных на целевых хостах.
# Install dnsdist from the master branch
- hosts: dnsdist
  roles:
  - { role: PowerDNS.dnsdist,
      dnsdist_install_repo: "{{ dnsdist_powerdns_repo_master }}"

# Install dnsdist 1.3.x
- hosts: dnsdist
  roles:
  - { role: PowerDNS.dnsdist,
      dnsdist_install_repo: "{{ dnsdist_powerdns_repo_13 }}"

Приведенные выше примеры показывают, как установить DNSdist из официальных репозиториев PowerDNS (смотрите полный список предопределенных репозиториев в vars/main.yml).

Также возможно установить dnsdist из пользовательских репозиториев, как показано в примере ниже.
- hosts: all
  vars:
    dnsdist_install_repo:
      name: "dnsdist" # the repository name
      apt_repo_origin: "example.com"  # used to pin dnsdist to the provided repository
      apt_repo: "deb http://example.com/{{ ansible_distribution | lower }} {{ ansible_distribution_release | lower }}/dnsdist main"
      gpg_key: "http://example.com/MYREPOGPGPUBKEY.asc" # repository public GPG key
      gpg_key_id: "MYREPOGPGPUBKEYID" # to avoid to reimport the key each time the role is executed
      yum_repo_baseurl: "http://example.com/centos/$basearch/$releasever/dnsdist"
      yum_debug_symbols_repo_baseurl: "http://example.com/centos/$basearch/$releasever/dnsdist/debug"
  roles:
  - { role: PowerDNS.dnsdist }
  
По умолчанию установите EPEL для удовлетворения некоторых зависимостей DNSdist, таких как lid sodium. 
Чтобы пропустить установку EPEL, установите для переменной dnsdist_install_epel значение False.
dnsdist_install_epel: True

Название пакета dnsdist: "dnsdist" как в дистрибутивах RHEL, так и в производных от Debian.
dnsdist_package_name: "{{ default_dnsdist_package_name }}"

При необходимости разрешите установить определенную версию пакета dnsdist для установки.
dnsdist_package_version: ""

Установите пакет dnsdist debug symbols.
dnsdist_install_debug_symbols_package: False

Имя пакета dnsdist debug symbols, который будет установлен, если dnsdist_install_debug_symbols_package имеет значение True.
dnsdist_debug_symbols_package_name: "{{ default_dnsdist_debug_symbols_package_name }}"

Настраивает ACLS dnsdist (netmask).
dnsdist_acls: []

Настраивает адреса прослушивания dnsdist.
dnsdist_locals: ['127.0.0.1:5300']

Список IP-адресов нижестоящих DNS-серверов dnsdist должен содержать отправку трафика в таблицы Lua или из таблиц, 
которые функционируют на сервере новостей ( https://dnsdist.org/reference/config.html#newServer ) может анализировать.
dnsdist_servers:
  - '127.0.0.1'
  - "{ address='127.0.0.1:5300', source='127.0.0.1@lo', order=1 }"
  
IP-адрес сервера Carbon, который должен получать показатели dnsdist.
dnsdist_carbonserver: ""

IP-адрес прослушиваемого TCP-сокета управления dnsdist.
dnsdist_controlsocket: "127.0.0.1"

Ключ шифрования для управляющего TCP-сокета dnsdist. Если он пуст, то будет сгенерирован случайный ключ.
Если ключ уже присутствует в файле, он будет сохранен.
dnsdist_setkey: ""

IP-адрес прослушиваемого встроенного веб-сервера пуст, таким образом, по умолчанию отключен.
dnsdist_webserver_address: ""

Учетные данные для проверки подлинности встроенного веб-сервера. Должен быть установлен, когда задан dnsdist_web server_address.
dnsdist_webserver_password: ""

Учетные данные для проверки подлинности встроенного API.
dnsdist_webserver_apikey: ""

Начиная с версии 1.5.0, по умолчанию разрешены только подключения с 127.0.0.1 и ::1. 
Смотри https://dnsdist.org/guides/webserver.html для получения дополнительной информации.
dnsdist_webserver_acl: ""

Дополнительная конфигурация dnsdist должна быть введена дословно в файл dnsdist.conf.
dnsdist_config: ""

Пользователь и группа, которым принадлежит файл dnsdist.conf.
dnsdist_config_owner: 'root'
dnsdist_config_group: 'root'

Dict с переопределениями для службы (только для систем). Это можно использовать для изменения любых системных настроек в категории [Service].
dnsdist_service_overrides: {}

Dict с переопределениями для сервисного модуля (только systemd). Это можно использовать для изменения любых системных настроек в категории [Unit].
dnsdist_unit_overrides: {}

Dict с переопределениями для служебных сред (только для систем). Это можно использовать 
для изменения любых переменных окружения в системных настройках в категории [Service].
dnsdist_environment_overrides: {}

Позволяет указать желаемое состояние службы DNSdist. Например. Это позволяет устанавливать и настраивать DNSdist без автоматического запуска службы.
dnsdist_service_state: "started"
dnsdist_service_enabled: "yes"

Отключает автоматический перезапуск службы при изменении конфигурации.
dnsdist_disable_handlers: False

Настраивает DNS через прослушиватели TLS. Записи копируются дословно, запись за записью.
dnsdist_tlslocals: []

Принудительно переустановите пакеты dnsdist, выполнив удаление перед этапами установки пакета. 
Предназначен для использования там, где необходимо выполнить понижение версии dnsdist.
dnsdist_force_reinstall: False

Пример playbook
Разверните dnsdist перед Quad9 и включите веб-интерфейс мониторинга
- hosts: dnsdist
  roles:
    - { role: PowerDNS.dnsdist,
        dnsdist_servers: ['9.9.9.9'],
        dnsdist_webserver_address: "{{ ansible_default_ipv4['address'] }}:8083",
        dnsdist_webserver_password: 'geheim' }
		



