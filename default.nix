{ lib, pkgs, config, inputs, ... }:
with lib;                      
let
  #mainCFG = config.services.migrated_pjb70;
  mainCFG = config.pjb70_server;
  #migrated_pjb70=inputs.pjb70.packages.x86_64-linux.openerp-server;
  migrated_pjb70=inputs.pjb70.packages.x86_64-linux.migrated_pjb70;
  #migrated_pjb70 = import /home/jan/projects/migrated_pjb70.nix {};
  
 
in {
  options.pjb70_server = {
    enable = mkEnableOption "nixos-pjb70_server";
    
    config_file = mkOption {
      type = types.path;
      default = "/home/jan/projects/server_pjbrefct.conf";
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
          ExecStart = "${migrated_pjb70}/bin/openerp-server -c ${mainCFG.config_file}  --pidfile=${mainCFG.stateDir}/pjbrefct.pid";};
   };
    
  };


}
