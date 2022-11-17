#!/bin/sh

IP_ADDR=$(ip addr | grep inet | awk '{print $2}' | tail -n 2 | head -n 1)
ip_addr=${IP_ADDR%/*}
echo $ip_addr
