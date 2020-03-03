pkgs: {

  deploymentName = "exchanges-monitor";

  dnsZone = "cardano-exchanges.iohk.io";

  domain = "${pkgs.globals.dnsZone}";

  ec2 = {
    credentials = {
      accessKeyIds = {
        IOHK = "mainnet-iohk";
        dns = "mainnet-iohk";
      };
    };
  };
}
