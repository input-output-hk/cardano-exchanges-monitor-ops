import ../clusters/exchanges-monitor.nix (with (import ../nix {}).iohk-ops-lib.physical.libvirtd; {
  inherit targetEnv medium;
  xlarge = large;
  xlarge-monitor = large;
})
