#!/bin/sh

local_sources_dir=`pwd`
local_sources_script_dir=$local_sources_dir/scripts

source $local_sources_script_dir/rpi_ip.sh

rpi_scripts_dir=$rpi_src_path/scripts

# Create environment on RPI before copying
cd ..
ssh $ssh_arg $rpi_user@$rpi_ip "cd ~;mkdir -p $rpi_scripts_dir;" 

# Send scripts for make install/uninstall targets
scp $scp_arg -r $local_sources_script_dir/*.sh $rpi_user@$rpi_ip:$rpi_scripts_dir
scp $scp_arg $local_sources_script_dir/../update.sh $rpi_user@$rpi_ip:$rpi_scripts_dir/../

ssh $ssh_arg $rpi_user@$rpi_ip "chmod +x $rpi_scripts_dir/rpi_get_throttling_state.sh"
ssh $ssh_arg $rpi_user@$rpi_ip "chmod +x $rpi_scripts_dir/stop_service_if_running.sh"
ssh $ssh_arg $rpi_user@$rpi_ip "chmod +x $rpi_scripts_dir/update_host_ip_for_video_streaming.sh"
ssh $ssh_arg $rpi_user@$rpi_ip "chmod +x $rpi_scripts_dir/rpi_launch_udp_4k_soft_h264.sh"
ssh $ssh_arg $rpi_user@$rpi_ip "chmod +x $rpi_scripts_dir/rpi_launch_udp_1080p_mjpg.sh"
ssh $ssh_arg $rpi_user@$rpi_ip "chmod +x $rpi_scripts_dir/rpi_stop_video_stream.sh"
ssh $ssh_arg $rpi_user@$rpi_ip "chmod +x $rpi_scripts_dir/check_config_exists.sh"
ssh $ssh_arg $rpi_user@$rpi_ip "chmod +x $rpi_src_path/update.sh"
