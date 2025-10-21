### THIS FILE IS AUTO-GENERATED. DO NOT EDIT. ###

from typing import Literal, Optional

from openbb_core.app.model.field import OpenBBField
from openbb_core.app.model.obbject import OBBject
from openbb_core.app.static.container import Container
from openbb_core.app.static.utils.decorators import exception_handler, validate
from openbb_core.app.static.utils.filters import filter_inputs
from typing_extensions import Annotated


class ROUTER_equity_darkpool(Container):
    """/equity/darkpool
    otc
    """

    def __repr__(self) -> str:
        return self.__doc__ or ""

    @exception_handler
    @validate
    def otc(
        self,
        symbol: Annotated[
            Optional[str], OpenBBField(description="Symbol to get data for.")
        ] = None,
        provider: Annotated[
            Optional[Literal["finra"]],
            OpenBBField(
                description="The provider to use, by default None. If None, the priority list configured in the settings is used. Default priority: finra."
            ),
        ] = None,
        **kwargs
    ) -> OBBject:
        """Get the weekly aggregate trade data for Over The Counter deals.

        ATS and non-ATS trading data for each ATS/firm
        with trade reporting obligations under FINRA rules.


        Parameters
        ----------
        provider : str
            The provider to use, by default None. If None, the priority list configured in the settings is used. Default priority: finra.
        symbol : Optional[str]
            Symbol to get data for.
        tier : Literal['T1', 'T2', 'OTCE']
            "T1 - Securities included in the S&P 500, Russell 1000 and selected exchange-traded products;
            OTC - Over-the-Counter equity securities (provider: finra)
        is_ats : bool
            ATS data if true, NON-ATS otherwise (provider: finra)

        Returns
        -------
        OBBject
            results : list[OTCAggregate]
                Serializable results.
            provider : Optional[str]
                Provider name.
            warnings : Optional[list[Warning_]]
                list of warnings.
            chart : Optional[Chart]
                Chart object.
            extra : Dict[str, Any]
                Extra info.

        OTCAggregate
        ------------
        update_date : date
            Most recent date on which total trades is updated based on data received from each ATS/OTC.
        share_quantity : float
            Aggregate weekly total number of shares reported by each ATS for the Symbol.
        trade_quantity : float
            Aggregate weekly total number of trades reported by each ATS for the Symbol

        Examples
        --------
        >>> from openbb import obb
        >>> obb.equity.darkpool.otc(provider='finra')
        >>> # Get OTC data for a symbol
        >>> obb.equity.darkpool.otc(symbol='AAPL', provider='finra')
        """  # noqa: E501

        return self._run(
            "/equity/darkpool/otc",
            **filter_inputs(
                provider_choices={
                    "provider": self._get_provider(
                        provider,
                        "equity.darkpool.otc",
                        ("finra",),
                    )
                },
                standard_params={
                    "symbol": symbol,
                },
                extra_params=kwargs,
            )
        )
