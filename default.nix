{ lib, pkgs, config, inputs, ... }:
with lib;                      
let
  #mainCFG = config.services.migrated_pjb70;
  mainCFG = config.pjb70_server;
  #migrated_pjb70=inputs.pjb70.packages.x86_64-linux.openerp-server;
  migrated_pjb70=inputs.pjb70.packages.x86_64-linux.migrated_pjb70;
  pj_bridgman_addons=inputs.pj_bridgman.packages.x86_64-linux.default;
  migrated_pjb70_addons=inputs.migrated_pjb70_addons.packages.x86_64-linux.default;
  mvect2_transactical_addons=inputs.mvect2_transactical_addons.packages.x86_64-linux.transactical-addons;
  pjb_keyring=inputs.pjb_keyring.packages.x86_64-linux.default;
  run_in_loop=inputs.run_in_loop.packages.x86_64-linux.default;
  #migrated_pjb70 = import /home/jan/projects/migrated_pjb70.nix {};
  
 
in {
  options.pjb70_server = {
    enable = mkEnableOption "nixos-pjb70_server";
    
    config_file = mkOption {
      type = types.path;
      default = "${pjb_keyring}/server_pjbrefct.conf"; 
      #default = "/home/jan/projects/server_pjbrefct.conf";
    };

    stateDir = mkOption {
        type = types.path;
        default = "/home/jan/projects";
        description = ''
        '';
    };
    group = mkOption {
        type = types.str;
        default = "users";
        description = ''
        '';
      };

    user = mkOption {
        type = types.str;
        default = "jan";
        description = ''
        '';
      };
  };



  config = lib.mkIf mainCFG.enable {
    users.users.odoo = {    
      isNormalUser = true;       
      home = "/home/odoo";               
      description = "odoo";           
      extraGroups = [ "wheel" "dialout" "adbusers"]; # Enable ‘sudo’ for the user. 
      #uid = 1000; 
      openssh.authorizedKeys.keys = [ "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDGjW8vyQRsdU5yRF1Q/5CrIvxu7ga3pwGUSRd4unsZI5AQnrHvD+yjKu25Ug6ZcZtsvHM8FzgDaW26jRZ6CJ7Q/4IldnxBxDU6epFruoxegv6E/oNiAwGaj8xwdZ/g8+g5aHRbRN0PJeBQgBTKOHCZcv9DO1/dsz+eLPu1QfePsurLHWc9sI7v/iJtUPS3Lghwm/k5oYN2jDazeGcNMY0ZfGUThA2Adxx+PDgxcZ9b+zcy60nVFZwXbbWd4NUcZzBSF6WmrLVWzbcaxDTNx+qgm9vmQdqIJYB5bfeIobPsNzMA8IhzsJxwwbPZ4KcHvWdU4LqMrBXU4owiGuqkdSf jan@galtys" ]; 
    };

    systemd.services.migrated_pjb70  = {
      wantedBy = [ "multi-user.target" ];
      preStart =
            ''
              mkdir -m 0750 -p ${mainCFG.stateDir}
              #chown jan:${mainCFG.group} ${mainCFG.stateDir}
              #[ $(id -u) != 0 ] || chown root.${mainCFG.group} ${mainCFG.stateDir}
            '';
      
      serviceConfig = {
        User = mainCFG.user;
          Restart = lib.mkForce "always";
          RestartSec = 3;
          Group = mainCFG.group;
          PIDFile = "${mainCFG.stateDir}/pjbrefct.pid";
          ExecStart = "${migrated_pjb70}/bin/openerp-server --addons-path=${migrated_pjb70_addons}/addons,${pj_bridgman_addons}/addons,${mvect2_transactical_addons}/addons -c ${mainCFG.config_file}  --pidfile=${mainCFG.stateDir}/pjbrefct.pid";};
    };

    systemd.services.run_in_loop2  = {
      wantedBy = [ "multi-user.target" ];
      #preStart =
      #      ''
      #        mkdir -m 0750 -p ${mainCFG.stateDir}
      #        #chown jan:${mainCFG.group} ${mainCFG.stateDir}
      #        #[ $(id -u) != 0 ] || chown root.${mainCFG.group} ${mainCFG.stateDir}
      #      '';
      
      serviceConfig = {
        User = mainCFG.user;
          Restart = lib.mkForce "always";
          RestartSec = 30;
          Group = mainCFG.group;
          PIDFile = "${mainCFG.stateDir}/run_in_loop.pid";
          ExecStart = "${run_in_loop}/bin/run_in_loop2.py";};
    };


    
  };


}
