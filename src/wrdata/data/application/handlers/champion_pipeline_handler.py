"""Handler for the champion data pipeline use case."""

from ...domain.ports.handlers import ChampionPipeline
from ...domain.ports.parsers import ChampionParser
from ...domain.ports.repositories import ChampionRepository


class ChampionPipelineHandler(ChampionPipeline):
    """Handles the champion data pipeline: parse → save.

    This is the application service that implements the inbound port.
    It orchestrates the business logic by coordinating between
    outbound ports (parser, repository).
    """

    def __init__(
        self,
        parser: ChampionParser,
        repository: ChampionRepository,
        source_url: str,
    ) -> None:
        """Initialize the handler with dependencies.

        Args:
            parser: Port for parsing champion data
            repository: Port for persisting champions
            source_url: URL to fetch champion data from
        """
        self._parser = parser
        self._repository = repository
        self._source_url = source_url

    def run(self) -> None:
        """Execute the complete pipeline: parse → save.

        This method orchestrates the entire workflow:
        1. Parse champions from the source URL (parser handles fetching)
        2. Save the parsed champions to storage

        The handler depends only on port interfaces, making it
        independent of specific infrastructure implementations.
        """
        # Pass URL directly to parser - it will handle the webdriver
        champions = self._parser.parse(self._source_url)

        self._repository.save(champions)
