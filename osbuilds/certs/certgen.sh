#!/bin/bash

bCIRT_CERTS='./export/'
bCIRT_CA_CERTPASS='Password1.'
bCIRT_CLIENT1_CERTPASS='Client1'


sudo mkdir -p ${bCIRT_CERTS}/private/
sudo mkdir -p ${bCIRT_CERTS}/client/
sudo mkdir -p ${bCIRT_CERTS}/server/

# create CA cert
sudo openssl genrsa -des3 -passout pass:${bCIRT_CA_CERTPASS} -out ${bCIRT_CERTS}/private/ca.key 4096

sudo openssl req -new -x509 -days 365 -key ${bCIRT_CERTS}/private/ca.key -out ${bCIRT_CERTS}/private/ca.crt -passin pass:${bCIRT_CA_CERTPASS} --config=./certconf.conf

# Creating a Key and CSR for the Server
sudo openssl req -newkey rsa:4096 -nodes -keyout ${bCIRT_CERTS}/server/bcirt_server.key -out ${bCIRT_CERTS}/server/bcirt_server.csr --config=./certconf_server.conf
# Signing Server Certificate with previously created CA.
# Do not forget to change serial number. As it may conflict with existing one.
sudo openssl x509 -req -days 365 -set_serial 01 -in ${bCIRT_CERTS}/server/bcirt_server.csr -CA ${bCIRT_CERTS}/private/ca.crt -CAkey ${bCIRT_CERTS}/private/ca.key -passin pass:${bCIRT_CA_CERTPASS} -out ${bCIRT_CERTS}/server/bcirt_server.crt

# Creating a Key and CSR for the Client #1
sudo openssl req -newkey rsa:4096 -nodes -keyout ${bCIRT_CERTS}/client/client1.key -out ${bCIRT_CERTS}/client/client1.csr --config=./certconf_client.conf
# Signing the client certificate with previously created CA.
# Not: Do not forget to change serial each time you sign new certificate, otherwise may get serial conflict error in the web browsers.
sudo openssl x509 -req -days 365 -set_serial 02 -in ${bCIRT_CERTS}/client/client1.csr -CA ${bCIRT_CERTS}/private/ca.crt -CAkey ${bCIRT_CERTS}/private/ca.key -passin pass:${bCIRT_CA_CERTPASS} -out ${bCIRT_CERTS}/client/client1.crt

# Converting certificate and to pkcs12 format for the Windows clients
sudo openssl pkcs12 -export -out ${bCIRT_CERTS}/client/client1.pfx -inkey ${bCIRT_CERTS}/client/client1.key -in ${bCIRT_CERTS}/client/client1.crt -passout pass:${bCIRT_CLIENT1_CERTPASS} -certfile ${bCIRT_CERTS}/private/ca.crt
