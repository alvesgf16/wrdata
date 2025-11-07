"""Handler for the champion data pipeline use case."""

from ...domain.ports.fetchers import WebFetcher
from ...domain.ports.handlers import ChampionPipeline
from ...domain.ports.parsers import ChampionParser
from ...domain.ports.repositories import ChampionRepository


class ChampionPipelineHandler(ChampionPipeline):
    """Handles the champion data pipeline: fetch → parse → save.

    This is the application service that implements the inbound port.
    It orchestrates the business logic by coordinating between
    outbound ports (fetcher, parser, repository).
    """

    def __init__(
        self,
        web_fetcher: WebFetcher,
        parser: ChampionParser,
        repository: ChampionRepository,
        source_url: str,
    ) -> None:
        """Initialize the handler with dependencies.

        Args:
            web_fetcher: Port for fetching web pages
            parser: Port for parsing champion data
            repository: Port for persisting champions
            source_url: URL to fetch champion data from
        """
        self._web_fetcher = web_fetcher
        self._parser = parser
        self._repository = repository
        self._source_url = source_url

    def run(self) -> None:
        """Execute the complete pipeline: fetch → parse → save.

        This method orchestrates the entire workflow:
        1. Fetch the web page from the source URL
        2. Parse champions from the fetched page
        3. Save the parsed champions to storage
        4. Clean up resources

        The handler depends only on port interfaces, making it
        independent of specific infrastructure implementations.
        """
        try:
            page = self._web_fetcher.fetch(self._source_url)

            champions = self._parser.parse(page)

            self._repository.save(champions)

        finally:
            self._web_fetcher.close()
