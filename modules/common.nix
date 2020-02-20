with (import ../nix {});
{ ... }:
let
  boolOption = lib.mkOption {
    type = lib.types.bool;
    default = false;
  };
in {
  imports = [
    iohk-ops-lib.modules.common
  ];

  options = {
    node = {
      org = lib.mkOption {
        type = lib.types.enum [ "IOHK" "Emurgo" "CF" ];
        default = "IOHK";
      };
      roles = {
        isMonitor = boolOption;
      };
    };
  };
}
