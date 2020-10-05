{
  services.monitoring-services = {
    applicationDashboards = ./grafana/exchanges-monitor;

    applicationRules = [
      {
        alert = "exchange-down-binance";
        expr = "binance_active == 0";
        for = "10m";
        labels.severity = "page";
        annotations = {
          description = "{{$labels.alias}} withdraws/deposits down for >=10mins";
        };
      }
      {
        alert = "exchange-down-bittrex";
        expr = "bittrex_active == 0";
        for = "10m";
        labels.severity = "page";
        annotations = {
          description = "{{$labels.alias}} withdraws/deposits down for >=10mins";
        };
      }
      {
        alert = "exchange-down-bitthumb";
        expr = "bithumb_active == 0";
        for = "10m";
        labels.severity = "page";
        annotations = {
          description = "{{$labels.alias}} withdraws/deposits down for >=10mins";
        };
      }
      {
        alert = "exchange-down-hitbtc";
        expr = "hitbtc_withdraws == false or hitbtc_deposits == false";
        for = "10m";
        labels.severity = "page";
        annotations = {
          description = "{{$labels.alias}} withdraws/deposits down for >=10mins";
        };
      }
      {
        alert = "exchange-down-huobi";
        expr = "huobi_withdraws == false or huobi_deposits == false";
        for = "10m";
        labels.severity = "page";
        annotations = {
          description = "{{$labels.alias}} withdraws/deposits down for >=10mins";
        };
      }
      {
        alert = "exchange-down-coinex";
        expr = "coinex_withdraws == false or coinex_deposits == false";
        for = "10m";
        labels.severity = "page";
        annotations = {
          description = "{{$labels.alias}} withdraws/deposits down for >=10mins";
        };
      }
      {
        alert = "exchange-down-bitmax";
        expr = "bitmax_active == 0";
        for = "10m";
        labels.severity = "page";
        annotations = {
          description = "{{$labels.alias}} withdraws/deposits down for >=10mins";
        };
      }
        {
        alert = "exchange-down-bkex";
        expr = "bkex_withdraws == false or bkex_deposits == false";
        for = "10m";
        labels.severity = "page";
        annotations = {
          description = "{{$labels.alias}} withdraws/deposits down for >=10mins";
        };
        }
      {
        alert = "exchange-down-bitrue";
        expr = "bitrue_active == 0";
        for = "10m";
        labels.severity = "page";
        annotations = {
          description = "{{$labels.alias}} withdraws/deposits down for >=10mins";
        };
      }
      {
        alert = "exchange-down-exx";
        expr = "exx_active == 0";
        for = "10m";
        labels.severity = "page";
        annotations = {
          description = "{{$labels.alias}} withdraws/deposits down for >=10mins";
        };
      }
      {
        alert = "exchange-down-mxc";
        expr = "mxc_active == 0";
        for = "10m";
        labels.severity = "page";
        annotations = {
          description = "{{$labels.alias}} withdraws/deposits down for >=10mins";
        };
      }
    ];
  };
}
