pkgs: {

  deploymentName = "exchanges-monitor";

  dnsZone = "${pkgs.globals.domain}";

  domain = "cardano-exchanges.iohk.io";

  ec2 = {
    credentials = {
      accessKeyIds = {
        IOHK = "mainnet-iohk";
        dns = "mainnet-iohk";
      };
    };
  };
}
