### THIS FILE IS AUTO-GENERATED. DO NOT EDIT. ###


from openbb_core.app.static.container import Container


class Extensions(Container):
    # fmt: off
    """
Routers:
    /commodity
    /crypto
    /currency
    /derivatives
    /econometrics
    /economy
    /equity
    /etf
    /fixedincome
    /index
    /news
    /quantitative
    /regulators
    /technical

Extensions:
    - commodity@1.2.2
    - crypto@1.3.2
    - currency@1.3.2
    - derivatives@1.3.2
    - econometrics@1.4.2
    - economy@1.3.2
    - equity@1.3.2
    - etf@1.3.2
    - fixedincome@1.3.2
    - index@1.3.2
    - news@1.3.2
    - quantitative@1.3.2
    - regulators@1.3.2
    - technical@1.3.2

    - alpha_vantage@1.3.2
    - benzinga@1.3.2
    - biztoc@1.3.2
    - bls@1.0.0
    - cboe@1.3.2
    - cftc@1.0.0
    - ecb@1.3.2
    - econdb@1.2.2
    - federal_reserve@1.3.2
    - finra@1.3.2
    - finviz@1.2.2
    - fmp@1.3.2
    - fred@1.3.2
    - government_us@1.3.2
    - intrinio@1.3.2
    - multpl@1.0.2
    - nasdaq@1.3.2
    - oecd@1.3.2
    - polygon@1.3.2
    - sec@1.3.2
    - seeking_alpha@1.3.2
    - stockgrid@1.3.2
    - tiingo@1.3.2
    - tmx@1.2.2
    - tradier@1.2.2
    - tradingeconomics@1.3.2
    - wsj@1.3.2
    - yfinance@1.3.3    """
    # fmt: on

    def __repr__(self) -> str:
        return self.__doc__ or ""

    @property
    def commodity(self):
        # pylint: disable=import-outside-toplevel
        from . import commodity

        return commodity.ROUTER_commodity(command_runner=self._command_runner)

    @property
    def crypto(self):
        # pylint: disable=import-outside-toplevel
        from . import crypto

        return crypto.ROUTER_crypto(command_runner=self._command_runner)

    @property
    def currency(self):
        # pylint: disable=import-outside-toplevel
        from . import currency

        return currency.ROUTER_currency(command_runner=self._command_runner)

    @property
    def derivatives(self):
        # pylint: disable=import-outside-toplevel
        from . import derivatives

        return derivatives.ROUTER_derivatives(command_runner=self._command_runner)

    @property
    def econometrics(self):
        # pylint: disable=import-outside-toplevel
        from . import econometrics

        return econometrics.ROUTER_econometrics(command_runner=self._command_runner)

    @property
    def economy(self):
        # pylint: disable=import-outside-toplevel
        from . import economy

        return economy.ROUTER_economy(command_runner=self._command_runner)

    @property
    def equity(self):
        # pylint: disable=import-outside-toplevel
        from . import equity

        return equity.ROUTER_equity(command_runner=self._command_runner)

    @property
    def etf(self):
        # pylint: disable=import-outside-toplevel
        from . import etf

        return etf.ROUTER_etf(command_runner=self._command_runner)

    @property
    def fixedincome(self):
        # pylint: disable=import-outside-toplevel
        from . import fixedincome

        return fixedincome.ROUTER_fixedincome(command_runner=self._command_runner)

    @property
    def index(self):
        # pylint: disable=import-outside-toplevel
        from . import index

        return index.ROUTER_index(command_runner=self._command_runner)

    @property
    def news(self):
        # pylint: disable=import-outside-toplevel
        from . import news

        return news.ROUTER_news(command_runner=self._command_runner)

    @property
    def quantitative(self):
        # pylint: disable=import-outside-toplevel
        from . import quantitative

        return quantitative.ROUTER_quantitative(command_runner=self._command_runner)

    @property
    def regulators(self):
        # pylint: disable=import-outside-toplevel
        from . import regulators

        return regulators.ROUTER_regulators(command_runner=self._command_runner)

    @property
    def technical(self):
        # pylint: disable=import-outside-toplevel
        from . import technical

        return technical.ROUTER_technical(command_runner=self._command_runner)
